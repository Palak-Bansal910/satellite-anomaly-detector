from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnomalyCreate(BaseModel):
    satellite_id: str
    metric: str
    value: float
    severity: Optional[str] = "low"


class Anomaly(BaseModel):
    id: int
    satellite_id: str
    metric: str
    value: float
    severity: str
    timestamp: datetime


class Config:
    orm_mode = True
