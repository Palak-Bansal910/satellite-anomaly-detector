# simulator/temp_anomalies.py
import random
from typing import Dict

try:
    from .telemetry_simulator import TelemetrySimulator
except ImportError:
    from simulator.telemetry_simulator import TelemetrySimulator


class TempAnomalyInjector:
    """
    Wraps a TelemetrySimulator and occasionally injects temperature anomalies:
    - payload overheating
    - battery overheating
    """

    def __init__(self, base_sim: TelemetrySimulator,
                 overheat_probability: float = 0.05,
                 burst_length_range=(5, 20)):
        self.base_sim = base_sim
        self.overheat_probability = overheat_probability
        self.burst_length_range = burst_length_range
        self.burst_remaining = 0
        self.mode = None  # "payload" or "battery"

    def step(self, dt_seconds: float = 5.0) -> Dict:
        data = self.base_sim.step(dt_seconds)

        # manage bursts
        if self.burst_remaining <= 0:
            # maybe start a new burst
            if random.random() < self.overheat_probability:
                self.burst_remaining = random.randint(*self.burst_length_range)
                self.mode = random.choice(["payload", "battery"])
        else:
            self.burst_remaining -= 1

        if self.burst_remaining > 0:
            if self.mode == "payload":
                data["temp_payload"] += random.uniform(10, 25)  # serious overheating
            elif self.mode == "battery":
                data["temp_battery"] += random.uniform(8, 18)

        return data
