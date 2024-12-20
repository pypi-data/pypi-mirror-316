from setuptools import setup, find_packages

setup(
    name="LatentBoostClassifier",  # Package name
    version="1.0.0",               # Initial release version
    author="Ali Bavarchee",
    author_email="ali.bavarchee@gmail.com",
    description="A hybrid generative model combining CVAE, CGAN, and Random Forest.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AliBavarchee/LatentBoostClassifier",  # Replace with your repo URL
    packages=find_packages(),      # Automatically find packages in the directory
    install_requires=[
        "tensorflow>=2.8.0",
        "keras-tuner>=1.1.0",
        "scikit-learn>=1.0",
        "matplotlib>=3.4",
        "seaborn>=0.11"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
