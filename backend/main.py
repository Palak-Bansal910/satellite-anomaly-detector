from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)
app = FastAPI(title="SkyHack Anomaly Backend")


# dependency
def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()


@app.post('/anomalies', response_model=schemas.Anomaly)
def post_anomaly(anomaly: schemas.AnomalyCreate, db: Session = Depends(get_db)):
return crud.create_anomaly(db, anomaly)


@app.get('/anomalies', response_model=list[schemas.Anomaly])
def get_anomalies(limit: int = 50, db: Session = Depends(get_db)):
return crud.list_anomalies(db, limit=limit)


@app.get('/')
def root():
return {"status": "ok"}
