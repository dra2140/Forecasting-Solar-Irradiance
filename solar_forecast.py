import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt
import os

def load_data(data_path):
    """
    Load preprocessed solar irradiance data
    """
    # Load the preprocessed data
    data = pd.read_csv(os.path.join(data_path, 'preprocessed_data.csv'))
    
    # Set datetime index
    data['datetime'] = pd.to_datetime(data['Date'])
    data.set_index('datetime', inplace=True)
    
    # Drop the original Date column if it exists
    if 'Date' in data.columns:
        data = data.drop('Date', axis=1)
    
    return data

def create_sequences(data, seq_length):
    """
    Create sequences for LSTM model
    """
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data.iloc[i:(i + seq_length)].values)
        y.append(data.iloc[i + seq_length]['GHI'])
    return np.array(X), np.array(y)

def build_model(seq_length, n_features):
    """
    Build LSTM model for solar irradiance forecasting
    """
    model = Sequential([
        LSTM(64, input_shape=(seq_length, n_features), return_sequences=True),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def train_model(model, X_train, y_train, X_val, y_val, epochs=50, batch_size=32):
    """
    Train the LSTM model
    """
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        verbose=1
    )
    return history

def plot_results(history, y_true, y_pred):
    """
    Plot training history and predictions
    """
    # Plot training history
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Plot predictions
    plt.subplot(1, 2, 2)
    plt.plot(y_true, label='Actual')
    plt.plot(y_pred, label='Predicted')
    plt.title('Solar Irradiance Forecast')
    plt.xlabel('Time')
    plt.ylabel('GHI (W/m²)')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    # Load data
    data_path = 'California/LA'
    data = load_data(data_path)
    
    # Normalize data
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    data_scaled = pd.DataFrame(data_scaled, columns=data.columns, index=data.index)
    
    # Create sequences
    seq_length = 24  # 24 hours
    X, y = create_sequences(data_scaled, seq_length)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    
    # Build and train model
    model = build_model(seq_length, X.shape[2])
    history = train_model(model, X_train, y_train, X_val, y_val)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Inverse transform predictions
    y_true = scaler.inverse_transform(np.concatenate([X_test[:, -1, :-1], y_test.reshape(-1, 1)], axis=1))[:, -1]
    y_pred = scaler.inverse_transform(np.concatenate([X_test[:, -1, :-1], y_pred], axis=1))[:, -1]
    
    # Plot results
    plot_results(history, y_true, y_pred)

if __name__ == "__main__":
    main() 