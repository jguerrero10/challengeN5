from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException, status, Depends

from database.crud import (
    add_object,
    delete_object,
    get_all_objects,
    get_object,
    update_object, search_objects,
)
from schemas.person_schemas import Person, PersonCreate, PersonUpdate
from schemas.user_schemas import TokenData
from utils.auth_utils import define_role
from utils.enums import Role
from utils.token_manage import get_current_user

person_router = APIRouter()


@person_router.get("/", response_model=List[Person])
async def get_persons(token_data: TokenData = Depends(get_current_user)) -> List[Any]:
    define_role(token_data, Role.ADMIN)
    return await get_all_objects("persons")


@person_router.get("/{person_id}", response_model=Person)
async def get_person(person_id: str, token_data: TokenData = Depends(get_current_user)) -> Any:
    define_role(token_data, Role.ADMIN)
    return await get_object("persons", person_id)


@person_router.post("/", response_model=Person)
async def create_person(person: PersonCreate, token_data: TokenData = Depends(get_current_user)) -> Any:
    define_role(token_data, Role.ADMIN)
    search_person = await search_objects("persons", "email", person.email)
    if search_person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Person with email {person.email} already exists"
        )
    return await add_object("persons", dict(person))


@person_router.patch("/{person_id}", response_model=Person)
async def update_person(person_id: str, person: PersonUpdate, token_data: TokenData = Depends(get_current_user)) -> Any:
    define_role(token_data, Role.ADMIN)
    return await update_object("persons", person_id, dict(person))


@person_router.delete("/{person_id}")
async def delete_person(person_id: str, token_data: TokenData = Depends(get_current_user)) -> Dict[str, str]:
    define_role(token_data, Role.ADMIN)
    person_deleted = await delete_object("persons", person_id)
    if person_deleted == 1:
        return {"message": "Person deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error deleting person")
