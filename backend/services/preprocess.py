import numpy as np
from ..api.schemas import Telemetry




def preprocess_telemetry(data: Telemetry) -> np.ndarray:
"""
Convert Telemetry object into numeric feature vector.
Keep ordering consistent with anomaly_engine expectations.
"""
return np.array([
data.position_x,
data.position_y,
data.position_z,
data.velocity_x,
data.velocity_y,
data.velocity_z,
data.temp_payload,
data.temp_battery,
data.temp_bus,
data.sensor1_value,
data.sensor2_value,
data.sensor3_value,
data.comms_rssi,
data.comms_snr,
data.comms_packet_loss,
], dtype=float)