from typing import List

from fastapi import APIRouter, HTTPException, status, Depends

from database.crud import get_all_objects, search_objects, add_object, update_object, delete_object
from schemas.officer_schemas import Officer, OfficerCreate, OfficerUpdate
from schemas.user_schemas import TokenData
from utils.auth_utils import define_role
from utils.enums import Role
from utils.hash_password_utils import get_password_hash
from utils.token_manage import get_current_user

officer_router = APIRouter()


@officer_router.get("/", response_model=List[Officer])
async def get_officers(token_data: TokenData = Depends(get_current_user)):
    define_role(token_data, Role.ADMIN)
    return await get_all_objects("officers")


@officer_router.get("/{number_identifier}", response_model=Officer)
async def get_officer(number_identifier: str, token_data: TokenData = Depends(get_current_user)):
    define_role(token_data, Role.ADMIN)
    search_officer = await search_objects(
        "officers",
        "number_identifier",
        number_identifier,
    )
    if not search_officer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")

    return search_officer[0]


@officer_router.post("/", response_model=Officer, status_code=status.HTTP_201_CREATED)
async def create_officer(officer: OfficerCreate, token_data: TokenData = Depends(get_current_user)):
    define_role(token_data, Role.ADMIN)
    search_person = await search_objects(
        "officers",
        "number_identifier",
        officer.number_identifier
    )
    search_user = await search_objects("users", "username", officer.username)
    if search_person or search_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Officer or user already exists"
        )
    officer_added = await add_object("officers", dict(officer))
    await add_object(
        "users",
        {
            "username": officer.username,
            "hashed_password": get_password_hash(officer.password),
            "role": Role.OFFICER
        }
    )
    return officer_added


@officer_router.patch("/{number_identifier}", response_model=Officer)
async def update_officer(
        number_identifier: str,
        officer: OfficerUpdate,
        token_data: TokenData = Depends(get_current_user)
):
    define_role(token_data, Role.ADMIN)
    search_officer = await search_objects(
        "officers",
        "number_identifier",
        number_identifier,
    )
    if not search_officer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")

    officer_obj = Officer(**search_officer[0])

    return await update_object("officers", officer_obj.id, dict(officer))


@officer_router.delete("/{number_identifier}")
async def delete_officer(number_identifier: str, token_data: TokenData = Depends(get_current_user)):
    define_role(token_data, Role.ADMIN)
    search_officer = await search_objects(
        "officers",
        "number_identifier",
        number_identifier,
    )
    if not search_officer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Officer not found")

    officer = Officer(**search_officer[0])
    officer_deleted = await delete_object("officers", officer.id)
    if officer_deleted == 1:
        return {"message": "Officer deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error deleting person")
