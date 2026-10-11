from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.station import ChargingStation
from app.schemas.station import StationCreate, StationResponse


router = APIRouter(
    prefix="/stations",
    tags=["Charging Stations"]
)


@router.post("/", response_model=StationResponse)
def create_station(
    station_data: StationCreate,
    db: Session = Depends(get_db)
):
    station = ChargingStation(
        station_name=station_data.station_name,
        location=station_data.location,
        total_power_capacity=station_data.total_power_capacity,
        status=station_data.status
    )

    db.add(station)
    db.commit()
    db.refresh(station)

    return station


@router.get("/", response_model=list[StationResponse])
def get_stations(
    db: Session = Depends(get_db)
):
    return db.query(ChargingStation).all()