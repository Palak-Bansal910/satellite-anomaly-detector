
from pydantic import BaseModel
from datetime import datetime

class TelemetrySchema(BaseModel):
    satellite_id: str
    temperature: float | None = None
    rssi: float | None = None
    snr: float | None = None
    packet_loss: float | None = None
    position_x: float | None = None
    position_y: float | None = None
    position_z: float | None = None
    velocity_x: float | None = None
    velocity_y: float | None = None
    velocity_z: float | None = None
    battery_voltage: float | None = None
    solar_panel_current: float | None = None
    timestamp: datetime

<<<<<<< HEAD
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
=======
class AnomalySchema(BaseModel):
    satellite_id: str
    severity: str
    issue: str
    score: float
    timestamp: datetime

>>>>>>> 352a09d13b15722bc231abf761a5364341257ee6
