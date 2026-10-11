from fastapi import FastAPI
from sqlalchemy import text
from database import engine


app = FastAPI(title="EV Charging Optimizer")


@app.get("/")
def root():
    return {
        "message": "EV Charging Optimizer Backend is running"
    }


@app.get("/test-db")
def test_database():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database": "connected",
            "result": result.scalar()
        }