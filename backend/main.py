from typing import Dict

from fastapi import FastAPI

from routes.auth_routes import auth_router
from routes.officer_routes import officer_router
from routes.person_routes import person_router
from routes.traffic_violations_routes import traffic_violations_router
from routes.vehicle_routes import vehicle_router

app = FastAPI()

app.title = "Challenger Dev Python Senior"
app.version = "0.0.1"

app.include_router(person_router, prefix="/person", tags=["Person"])
app.include_router(vehicle_router, prefix="/vehicle", tags=["Vehicle"])
app.include_router(officer_router, prefix="/officer", tags=["Officer"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(traffic_violations_router, prefix="/traffic-violations", tags=["Traffic Violations"])


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Backend - Challenger Dev Python Senior"}
