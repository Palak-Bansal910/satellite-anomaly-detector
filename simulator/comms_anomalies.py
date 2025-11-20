# simulator/comms_anomalies.py
import random
from typing import Dict
from .telemetry_simulator import TelemetrySimulator


class CommsAnomalyInjector:
    """
    Introduces periods of degraded comms:
    - lower RSSI, lower SNR
    - higher packet loss
    """

    def __init__(self, base_sim: TelemetrySimulator,
                 outage_probability: float = 0.04,
                 event_length_range=(8, 30)):
        self.base_sim = base_sim
        self.outage_probability = outage_probability
        self.event_length_range = event_length_range
        self.event_remaining = 0

    def step(self, dt_seconds: float = 5.0) -> Dict:
        data = self.base_sim.step(dt_seconds)

        if self.event_remaining <= 0:
            if random.random() < self.outage_probability:
                self.event_remaining = random.randint(*self.event_length_range)
        else:
            self.event_remaining -= 1

        if self.event_remaining > 0:
            data["comms_rssi"] -= random.uniform(8, 18)          # weaker signal
            data["comms_snr"] -= random.uniform(6, 12)           # worse SNR
            data["comms_packet_loss"] = min(1.0, max(
                data["comms_packet_loss"] + random.uniform(0.15, 0.4), 0.0
            ))

        return data
