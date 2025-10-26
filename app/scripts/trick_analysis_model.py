import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import Input
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from fastapi import FastAPI, HTTPException

def train_lstm_model(ollie_dataset_path):
    # Load the dataset
    try:
        df = pd.read_csv(ollie_dataset_path)
        print(df.head())
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to load dataset: {str(e)}")

    # Ensure all pose data is numeric
    X = df.drop('label', axis=1).apply(pd.to_numeric, errors='coerce')
    y = df['label']

    # Convert labels to numeric using LabelEncoder
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)

    # Handle NaN values
    if X.isnull().values.any():
        print("NaN values found in the dataset, replacing with 0")
        X = X.fillna(0)

    # Prepare data for LSTM (reshape it to be 3D: samples, timesteps, features)
    timesteps = 10

    def create_sequences(data, labels, timesteps):
        X_seq, y_seq = [], []
        for i in range(len(data) - timesteps):
            X_seq.append(data.iloc[i:(i + timesteps), :].values)  # Exclude the label column
            y_seq.append(labels[i + timesteps])  # Label is the trick (perfect Ollie)
        return np.array(X_seq), np.array(y_seq)

    X_seq, y_seq = create_sequences(X, y, timesteps)

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X_seq, y_seq, test_size=0.2, random_state=42)

    # Build the LSTM model
    model = Sequential()

    # Define the input shape for the first LSTM layer
    model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))

    # First LSTM layer with dropout to prevent overfitting
    model.add(LSTM(units=100, return_sequences=True))
    model.add(Dropout(0.2))

    # Second LSTM layer
    model.add(LSTM(units=100, return_sequences=False))
    model.add(Dropout(0.2))

    # Output layer
    model.add(Dense(1, activation='sigmoid'))

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, epochs=20, batch_size=64, validation_split=0.2)

    # Evaluate the model
    loss, accuracy = model.evaluate(X_test, y_test)

    # Save the model
    model.save("trick_analysis_model.h5")

    return {"accuracy": accuracy, "loss": loss, "message": "Model training completed and saved as 'trick_analysis_model.h5'"}
