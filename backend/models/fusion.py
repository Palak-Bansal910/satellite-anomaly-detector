# backend/models/fusion.py

"""
Simple fusion logic that combines scores from
orbit, sensor, and communication anomaly detectors.

Each detector returns a score in [0, 1].
We take a weighted average + derive a label.
"""

from typing import Optional, Dict, Any


def fusion_anomaly(
    orbit_score: Optional[float] = None,
    sensor_score: Optional[float] = None,
    comms_score: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Returns:
        {
            "fusion_score": float,
            "severity": "NORMAL" | "WARNING" | "CRITICAL",
            "details": {...}
        }
    """

    scores = []
    details = {}

    if orbit_score is not None:
        scores.append(("orbit", orbit_score))
    if sensor_score is not None:
        scores.append(("sensor", sensor_score))
    if comms_score is not None:
        scores.append(("comms", comms_score))

    if not scores:
        return {
            "fusion_score": 0.0,
            "severity": "NORMAL",
            "details": {"reason": "No scores available"},
        }

    # Simple weighted average: you can tune weights if needed
    weights = {
        "orbit": 0.4,
        "sensor": 0.3,
        "comms": 0.3,
    }

    num = 0.0
    den = 0.0
    for name, s in scores:
        w = weights.get(name, 0.3)
        num += w * s
        den += w
        details[name] = s

    fusion_score = num / den if den > 0 else 0.0

    # Severity thresholds – tweak if needed
    if fusion_score < 0.3:
        severity = "NORMAL"
    elif fusion_score < 0.6:
        severity = "WARNING"
    else:
        severity = "CRITICAL"

    return {
        "fusion_score": fusion_score,
        "severity": severity,
        "details": details,
    }
