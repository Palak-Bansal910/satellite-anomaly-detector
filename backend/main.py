from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from core import models, schemas
from core.database import engine, get_db
from datetime import datetime

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Satellite Telemetry Backend")

@app.post("/telemetry/")
def receive_telemetry(data: schemas.TelemetrySchema, db: Session = Depends(get_db)):
    telemetry = models.Telemetry(**data.dict())
    db.add(telemetry)
    db.commit()
    db.refresh(telemetry)

    # Example anomaly logic
    issues = []
    score = 0
    severity = "normal"

    if telemetry.temperature and telemetry.temperature > 70:
        issues.append("High Temperature")
        score += 0.6
    if telemetry.packet_loss and telemetry.packet_loss > 10:
        issues.append("High Packet Loss")
        score += 0.8

    if len(issues) == 1:
        severity = "warning"
    elif len(issues) >= 2:
        severity = "critical"

    if issues:
        anomaly = models.Anomaly(
            satellite_id=telemetry.satellite_id,
            severity=severity,
            issue=", ".join(issues),
            score=score
        )
        db.add(anomaly)
        db.commit()
        db.refresh(anomaly)

    return {"status": "ok", "anomaly_detected": bool(issues)}

@app.get("/anomalies/latest")
def get_latest_anomalies(db: Session = Depends(get_db)):
    anomalies = db.query(models.Anomaly).order_by(models.Anomaly.timestamp.desc()).limit(10).all()
    return anomalies

