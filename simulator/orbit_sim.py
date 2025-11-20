# simulator/orbit_sim.py
import math
from dataclasses import dataclass
from typing import Dict
from datetime import datetime, timezone


@dataclass
class OrbitParams:
    satellite_id: str
    radius_km: float = 7000.0
    inclination_deg: float = 0.0
    period_minutes: float = 90.0


class OrbitSimulator:
    """
    Lightweight orbit-only simulator for visualization.
    """

    def __init__(self, params: OrbitParams):
        self.params = params
        self.theta = 0.0
        self.angular_speed = 2 * math.pi / (params.period_minutes * 60.0)

    def _now_iso(self):
        return datetime.now(timezone.utc).isoformat()

    def step(self, dt_seconds: float = 10.0) -> Dict:
        self.theta = (self.theta + self.angular_speed * dt_seconds) % (2 * math.pi)

        inc = math.radians(self.params.inclination_deg)
        r = self.params.radius_km

        # inclined circular orbit
        x = r * math.cos(self.theta)
        y = r * math.sin(self.theta) * math.cos(inc)
        z = r * math.sin(self.theta) * math.sin(inc)

        return {
            "timestamp": self._now_iso(),
            "satellite_id": self.params.satellite_id,
            "position_x": x,
            "position_y": y,
            "position_z": z,
        }
