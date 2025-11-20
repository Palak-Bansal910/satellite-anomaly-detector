# simulator/sensor_failures.py
import random
from typing import Dict

try:
    from .telemetry_simulator import TelemetrySimulator
except ImportError:
    from simulator.telemetry_simulator import TelemetrySimulator


class SensorFailureInjector:
    """
    Randomly introduces sensor glitches:
    - hard failure (stuck at constant value)
    - drifting sensor
    """

    def __init__(self, base_sim: TelemetrySimulator,
                 failure_probability: float = 0.03,
                 drift_probability: float = 0.03,
                 event_length_range=(10, 40)):
        self.base_sim = base_sim
        self.failure_probability = failure_probability
        self.drift_probability = drift_probability
        self.event_length_range = event_length_range

        self.event = None  # None | "stuck1" | "stuck2" | "drift3"
        self.event_remaining = 0
        self.stuck_value = None
        self.drift_offset = 0.0

    def step(self, dt_seconds: float = 5.0) -> Dict:
        data = self.base_sim.step(dt_seconds)

        # event lifecycle
        if self.event_remaining <= 0:
            self.event = None
            # maybe start a new event
            r = random.random()
            if r < self.failure_probability:
                self.event = random.choice(["stuck1", "stuck2"])
                self.event_remaining = random.randint(*self.event_length_range)
                if self.event == "stuck1":
                    self.stuck_value = data["sensor1_value"]
                else:
                    self.stuck_value = data["sensor2_value"]
            elif r < self.failure_probability + self.drift_probability:
                self.event = "drift3"
                self.event_remaining = random.randint(*self.event_length_range)
                self.drift_offset = 0.0
        else:
            self.event_remaining -= 1

        # apply events
        if self.event == "stuck1":
            data["sensor1_value"] = self.stuck_value
        elif self.event == "stuck2":
            data["sensor2_value"] = self.stuck_value
        elif self.event == "drift3":
            self.drift_offset += random.uniform(-1.0, 1.5)
            data["sensor3_value"] += self.drift_offset

        return data
