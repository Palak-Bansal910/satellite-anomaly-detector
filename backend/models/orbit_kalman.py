# backend/models/orbit_kalman.py

from .sensor_autoencoderwith_temp import detect as detect_sensor_anomaly
from .comms_seq_model import detect as detect_comms_anomaly
from .fusion import fusion_anomaly  # uses your existing fusion function

# backend/models/orbit_kalman.py

"""
Simplified orbit drift detector for demo purposes.

We DON'T use a real Kalman filter here to avoid extra dependencies.
We just compute a basic drift score based on change in altitude/inclination.
"""

from typing import Dict, Any, Tuple


def kalman_predict(prev_state: Dict[str, float], obs: Dict[str, float]) -> Dict[str, float]:
    """
    Dummy 'prediction' step: just blend previous state and current observation.
    """
    if not prev_state:
        return obs

    alpha = 0.7  # weight for previous state
    beta = 1 - alpha

    new_state = {}
    for key in ["orbit_altitude_km", "orbit_inclination_deg"]:
        prev_val = prev_state.get(key)
        obs_val = obs.get(key)
        if prev_val is None:
            new_state[key] = obs_val
        elif obs_val is None:
            new_state[key] = prev_val
        else:
            new_state[key] = alpha * prev_val + beta * obs_val

    return new_state


def detect(prev_state: Dict[str, float], obs: Dict[str, float]) -> Tuple[float, str, Dict[str, float]]:
    """
    Detect orbit drift given previous and current orbit state.

    Returns:
        score (float): 0–1 anomaly score
        message (str): human-readable description
        new_state (dict): updated tracked state
    """
    new_state = kalman_predict(prev_state, obs)

    alt_prev = prev_state.get("orbit_altitude_km")
    alt_now = obs.get("orbit_altitude_km")
    inc_prev = prev_state.get("orbit_inclination_deg")
    inc_now = obs.get("orbit_inclination_deg")

    score = 0.0
    reasons = []

    if alt_prev is not None and alt_now is not None:
        alt_diff = abs(alt_now - alt_prev)
        # crude thresholding
        if alt_diff > 50:
            score += 0.6
            reasons.append(f"Altitude jump {alt_diff:.1f} km")
        elif alt_diff > 20:
            score += 0.3
            reasons.append(f"Altitude change {alt_diff:.1f} km")

    if inc_prev is not None and inc_now is not None:
        inc_diff = abs(inc_now - inc_prev)
        if inc_diff > 5:
            score += 0.4
            reasons.append(f"Inclination jump {inc_diff:.1f}°")
        elif inc_diff > 2:
            score += 0.2
            reasons.append(f"Inclination change {inc_diff:.1f}°")

    score = min(score, 1.0)
    if not reasons:
        message = "Orbit stable"
    else:
        message = "; ".join(reasons)

    return score, message, new_state





