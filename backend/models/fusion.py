from .orbit_kalman import detect as orbit_detect, kalman_predict
from .comms_seq_model import detect as comms_detect, preprocess_sequence

ORBIT_THRESHOLD = 0.001
COMMS_THRESHOLD = 0.001

def fusion_anomaly(orbit_seq, comms_seq):
    # Step 1: Orbit error
    orbit_error = orbit_detect(kalman_predict(orbit_seq))

    # Step 2: Comms error
    comms_error = comms_detect(preprocess_sequence(comms_seq))

    # Step 3: Fusion logic
    fused_anomaly = orbit_error > ORBIT_THRESHOLD or comms_error > COMMS_THRESHOLD

    # Step 4: Return results
    return {
        "fused_anomaly": fused_anomaly,
        "orbit_error": orbit_error,
        "comms_error": comms_error
    }
