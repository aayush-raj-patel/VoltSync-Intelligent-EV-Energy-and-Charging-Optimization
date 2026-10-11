from pydantic import BaseModel


class StationCreate(BaseModel):
    station_name: str
    location: str
    total_power_capacity: float
    status: str = "ACTIVE"


class StationResponse(StationCreate):
    station_id: int

    class Config:
        from_attributes = True