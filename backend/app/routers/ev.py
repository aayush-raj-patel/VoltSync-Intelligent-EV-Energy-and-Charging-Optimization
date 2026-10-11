from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ev import EV
from app.schemas.ev import EVCreate, EVResponse

router = APIRouter(
    prefix="/evs",
    tags=["EVs"]
)


@router.post("/", response_model=EVResponse)
def create_ev(
    ev_data: EVCreate,
    db: Session = Depends(get_db)
):
    ev = EV(
        user_id=ev_data.user_id,
        model=ev_data.model,
        license_plate=ev_data.license_plate,
        battery_capacity=ev_data.battery_capacity,
        current_battery_level=ev_data.current_battery_level,
        charging_type=ev_data.charging_type,
        vehicle_priority=ev_data.vehicle_priority
    )

    db.add(ev)
    db.commit()
    db.refresh(ev)

    return ev


@router.get("/", response_model=list[EVResponse])
def get_all_evs(
    db: Session = Depends(get_db)
):
    return db.query(EV).all()


@router.get("/{ev_id}", response_model=EVResponse)
def get_ev(
    ev_id: int,
    db: Session = Depends(get_db)
):
    ev = db.query(EV).filter(EV.ev_id == ev_id).first()

    if not ev:
        raise HTTPException(
            status_code=404,
            detail="EV not found"
        )

    return ev