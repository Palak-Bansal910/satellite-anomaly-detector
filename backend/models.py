from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

# Telemetry table
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

# Anomaly table
class Anomaly(Base):
    __tablename__ = "anomalies"
    id = Column(Integer, primary_key=True, index=True)
    satellite_id = Column(String, index=True)
    severity = Column(String)
    issue = Column(String)
    score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

