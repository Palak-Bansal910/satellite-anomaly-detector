# backend/models/sensor_autoencoderwith_temp.py

"""
Simplified sensor + temperature anomaly detector for demo.

Instead of a TensorFlow autoencoder, we use simple rule-based checks
to compute an anomaly score between 0 and 1.
"""

from typing import Dict, Tuple


def detect(features: Dict[str, float]) -> Tuple[float, str]:
    """
    Detect anomaly based on sensor readings and temperature.

    Args:
        features: dict with keys like:
            - sensor_temp_c
            - battery_level_pct
            - comm_signal_db
            - orbit_altitude_km (optional)

    Returns:
        score (float): 0–1 anomaly score
        message (str): explanation
    """
    temp = features.get("sensor_temp_c")
    battery = features.get("battery_level_pct")
    signal = features.get("comm_signal_db")

    score = 0.0
    reasons = []

    # Temperature checks
    if temp is not None:
        if temp > 80:
            score += 0.6
            reasons.append(f"High temperature {temp:.1f} °C")
        elif temp > 60:
            score += 0.3
            reasons.append(f"Elevated temperature {temp:.1f} °C")
        elif temp < -20:
            score += 0.4
            reasons.append(f"Very low temperature {temp:.1f} °C")

    # Battery checks
    if battery is not None:
        if battery < 15:
            score += 0.4
            reasons.append(f"Low battery {battery:.1f}%")
        elif battery < 30:
            score += 0.2
            reasons.append(f"Weak battery {battery:.1f}%")

    # Signal strength checks
    if signal is not None:
        # e.g. -120 dB = very weak, -50 dB = strong
        if signal < -110:
            score += 0.4
            reasons.append(f"Very weak signal {signal:.1f} dB")
        elif signal < -90:
            score += 0.2
            reasons.append(f"Weak signal {signal:.1f} dB")

    # Cap score
    if score == 0.0:
        message = "Sensor & temperature nominal"
    else:
        if score > 1.0:
            score = 1.0
        message = "; ".join(reasons)

    return score, message
