from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.charging_request import ChargingRequest
from app.models.ev import EV
from app.models.station import ChargingStation
from app.schemas.charging_request import (
    ChargingRequestCreate,
    ChargingRequestResponse
)


router = APIRouter(
    prefix="/charging-requests",
    tags=["Charging Requests"]
)


@router.post("/", response_model=ChargingRequestResponse)
def create_charging_request(
    request_data: ChargingRequestCreate,
    db: Session = Depends(get_db)
):

    ev = db.query(EV).filter(
        EV.ev_id == request_data.ev_id
    ).first()

    if not ev:
        raise HTTPException(
            status_code=404,
            detail="EV not found"
        )

    station = db.query(ChargingStation).filter(
        ChargingStation.station_id == request_data.station_id
    ).first()

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Charging station not found"
        )

    request = ChargingRequest(
        ev_id=request_data.ev_id,
        station_id=request_data.station_id,
        required_energy=request_data.required_energy,
        expected_departure_time=request_data.expected_departure_time,
        priority_score=0,
        status="WAITING"
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return request


@router.get(
    "/",
    response_model=list[ChargingRequestResponse]
)
def get_all_requests(
    db: Session = Depends(get_db)
):
    return db.query(ChargingRequest).all()


@router.get(
    "/{request_id}",
    response_model=ChargingRequestResponse
)
def get_request(
    request_id: int,
    db: Session = Depends(get_db)
):

    request = db.query(ChargingRequest).filter(
        ChargingRequest.request_id == request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Charging request not found"
        )

    return request