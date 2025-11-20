# backend/services/state.py
from collections import deque

LATEST_ANOMALIES = deque(maxlen=200)

def add_anomaly_record(record: dict):
    LATEST_ANOMALIES.append(record)

def get_latest_anomalies():
    # newest first
    return list(LATEST_ANOMALIES)[::-1]
