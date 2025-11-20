# orbit_anomaly_detection_with_temp.py

import numpy as np
from tensorflow.keras.models import load_model
from pykalman import KalmanFilter

# ---------------------------
# 1. Load LSTM Autoencoder
# ---------------------------
# Make sure your autoencoder was trained with the same number of features (x, y, z, temp)
model = load_model("lstm_model.h5")

# Define sequence length and number of features
seq_len = 50      # Number of time steps in each sequence
n_features = 4    # Features per time step: x, y, z, temp

# ---------------------------
# 2. Reconstruction error function
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
# 3. Kalman filter prediction function
# ---------------------------
def kalman_predict(orbit_seq):
    """
    Smooth orbit sequence using Kalman filter.
    orbit_seq: numpy array of shape (seq_len, n_features)
    Returns: smoothed sequence of same shape
    """
    kf = KalmanFilter(
        transition_matrices=np.eye(n_features),
        observation_matrices=np.eye(n_features),
        initial_state_mean=orbit_seq[0],
        observation_covariance=np.eye(n_features) * 0.01,
        transition_covariance=np.eye(n_features) * 0.001
    )
    state_means, _ = kf.filter(orbit_seq)
    return state_means

# ---------------------------
# 4. Load orbit sequences
# ---------------------------
# Each sequence should have shape: (seq_len, n_features)
# Example placeholder with random data:
# orbit_data = [np.random.rand(seq_len, n_features) for _ in range(10)]
orbit_data = ...  # Replace with your actual sequences (x, y, z, temp)

# ---------------------------
# 5. Set anomaly detection threshold
# ---------------------------
# Calculate from normal sequences: mean + 2*std of reconstruction errors
threshold = 0.001  # adjust based on your data

# ---------------------------
# 6. Run anomaly detection
# ---------------------------
for i, seq in enumerate(orbit_data):
    # 1. Smooth sequence with Kalman filter
    kalman_seq = kalman_predict(seq)

    # 2. Compute reconstruction error (autoencoder)
    error = detect(kalman_seq)

    # 3. Check for anomaly
    if error > threshold:
        print(f"[ALERT] Sequence {i}: Anomaly detected! Error = {error:.6f}")
    else:
        print(f"Sequence {i}: Normal orbit. Error = {error:.6f}")
