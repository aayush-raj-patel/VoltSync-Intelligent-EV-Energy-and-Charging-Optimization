from pydantic import BaseModel


class ChargerCreate(BaseModel):
    station_id: int
    charger_type: str
    max_power: float
    status: str = "AVAILABLE"


class ChargerResponse(ChargerCreate):
    charger_id: int

    class Config:
        from_attributes = True