import json
import os
from datetime import datetime

from sqlalchemy.orm import Session
from dotenv import load_dotenv

# Import from backend
from core.database import SessionLocal
from core import models

# Load .env
load_dotenv()

DATA_FILE = os.getenv("NASA_DATA_FILE", "nasa_telemetry.json")


def load_json_data(filepath: str):
    """Load NASA telemetry data from JSON file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"❌ Data file not found: {filepath}")

    with open(filepath, "r") as f:
        return json.load(f)


def insert_telemetry_record(db: Session, record: dict):
    """Insert a telemetry record into PostgreSQL."""

    telemetry = models.Telemetry(
        satellite_id=record["satellite_id"],
        timestamp=datetime.fromisoformat(record["timestamp"]),
        temperature=record["temperature"],
        battery_voltage=record["battery_voltage"],
        solar_panel_current=record["solar_panel_current"],
        position_x=record["position"]["x"],
        position_y=record["position"]["y"],
        position_z=record["position"]["z"],
        velocity_x=record["velocity"]["x"],
        velocity_y=record["velocity"]["y"],
        velocity_z=record["velocity"]["z"],
    )

    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    print(f"✔ Stored telemetry for satellite {record['satellite_id']} at {record['timestamp']}")


def run():
    print("\n🚀 NASA Telemetry Data Importer Started")

    # Load data
    data = load_json_data(DATA_FILE)
    print(f"📄 Loaded {len(data)} NASA records")

    db = SessionLocal()

    try:
        for rec in data:
            insert_telemetry_record(db, rec)

    finally:
        db.close()

    print("\n🎉 All NASA telemetry data stored successfully!")


if __name__ == "__main__":
    run()
