import numpy as np
from typing import Union, Dict

def preprocess_telemetry(data: Union[Dict, object]) -> np.ndarray:
    """
Convert Telemetry dict or object into numeric feature vector.
Keep ordering consistent with anomaly_engine expectations.
"""
    if isinstance(data, dict):
        get_attr = lambda key: data.get(key) or data[key]
    else:
        get_attr = lambda key: getattr(data, key)
    
    return np.array([
        get_attr("position_x"),
        get_attr("position_y"),
        get_attr("position_z"),
        get_attr("velocity_x"),
        get_attr("velocity_y"),
        get_attr("velocity_z"),
        get_attr("temp_payload"),
        get_attr("temp_battery"),
        get_attr("temp_bus"),
        get_attr("sensor1_value"),
        get_attr("sensor2_value"),
        get_attr("sensor3_value"),
        get_attr("comms_rssi"),
        get_attr("comms_snr"),
        get_attr("comms_packet_loss"),
    ], dtype=float)