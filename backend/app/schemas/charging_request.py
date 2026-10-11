from datetime import datetime
from pydantic import BaseModel
class ChargingRequestCreate(BaseModel):
    ev_id: int
    station_id:int
    required_energy: float
    expected_departure_time:datetime
class ChargingRequestResponse(ChargingRequestCreate):
    request_id:int
    requested_at:datetime
    priority_score:float
    status:str
    class Config:
        from_attributes=True
        
