# backend/models/comms_seq_model.py

import numpy as np
from tensorflow.keras.models import load_model

# ---------------------------
# 1. Load LSTM Autoencoder model
# ---------------------------
# Replace 'comms_lstm_model.h5' with your trained model file
model = load_model("comms_lstm_model.h5")

# Define sequence length and number of features (update to match your training)
seq_len = 50
n_features = 4  # e.g., signal features like amplitude, frequency, phase, etc.

# ---------------------------
# 2. Function to compute reconstruction error
# ---------------------------
def detect(sequence):
    """
    Compute reconstruction error for a sequence using LSTM autoencoder.
    Higher error indicates anomaly.
    """
    seq = np.array(sequence).reshape(1, seq_len, n_features)
    recon = model.predict(seq, verbose=0)
    error = np.mean((seq - recon) ** 2)
    return error

# ---------------------------
# 3. Optional: helper function to preprocess sequences
# ---------------------------
def preprocess_sequence(sequence):
    """
    Example preprocessing: normalize, reshape, or pad sequence.
    """
    seq = np.array(sequence)
    if seq.shape[0] < seq_len:
        # pad with zeros if sequence is too short
        pad_width = seq_len - seq.shape[0]
        seq = np.pad(seq, ((0, pad_width), (0, 0)), 'constant')
    return seq[:seq_len]  # trim if longer
from backend.models import detect, preprocess_sequence

seq = preprocess_sequence(my_raw_sequence)
error = detect(seq)

if error > 0.001:  # threshold based on training
    print("Anomaly detected in communication sequence!")
