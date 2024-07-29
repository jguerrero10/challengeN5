from fastapi import HTTPException, status

from database.crud import search_objects
from schemas.user_schemas import TokenData
from utils.enums import Role
from utils.hash_password_utils import verify_password


async def authenticate_user(username: str, password: str):
    user = await search_objects("users", "username", username)
    if not user:
        return False
    if not verify_password(password, user[0].get("hashed_password")):
        return False
    return user[0]


def define_role(token_data: TokenData, role: Role):
    if token_data.role != role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You do not have permissions to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return
