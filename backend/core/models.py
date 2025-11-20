from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class Anomaly(Base):
    __tablename__ = "anomalies"
id = Column(Integer, primary_key=True, index=True)
satellite_id = Column(String, index=True)
metric = Column(String)
value = Column(Float)
severity = Column(String)
timestamp = Column(DateTime, default=datetime.utcnow)
