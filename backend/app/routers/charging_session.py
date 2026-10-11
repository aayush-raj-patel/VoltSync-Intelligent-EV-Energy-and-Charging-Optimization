from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.charging_session import ChargingSession
from app.models.charging_request import ChargingRequest
from app.models.charger import Charger
from app.schemas.charging_session import (
    ChargingSessionCreate,
    ChargingSessionResponse
)


router = APIRouter(
    prefix="/charging-sessions",
    tags=["Charging Sessions"]
)


@router.post("/", response_model=ChargingSessionResponse)
def create_charging_session(
    session_data: ChargingSessionCreate,
    db: Session = Depends(get_db)
):

    request = db.query(ChargingRequest).filter(
        ChargingRequest.request_id == session_data.request_id
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Charging request not found"
        )

    charger = db.query(Charger).filter(
        Charger.charger_id == session_data.charger_id
    ).first()

    if not charger:
        raise HTTPException(
            status_code=404,
            detail="Charger not found"
        )

    if charger.status != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Charger is not available"
        )

    session = ChargingSession(
        request_id=session_data.request_id,
        ev_id=session_data.ev_id,
        charger_id=session_data.charger_id,
        station_id=session_data.station_id,
        power_allocated=session_data.power_allocated,
        energy_delivered=0,
        status="ACTIVE"
    )

    charger.status = "OCCUPIED"

    request.status = "CHARGING"

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


@router.get(
    "/",
    response_model=list[ChargingSessionResponse]
)
def get_all_sessions(
    db: Session = Depends(get_db)
):
    return db.query(ChargingSession).all()


@router.get(
    "/{session_id}",
    response_model=ChargingSessionResponse
)
def get_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    session = db.query(ChargingSession).filter(
        ChargingSession.session_id == session_id
    ).first()

    if not session:
        raise HTTPException(
            status_code=404,
            detail="Charging session not found"
        )

    return session