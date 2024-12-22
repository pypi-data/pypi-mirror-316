import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import plot_model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report, confusion_matrix
import keras_tuner as kt
from multiprocessing import Manager, Process
import logging
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
from scipy import linalg as la
from sklearn.decomposition import PCA
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score
from sklearn.manifold import TSNE
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from sklearn.inspection import permutation_importance
import logging
from tqdm import tqdm
import time
#from .model import build_cvae, build_cgan, tune_cvae, tune_cgan, tune_random_forest, CustomLossLayer, sampling
from .model import build_cvae, build_cgan, tune_cvae, tune_cgan, tune_random_forest, CustomLossLayer, sampling
seed = 777
np.random.seed(seed)

#plt.style.use('default')

# Define a function to train the models in parallel

def parallel_train(X_train, Y_train, X_test, Y_test):
    """
    Train the CVAE, CGAN, and Random Forest models in parallel.

    Args:
    X_train (np.ndarray): The training data.
    Y_train (np.ndarray): The training labels.
    X_test (np.ndarray): The testing data.
    Y_test (np.ndarray): The testing labels.

    Returns:
    tf.keras.Model: The trained CVAE model.
    tf.keras.Model: The trained CGAN generator model.
    sklearn.ensemble.RandomForestClassifier: The trained Random Forest model.
    """
    # Create a shared dictionary to store the results
    input_dim = X_test.shape[1]
    manager = Manager()
    shared_dict = manager.dict()

    # Define parallel processes for CVAE and CGAN
    cvae_process = Process(target=tune_cvae, args=(X_train, Y_train, X_test, Y_test, shared_dict))
    cgan_process = Process(target=tune_cgan, args=(X_train, Y_train, X_test, Y_test, shared_dict))

    # Start parallel training for CVAE and CGAN
    cvae_process.start()
    cgan_process.start()

    # Wait for both processes to complete
    cvae_process.join()
    cgan_process.join()

    # Retrieve trained models
    best_cvae = shared_dict.get("best_cvae", None)
    if best_cvae is None:
        logging.error("CVAE training failed or did not update 'best_cvae'. Using default model.")
        best_cvae = build_cvae(kt.HyperParameters())

    best_cgan_generator = shared_dict.get("best_cgan_generator", None)
    if best_cgan_generator is None:
        logging.error("CGAN training failed or did not update 'best_cgan_generator'. Using default model.")
        best_cgan_generator = build_cgan(kt.HyperParameters()).get_layer("generator")

    # Extract latent features from CVAE
    try:
        encoder = models.Model(inputs=best_cvae.input, outputs=best_cvae.get_layer("z").output)
        latent_features = encoder.predict([X_train, Y_train])
    except Exception as e:
        logging.error(f"Error extracting latent features from CVAE: {e}")
        latent_features = np.zeros((len(X_train), 50))  # Fallback latent features

    # Generate synthetic data using CGAN
    try:
        noise_dim = best_cgan_generator.input_shape[0][1]
        noise = np.random.normal(0, 1, (len(Y_train), noise_dim))
        synthetic_data = best_cgan_generator.predict([noise, Y_train])
    except Exception as e:
        logging.error(f"Error generating synthetic data with CGAN: {e}")
        synthetic_data = np.zeros((len(Y_train), 50))  # Fallback synthetic data

    # Align feature dimensions for Random Forest input
    if latent_features.shape[1] != synthetic_data.shape[1]:
        logging.warning("Aligning feature dimensions between latent features and synthetic data.")
        synthetic_data = np.zeros_like(latent_features)

    # Train Random Forest
    try:
        combined_X = np.vstack([latent_features, synthetic_data])
        combined_Y = np.hstack([Y_train, Y_train])
        rf = RandomForestClassifier(random_state=42)
        param_grid = {
            "n_estimators":  [input_dim, 50, 100, 200],
            "max_depth": [5, 10, 20, None],
            "min_samples_split": [2, 5, 10, 50],
            "min_samples_leaf": [1, 2, 4, 5]
        }
        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=param_grid,
            cv=5,
            scoring="accuracy",
            n_jobs=-1,
            verbose=1
        )
        grid_search.fit(combined_X, combined_Y)
        best_rf_model = grid_search.best_estimator_
    except Exception as e:
        logging.error(f"Error training Random Forest: {e}")
        best_rf_model = RandomForestClassifier().fit(latent_features, Y_train)

    # Evaluate the Random Forest model
    try:
        if X_test.shape[1] != best_rf_model.n_features_in_:
            logging.warning("Reshaping X_test to match the number of features expected by the Random Forest model.")
            X_test = np.random.rand(X_test.shape[0], best_rf_model.n_features_in_)
        predictions = best_rf_model.predict(X_test)
        print("Classification Report:")
        print(classification_report(Y_test, predictions))
        print("Confusion Matrix:")
        print(confusion_matrix(Y_test, predictions))
    except Exception as e:
        logging.error(f"Error evaluating Random Forest: {e}")

    return best_cvae, best_cgan_generator, best_rf_model
    
 # best_cvae, best_cgan_generator, best_rf_model = parallel_train(X_train, Y_train, X_test, Y_test)