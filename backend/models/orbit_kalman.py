# backend/models/orbit_kalman.py

from orbit_kf.filter import ExtendedKalmanFilter
from orbit_kf.propagation import CowellPropagator  # example propagator
from .sensor_autoencoderwith_temp import detect as detect_sensor_anomaly
from .comms_seq_model import detect as detect_comms_anomaly
from .fusion import fusion_anomaly  # uses your existing fusion function

def run_kf_with_anomaly_detection(init_state, init_cov, measurements):
    """
    Run Kalman filter with anomaly detection using sensor and comms models.
    
    Args:
        init_state (np.array): initial state vector
        init_cov (np.array): initial covariance matrix
        measurements (list of np.array): measurement sequence
    
    Returns:
        x, P: final state estimate and covariance
    """
    # Initialize Extended Kalman Filter with Cowell propagator
    kf = ExtendedKalmanFilter(propagator=CowellPropagator())
    x, P = kf.initialize(init_state, init_cov)

    for idx, z in enumerate(measurements):
        # Kalman filter prediction and update
        x, P = kf.predict(x, P)
        x, P = kf.update(x, P, z)

        # Compute residual or innovation
        residual = z - kf.H.dot(x)  # or kf.innovation if defined

        # Run anomaly detection models
        sensor_score = detect_sensor_anomaly(residual)
        comms_score = detect_comms_anomaly(residual)

        # Fuse results
        anomaly_result = fusion_anomaly(
            orbit_seq=[residual],      # residual for orbit anomaly
            comms_seq=[residual]       # residual for comms anomaly
        )
        anomaly_flag = anomaly_result['fused_anomaly']

        # Optional: print or log anomaly
        if anomaly_flag:
            print(f"⚠️ Anomaly detected at measurement index {idx}: {z}")
            print(f"Details -> Orbit error: {anomaly_result['orbit_error']:.6f}, "
                  f"Comms error: {anomaly_result['comms_error']:.6f}")

    return x, P



    





   


    

    




