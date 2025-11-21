# simulator/simulator.py
import time
import random
import requests
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

from telemetry_simulator import TelemetrySimulator
from temp_anomalies import TempAnomalyInjector
from sensor_failures import SensorFailureInjector
from comms_anomalies import CommsAnomalyInjector

BACKEND_URL = "http://127.0.0.1:8000/telemetry/"

SEND_INTERVAL_SECONDS = 3.0  # how often to send telemetry per sat


def build_pipeline(sat_id: str):
    base = TelemetrySimulator(satellite_id=sat_id)
    # chain injectors: base -> temp -> sensor -> comms
    temp = TempAnomalyInjector(base)
    sensor = SensorFailureInjector(temp)
    comms = CommsAnomalyInjector(sensor)
    return comms  # top of pipeline


def main():
    satellites = ["SAT-1", "SAT-2", "SAT-3"]
    sims = {sid: build_pipeline(sid) for sid in satellites}

    print(f"Starting simulator for {len(satellites)} satellites.")
    print(f"Sending telemetry to {BACKEND_URL}")

    try:
        while True:
            for sid, sim in sims.items():
                data = sim.step(SEND_INTERVAL_SECONDS)

                try:
                    resp = requests.post(BACKEND_URL, json=data, timeout=3)
                    if not resp.ok:
                        print(f"[{sid}] backend error {resp.status_code}: {resp.text}")
                    else:
                        print(f"[{sid}] sent at {data['timestamp']}")
                except Exception as e:
                    print(f"[{sid}] failed to send: {e}")

                # small stagger so they don't all hit at the exact same ms
                time.sleep(0.3)

            # global pacing
            time.sleep(SEND_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("Simulator stopped.")


if __name__ == "__main__":
    main()
