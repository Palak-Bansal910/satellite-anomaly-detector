# backend/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import telemetry, anomaly
from ..core.database import Base, engine
from ..core.logger import logger

# in main.py (where other routers are included)
from .routes import telemetry, anomaly, alerts

# create tables
Base.metadata.create_all(bind=engine)
logger.info("Database tables ensured.")

app = FastAPI(title="Satellite Anomaly Detector API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(telemetry.router)
app.include_router(anomaly.router)
app.include_router(alerts.router)
@app.get("/")
def root():
    return {"message": "Satellite Anomaly Detector Backend is running"}
