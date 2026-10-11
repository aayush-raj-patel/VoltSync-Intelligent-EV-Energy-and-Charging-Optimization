from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class EV(Base):
    __tablename__ = "evs"

    ev_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False
    )

    model = Column(String(100), nullable=False)

    license_plate = Column(
        String(20),
        unique=True,
        nullable=False
    )

    battery_capacity = Column(
        Float,
        nullable=False
    )

    current_battery_level = Column(
        Float,
        nullable=False
    )

    charging_type = Column(
        String(50),
        nullable=False
    )

    vehicle_priority = Column(
        Integer,
        default=1
    )