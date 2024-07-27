from typing import Dict

from fastapi import FastAPI

from routes.person_routes import person_router
from routes.vehicle_routes import vehicle_router

app = FastAPI()

app.title = "Challenger Dev Python Senior"
app.version = "0.0.1"

app.include_router(person_router, prefix="/person", tags=["Person"])
app.include_router(vehicle_router, prefix="/vehicle", tags=["Vehicle"])


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Challenger Dev Python Senior"}
