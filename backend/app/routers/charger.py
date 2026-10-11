from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.charger import Charger
from app.models.station import ChargingStation
from app.schemas.charger import ChargerCreate, ChargerResponse


router = APIRouter(
    prefix="/chargers",
    tags=["Chargers"]
)


@router.post("/", response_model=ChargerResponse)
def create_charger(
    charger_data: ChargerCreate,
    db: Session = Depends(get_db)
):

    station = db.query(ChargingStation).filter(
        ChargingStation.station_id == charger_data.station_id
    ).first()

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Charging station not found"
        )

    charger = Charger(
        station_id=charger_data.station_id,
        charger_type=charger_data.charger_type,
        max_power=charger_data.max_power,
        status=charger_data.status
    )

    db.add(charger)
    db.commit()
    db.refresh(charger)

    return charger


@router.get("/", response_model=list[ChargerResponse])
def get_chargers(
    db: Session = Depends(get_db)
):
    return db.query(Charger).all()


@router.get("/{charger_id}", response_model=ChargerResponse)
def get_charger(
    charger_id: int,
    db: Session = Depends(get_db)
):

    charger = db.query(Charger).filter(
        Charger.charger_id == charger_id
    ).first()

    if not charger:
        raise HTTPException(
            status_code=404,
            detail="Charger not found"
        )

    return charger