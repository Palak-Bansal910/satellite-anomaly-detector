# backend/api/routes/telemetry.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ...services.preprocess import preprocess_telemetry
from ...services.anomaly_engine import compute_anomaly
from ...services.state import add_anomaly_record
from ...core.database import SessionLocal
from ...core.models import AnomalyEvent
from ...core.logger import logger

router = APIRouter(prefix="/telemetry", tags=["Telemetry"])

# Define Pydantic schema inline or import from api/schemas.py if you prefer
class TelemetrySchema(BaseModel):
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

@router.post("/", status_code=200)
async def receive_telemetry(data: TelemetrySchema):
    try:
        logger.info(f"Received telemetry for {data.satellite_id} at {data.timestamp}")
        features = preprocess_telemetry(data.dict())
        anomaly = compute_anomaly(features)

        record = {
            "timestamp": data.timestamp,
            "satellite_id": data.satellite_id,
            "anomaly": anomaly
        }

        # add to in-memory
        add_anomaly_record(record)

        # persist to DB
        db = SessionLocal()
        try:
            db_event = AnomalyEvent(
                timestamp=data.timestamp,
                satellite_id=data.satellite_id,
                severity=anomaly.get("severity", "normal"),
                issues=",".join(anomaly.get("issues", [])),
                score=float(anomaly.get("score", 0.0))
            )
            db.add(db_event)
            db.commit()
        finally:
            db.close()

        return {"status": "ok", **record}
    except Exception as e:
        logger.error(f"Error in /telemetry: {e}")
        raise HTTPException(status_code=500, detail=str(e))
