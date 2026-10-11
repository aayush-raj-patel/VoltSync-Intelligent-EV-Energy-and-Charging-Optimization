from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine

from app.models.user import User
from app.models.ev import EV
from app.models.station import ChargingStation
from app.models.charger import Charger
from app.models.charging_session import ChargingSession

from app.routers.ev import router as ev_router
from app.routers.station import router as station_router
from app.routers.charger import router as charger_router
from app.routers.charging_request import router as charging_request_router
from app.routers.charging_session import router as charging_session_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Intelligent EV Charging and Energy Resource Optimization System",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ev_router)
app.include_router(station_router)
app.include_router(charger_router)
app.include_router(charging_request_router)
app.include_router(charging_session_router)

@app.get("/")
def root():
    return {
        "message": "EV Charging Optimization System is running"
    }

