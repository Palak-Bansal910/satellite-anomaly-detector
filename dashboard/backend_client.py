# dashboard/backend_client.py

import os
import requests
from typing import Dict, Any, List

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def send_telemetry_sample(sample: Dict[str, Any]) -> Dict[str, Any]:
   
    url = f"{API_BASE_URL}/telemetry/"
    resp = requests.post(url, json=sample, timeout=5)
    resp.raise_for_status()
    return resp.json()

def fetch_anomaly_history() -> List[Dict[str, Any]]:
    """
    Fetch history from /anomalies/history.
    """
    url = f"{API_BASE_URL}/anomalies/history"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()
