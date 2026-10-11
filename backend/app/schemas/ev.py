from pydantic import BaseModel


class EVCreate(BaseModel):
    user_id: int
    model: str
    license_plate: str
    battery_capacity: float
    current_battery_level: float
    charging_type: str
    vehicle_priority: int = 1


class EVResponse(EVCreate):
    ev_id: int

    class Config:
        from_attributes = True