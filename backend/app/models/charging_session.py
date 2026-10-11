from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from datetime import datetime
from app.database import Base


class ChargingSession(Base):
    __tablename__ = "charging_sessions"

    session_id = Column(Integer, primary_key=True, index=True)

    request_id = Column(
        Integer,
        ForeignKey("charging_requests.request_id"),
        nullable=False
    )

    ev_id = Column(
        Integer,
        ForeignKey("evs.ev_id"),
        nullable=False
    )

    charger_id = Column(
        Integer,
        ForeignKey("chargers.charger_id"),
        nullable=False
    )

    station_id = Column(
        Integer,
        ForeignKey("charging_stations.station_id"),
        nullable=False
    )

    start_time = Column(DateTime, default=datetime.utcnow)

    end_time = Column(DateTime, nullable=True)

    energy_delivered = Column(Float, default=0)

    power_allocated = Column(Float, nullable=False)

    status = Column(String(30), default="ACTIVE")