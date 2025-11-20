# simulator/telemetry_simulator.py
import math
import random
from datetime import datetime, timezone


class TelemetrySimulator:
    """
    Generates baseline 'healthy' telemetry for a satellite in LEO-like orbit.
    Other anomaly modules will wrap / modify this.
    """

    def __init__(self, satellite_id: str = "SAT-1", orbit_radius_km: float = 7000.0):
        self.satellite_id = satellite_id
        self.orbit_radius_km = orbit_radius_km
        self.theta = 0.0  # angle along orbit in radians
        self.angular_speed = 2 * math.pi / (60 * 90)  # one orbit in ~90 minutes

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def step(self, dt_seconds: float = 5.0) -> dict:
        """
        Advance simulation by dt_seconds and return a telemetry dict.
        """
        self.theta = (self.theta + self.angular_speed * dt_seconds) % (2 * math.pi)

        # simple circular orbit in XY-plane
        x = self.orbit_radius_km * math.cos(self.theta)
        y = self.orbit_radius_km * math.sin(self.theta)
        z = random.uniform(-50, 50)  # small oscillation

        # approximate velocity components
        v_mag = self.orbit_radius_km * self.angular_speed
        vx = -v_mag * math.sin(self.theta)
        vy = v_mag * math.cos(self.theta)
        vz = random.uniform(-0.5, 0.5)

        # nominal temperatures
        temp_payload = random.gauss(35, 1.5)
        temp_battery = random.gauss(30, 1.0)
        temp_bus = random.gauss(28, 1.0)

        # nominal sensor values
        sensor1 = random.gauss(100, 3)
        sensor2 = random.gauss(102, 3)
        sensor3 = random.gauss(98, 3)

        # nominal comms
        comms_rssi = random.gauss(-80, 2)         # dBm
        comms_snr = random.gauss(12, 1.5)         # dB
        comms_packet_loss = max(0.0, random.gauss(0.01, 0.003))

        return {
            "timestamp": self._now_iso(),
            "satellite_id": self.satellite_id,
            "position_x": x,
            "position_y": y,
            "position_z": z,
            "velocity_x": vx,
            "velocity_y": vy,
            "velocity_z": vz,
            "temp_payload": temp_payload,
            "temp_battery": temp_battery,
            "temp_bus": temp_bus,
            "sensor1_value": sensor1,
            "sensor2_value": sensor2,
            "sensor3_value": sensor3,
            "comms_rssi": comms_rssi,
            "comms_snr": comms_snr,
            "comms_packet_loss": comms_packet_loss,
        }
