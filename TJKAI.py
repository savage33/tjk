# -*- coding: utf-8 -*-
"""
Created on Fri Nov 4 16:50:28 2022

Author: Savage33

Description: Data preprocessing, feature engineering, and model training pipeline.
"""

import os
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path, sheet_name="Sheet1"):
    """Load dataset from an Excel file."""
    try:
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        logging.info(f"Data loaded successfully from {file_path}.")
        return data
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        raise

def preprocess_data(data):
    """Preprocess data: split features and target, apply encoding and scaling."""
    X = data.iloc[:, :8].values
    y = data.iloc[:, 8:].values

    # One-Hot Encode categorical variables
    ohe = ColumnTransformer([("ohe", OneHotEncoder(dtype=float), [1])], remainder="passthrough")
    X = ohe.fit_transform(X)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

    # Scale features
    scaler = StandardScaler(with_mean=False)
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    logging.info("Data preprocessing complete.")
    return X_train, X_test, y_train, y_test

def apply_pca(X_train, X_test, n_components=2):
    """Apply PCA for dimensionality reduction."""
    pca = PCA(n_components=n_components)
    X_train_pca = pca.fit_transform(X_train)
    X_test_pca = pca.transform(X_test)
    logging.info("PCA transformation complete.")
    return X_train_pca, X_test_pca

def build_model(input_dim):
    """Build and compile a simple neural network model."""
    model = Sequential([
        Dense(64, activation='relu', input_dim=input_dim),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    logging.info("Model built and compiled.")
    return model

def main():
    """Main function to execute the data processing and model training pipeline."""
    # Define file path
    file_path = r"C:\Users\Savage33\OneDrive\Masaüstü\TJK_islenmis.xlsx"

    # Load and preprocess data
    data = load_data(file_path)
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Apply PCA
    X_train_pca, X_test_pca = apply_pca(X_train, X_test)

    # Build and train model
    model = build_model(X_train_pca.shape[1])
    model.fit(X_train_pca, y_train, epochs=10, batch_size=32, validation_split=0.2)
    logging.info("Model training complete.")

    # Evaluate model
    y_pred = (model.predict(X_test_pca) > 0.5).astype("int32")
    cm = confusion_matrix(y_test, y_pred)
    logging.info(f"Confusion Matrix:\n{cm}")

if __name__ == "__main__":
    main()
