from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime

from app.database import Base

class ChargingRequest(Base):
    __tablename__ = "charging_requests"

    request_id = Column(Integer, primary_key=True, index=True)

    ev_id = Column(
        Integer,
        ForeignKey("evs.ev_id"),
        nullable=False
    )

    station_id = Column(
        Integer,
        ForeignKey("charging_stations.station_id"),
        nullable=False
    )

    required_energy = Column(
        Float,
        nullable=False
    )

    requested_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    expected_departure_time = Column(
        DateTime,
        nullable=False
    )

    priority_score = Column(
        Float,
        default=0
    )
    
    status = Column(
        String(30),
        default="WAITING"
    )