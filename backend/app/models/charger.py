from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Charger(Base):
    __tablename__ = "chargers"

    charger_id = Column(Integer, primary_key=True, index=True)

    station_id = Column(
        Integer,
        ForeignKey("charging_stations.station_id"),
        nullable=False
    )

    charger_type = Column(String(50), nullable=False)
    max_power = Column(Float, nullable=False)
    status = Column(String(20), default="AVAILABLE")