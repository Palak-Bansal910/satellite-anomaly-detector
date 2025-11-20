from fastapi import APIRouter, HTTPException
from ..schemas import Telemetry
from ...services.preprocess import preprocess_telemetry
from ...services.anomaly_engine import compute_anomaly
from ...services.state import add_anomaly_record
from ...core.db import SessionLocal
from ...models.anomaly_event import AnomalyEvent


router = APIRouter(prefix="/telemetry", tags=["Telemetry"])


@router.post("/")
async def receive_telemetry(data: Telemetry):
try:
    features = preprocess_telemetry(data)
    anomaly = compute_anomaly(features)


record = {
"timestamp": data.timestamp,
"satellite_id": data.satellite_id,
"anomaly": anomaly
}


# add to in-memory state
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
raise HTTPException(status_code=500, detail=str(e))