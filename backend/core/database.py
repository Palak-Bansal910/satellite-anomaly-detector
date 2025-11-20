from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
from dotenv import load_dotenv

# Load .env
load_dotenv()

# PostgreSQL DB URL from .env
DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/telemetry")

# Create engine
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ----------------- Telemetry Table -----------------
class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(String, index=True)
    temperature = Column(Float, nullable=True)
    rssi = Column(Float, nullable=True)
    snr = Column(Float, nullable=True)
    packet_loss = Column(Float, nullable=True)
    position_x = Column(Float, nullable=True)
    position_y = Column(Float, nullable=True)
    position_z = Column(Float, nullable=True)
    velocity_x = Column(Float, nullable=True)
    velocity_y = Column(Float, nullable=True)
    velocity_z = Column(Float, nullable=True)
    battery_voltage = Column(Float, nullable=True)
    solar_panel_current = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

# ----------------- Anomaly Table -----------------
class Anomaly(Base):
    __tablename__ = "anomalies"
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(String, index=True)
    severity = Column(String)
    issue = Column(String)
    score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

# ----------------- Initialize DB -----------------
def init_db():
    Base.metadata.create_all(bind=engine)
