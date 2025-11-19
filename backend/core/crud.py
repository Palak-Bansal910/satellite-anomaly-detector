from sqlalchemy.orm import Session
from . import models, schemas

# Create a new anomaly
def create_anomaly(db: Session, anomaly: schemas.AnomalyCreate):
    db_anomaly = models.Anomaly(**anomaly.dict())
    db.add(db_anomaly)
    db.commit()
    db.refresh(db_anomaly)
    return db_anomaly

# Get all anomalies
def get_anomalies(db: Session):
    return db.query(models.Anomaly).all()

# Get anomaly by ID
def get_anomaly(db: Session, anomaly_id: int):
    return db.query(models.Anomaly).filter(models.Anomaly.id == anomaly_id).first()
