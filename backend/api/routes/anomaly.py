# backend/api/routes/anomaly.py
from fastapi import APIRouter, Query
from backend.services.state import get_latest_anomalies
from backend.core.database import SessionLocal
from backend.core.models import AnomalyEvent

router = APIRouter(prefix="/anomalies", tags=["Anomalies"])

@router.get("/latest")
def latest_anomalies():
    return {"data": get_latest_anomalies()}

@router.get("/history")
def anomaly_history(limit: int = Query(50, ge=1, le=200)):
    db = SessionLocal()
    try:
        rows = (
            db.query(AnomalyEvent)
            .order_by(AnomalyEvent.id.desc())
            .limit(limit)
            .all()
        )
        result = [
            {
                "timestamp": r.timestamp,
                "satellite_id": r.satellite_id,
                "severity": r.severity,
                "issues": r.issues.split(",") if r.issues else [],
                "score": r.score,
            } for r in rows
        ]
        return {"data": result}
    finally:
        db.close()
