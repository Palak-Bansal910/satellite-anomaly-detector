import numpy as np




def compute_anomaly(features: np.ndarray) -> dict:
    """
    Simple rule-based anomaly detection for hackathon prototype.
    Replace with ML models later.
    """
# Index mapping (same as preprocess):
# 0-2 pos, 3-5 vel, 6 temp_payload, 7 temp_battery, 8 temp_bus, 9-11 sensors, 12 rssi, 13 snr, 14 packet_loss


    temp_payload = float(features[6])
    temp_battery = float(features[7])
    comms_packet_loss = float(features[14])


    issues = []


    if temp_payload > 70:
        issues.append("HIGH_PAYLOAD_TEMPERATURE")


    if temp_battery > 60:
        issues.append("HIGH_BATTERY_TEMPERATURE")


    if comms_packet_loss > 0.2:
        issues.append("HIGH_PACKET_LOSS")


    # Example sensor failure heuristic: large variance across sensors
    sensor_vals = features[9:12]
    if np.std(sensor_vals) > 50:
        issues.append("SENSOR_INCONSISTENCY")


    if not issues:
        severity = "normal"
    elif len(issues) == 1:
        severity = "warning"
    else:
        severity = "critical"


    # score normalization (simple)
    score = min(1.0, len(issues) / 3.0)


    return {
        "severity": severity,
        "issues": issues,
        "score": score
    }