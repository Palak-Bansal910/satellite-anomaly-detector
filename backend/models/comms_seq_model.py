# backend/models/comms_seq_model.py

"""
Simplified communication pattern anomaly detector for demo.

Instead of a trained sequence model (LSTM/autoencoder),
we use simple rule-based checks on:
- gaps between contact times
- sudden drop in packets
- unexpected spike in error rate
"""

from typing import Dict, Tuple


def detect(features: Dict[str, float]) -> Tuple[float, str]:
    """
    Args:
        features: dict with keys like:
            - avg_contact_gap_min      (float) average minutes between contacts
            - last_gap_min             (float) minutes since last contact
            - packets_per_min          (float)
            - error_rate_pct           (float)
            - downlink_success_ratio   (float 0–1, optional)

    Returns:
        score (float): 0–1 anomaly score
        message (str): explanation
    """

    gap_avg = features.get("avg_contact_gap_min")
    gap_last = features.get("last_gap_min")
    packets = features.get("packets_per_min")
    err = features.get("error_rate_pct")
    success = features.get("downlink_success_ratio")

    score = 0.0
    reasons = []

    # 1) Communication gap anomaly
    if gap_avg is not None and gap_last is not None:
        # if last gap is much larger than typical
        if gap_last > 3 * gap_avg:
            score += 0.6
            reasons.append(
                f"Long outage: last gap {gap_last:.1f} min vs avg {gap_avg:.1f} min"
            )
        elif gap_last > 2 * gap_avg:
            score += 0.3
            reasons.append(
                f"Extended contact gap {gap_last:.1f} min vs avg {gap_avg:.1f} min"
            )

    # 2) Throughput / packets anomaly
    if packets is not None:
        if packets < 5:
            score += 0.3
            reasons.append(f"Very low traffic {packets:.1f} packets/min")
        elif packets < 15:
            score += 0.15
            reasons.append(f"Low traffic {packets:.1f} packets/min")

    # 3) Error rate anomaly
    if err is not None:
        if err > 40:
            score += 0.5
            reasons.append(f"High error rate {err:.1f}%")
        elif err > 20:
            score += 0.25
            reasons.append(f"Elevated error rate {err:.1f}%")

    # 4) Downlink success ratio (optional)
    if success is not None:
        if success < 0.5:
            score += 0.4
            reasons.append(f"Poor downlink success {success * 100:.1f}%")
        elif success < 0.8:
            score += 0.2
            reasons.append(f"Weak downlink success {success * 100:.1f}%")

    # Finalize
    if score == 0.0:
        message = "Communication pattern nominal"
    else:
        score = min(score, 1.0)
        message = "; ".join(reasons)

    return score, message
