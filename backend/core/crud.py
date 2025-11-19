from sqlalchemy.orm import Session
from . import models, schemas

# --- Anomaly CRUD ---
def create_anomaly(db: Session, anomaly: schemas.AnomalyCreate):
    db_anomaly = models.Anomaly(**anomaly.dict())
    db.add(db_anomaly)
    db.commit()
    db.refresh(db_anomaly)
    return db_anomaly

def get_anomalies(db: Session):
    return db.query(models.Anomaly).all()

def get_anomaly(db: Session, anomaly_id: int):
    return db.query(models.Anomaly).filter(models.Anomaly.id == anomaly_id).first()

# --- User CRUD ---
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()
