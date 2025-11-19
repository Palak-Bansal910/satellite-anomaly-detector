from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core import schemas, crud
from core.database import SessionLocal

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new anomaly
@router.post("/anomalies/", response_model=schemas.Anomaly)
def create_anomaly_route(anomaly: schemas.AnomalyCreate, db: Session = Depends(get_db)):
    return crud.create_anomaly(db, anomaly)

# Get all anomalies
@router.get("/anomalies/", response_model=list[schemas.Anomaly])
def get_anomalies_route(db: Session = Depends(get_db)):
    return crud.get_anomalies(db)

# Get anomaly by ID
@router.get("/anomalies/{anomaly_id}", response_model=schemas.Anomaly)
def get_anomaly_route(anomaly_id: int, db: Session = Depends(get_db)):
    anomaly = crud.get_anomaly(db, anomaly_id)
    if not anomaly:
        raise HTTPException(status_code=404, detail="Anomaly not found")
    return anomaly
