def visualize_hybrid_model(best_cvae, best_cgan_generator, rf_model, X_test, Y_test, X_train, Y_train):
    """
    Visualizes the results of the hybrid model including latent space visualization,
    synthetic data comparison, and classification performance.
    """
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
    from sklearn.manifold import TSNE

    # 1. Extract latent features from CVAE for test data
    encoder = models.Model(inputs=best_cvae.input, outputs=best_cvae.get_layer("z").output)
    latent_features_test = encoder.predict([X_test, Y_test])

    # 2. Generate synthetic data using CGAN for test data
    noise_dim = best_cgan_generator.input_shape[0][1]
    noise_test = np.random.normal(0, 1, (len(Y_test), noise_dim))
    synthetic_data_test = best_cgan_generator.predict([noise_test, Y_test])

    # 3. Combine latent features and synthetic data for test set
    combined_test_features = np.hstack([latent_features_test, synthetic_data_test])

    # Adjust feature dimensions silently
    if combined_test_features.shape[1] != rf_model.n_features_in_:
        combined_test_features = combined_test_features[:, :rf_model.n_features_in_]

    # 4. Evaluate the Random Forest model
    predictions = rf_model.predict(combined_test_features)
    print("Classification Report:")
    print(classification_report(Y_test, predictions))
    print("Confusion Matrix:")
    conf_matrix = confusion_matrix(Y_test, predictions)
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Class 0", "Class 1"], yticklabels=["Class 0", "Class 1"])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.show()

    # 5. Latent Space Visualization
    latent_features_train = encoder.predict([X_train, Y_train])
    tsne = TSNE(n_components=2, random_state=42)
    latent_2d = tsne.fit_transform(latent_features_train)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=latent_2d[:, 0], y=latent_2d[:, 1], hue=Y_train.ravel(), palette="viridis")
    plt.title("Latent Space Visualization (t-SNE)")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.legend(title="Class")
    plt.show()

    # 6. ROC Curve and AUC
    probabilities = rf_model.predict_proba(combined_test_features)[:, 1]
    fpr, tpr, _ = roc_curve(Y_test, probabilities)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC Curve (AUC = {roc_auc:.2f})")
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Receiver Operating Characteristic")
    plt.legend(loc="lower right")
    plt.show()
# visualize_hybrid_model(best_cvae, best_cgan_generator, best_rf_model, X_test, Y_test, X_train, Y_train)