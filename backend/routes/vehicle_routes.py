from typing import List

from fastapi import APIRouter, Query, HTTPException, status, Depends
from pydantic import EmailStr

from database.crud import search_objects, update_object
from schemas.person_schemas import Person
from schemas.user_schemas import TokenData
from schemas.vehicle_schemas import Vehicle
from utils.auth_utils import is_admin
from utils.token_manage import get_current_user

vehicle_router = APIRouter()


@vehicle_router.get("/", response_model=List[Vehicle])
async def get_vehicles_by_person(
        person_email: EmailStr = Query(
            ...,
            example="example@mail.com",
            title="Person Email", description="Person Email"
        ),
        token_data: TokenData = Depends(get_current_user)
):
    is_admin(token_data)
    person_search = await search_objects("persons", "email", person_email)
    if not person_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    person = person_search[0]

    return person.get("vehicles", [])


@vehicle_router.get("/{patent_plate}", response_model=Vehicle)
async def get_vehicle(
        patent_plate: str,
        person_email: EmailStr = Query(..., title="Person Email", description="Person Email"),
        token_data: TokenData = Depends(get_current_user)
):
    is_admin(token_data)
    person_search = await search_objects("persons", "email", person_email)
    if not person_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    person = Person(**person_search[0])

    for vehicle in person.vehicles:
        if vehicle.patent_plate == patent_plate:
            return vehicle

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vehicle not found",
    )


@vehicle_router.post("/", response_model=Vehicle)
async def create_vehicle(
        vehicle: Vehicle,
        person_email: EmailStr = Query(..., title="Person Email", description="Person Email"),
        token_data: TokenData = Depends(get_current_user)
):
    is_admin(token_data)
    person_search = await search_objects("persons", "email", person_email)
    if not person_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    person = Person(**person_search[0])

    for v in person.vehicles:
        if v.patent_plate == vehicle.patent_plate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vehicle with patent plate {vehicle.patent_plate} already exists.",
            )

    vehicles = person.vehicles
    vehicles.append(vehicle)
    vehicles_dict = [dict(vehicle) for vehicle in vehicles]
    person_dict = dict(person)
    person_dict["vehicles"] = vehicles_dict
    await update_object("persons", person.id, person_dict)
    return vehicle


@vehicle_router.put("/{patent_plate}", response_model=Vehicle)
async def update_vehicle(
        patent_plate: str,
        updated_vehicle: Vehicle,
        person_email: EmailStr = Query(..., title="Person Email", description="Person Email"),
        token_data: TokenData = Depends(get_current_user)
):
    is_admin(token_data)
    person_search = await search_objects("persons", "email", person_email)
    if not person_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    person = Person(**person_search[0])

    for idx, vehicle in enumerate(person.vehicles):
        if vehicle.patent_plate == patent_plate:
            person.vehicles[idx] = updated_vehicle
            await update_object("persons", person.id, person.dict())
            return updated_vehicle

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vehicle not found",
    )


@vehicle_router.delete("/{patent_plate}", response_model=dict)
async def delete_vehicle(
        patent_plate: str,
        person_email: EmailStr = Query(..., title="Person Email", description="Person Email"),
        token_data: TokenData = Depends(get_current_user)
):
    is_admin(token_data)
    person_search = await search_objects("persons", "email", person_email)
    if not person_search:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )
    person = Person(**person_search[0])

    for vehicle in person.vehicles:
        if vehicle.patent_plate == patent_plate:
            person.vehicles.remove(vehicle)
            await update_object("persons", person.id, person.dict())
            return {"detail": "Vehicle deleted"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Vehicle not found",
    )
