from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class ChargingStation(Base):
    __tablename__ = "charging_stations"

    station_id = Column(Integer, primary_key=True, index=True)
    station_name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=False)
    total_power_capacity = Column(Float, nullable=False)
    status = Column(String(20), default="ACTIVE")