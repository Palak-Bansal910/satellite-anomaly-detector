# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..core.database import Base, engine
from ..core.logger import logger

# Import routers
from .routes import telemetry, anomaly, alerts

# create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured.")

app = FastAPI(title="Satellite Anomaly Detector", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(telemetry.router, prefix="/telemetry", tags=["telemetry"])
app.include_router(anomaly.router, prefix="/anomalies", tags=["anomalies"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
@app.get("/")
def root():
    return {"message": "Satellite Anomaly Detector Backend is running"}
