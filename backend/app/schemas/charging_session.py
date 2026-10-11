from pydantic import BaseModel
from datetime import datetime


class ChargingSessionCreate(BaseModel):
    request_id: int
    ev_id: int
    charger_id: int
    station_id: int
    power_allocated: float


class ChargingSessionResponse(ChargingSessionCreate):
    session_id: int
    start_time: datetime
    end_time: datetime | None
    energy_delivered: float
    status: str

    class Config:
        from_attributes = True