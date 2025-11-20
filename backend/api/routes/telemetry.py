# backend/api/routes/telemetry.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Any, Dict

from backend.services.preprocess import preprocess_telemetry
from backend.services.anomaly_engine import compute_anomaly
from backend.services.state import add_anomaly_record
from backend.core.database import SessionLocal
from backend.core.models import AnomalyEvent
from backend.core.logger import logger   # note: absolute import, no "..."


# Single router for telemetry
router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


# ----- Pydantic schema -----
class Telemetry(BaseModel):
    timestamp: str
    satellite_id: str

    position_x: float
    position_y: float
    position_z: float

    velocity_x: float
    velocity_y: float
    velocity_z: float

    temp_payload: float
    temp_battery: float
    temp_bus: float

    sensor1_value: float
    sensor2_value: float
    sensor3_value: float

    comms_rssi: float
    comms_snr: float
    comms_packet_loss: float


# ----- Main endpoint -----
@router.post("/", status_code=200)
async def receive_telemetry(data: Telemetry):
    """
    Ingest a single telemetry sample, run preprocessing + anomaly detection,
    store result in memory and DB, and return anomaly summary.
    """
    try:
        logger.info(f"Received telemetry for {data.satellite_id} at {data.timestamp}")

        # Convert to dict for downstream functions
        payload: Dict[str, Any] = data.dict()

        # 1) Preprocess features (expects dict)
        features = preprocess_telemetry(payload)

        # 2) Run anomaly engine (make sure this works with dict, not attributes!)
        anomaly: Dict[str, Any] = compute_anomaly(features)

        # Prepare record to keep history
        record = {
            "timestamp": data.timestamp,
            "satellite_id": data.satellite_id,
            "anomaly": anomaly,
        }

        # 3) Add to in-memory state
        add_anomaly_record(record)

        # 4) Persist to DB
        db = SessionLocal()
        try:
            db_event = AnomalyEvent(
                timestamp=data.timestamp,
                satellite_id=data.satellite_id,
                severity=anomaly.get("severity", "normal"),
                issues=",".join(anomaly.get("issues", [])),
                score=float(anomaly.get("score", 0.0)),
            )
            db.add(db_event)
            db.commit()
        finally:
            db.close()

        return {"status": "ok", **record}

    except Exception as e:
        logger.error(f"Error in /telemetry: {e}")
        raise HTTPException(status_code=500, detail=str(e))
