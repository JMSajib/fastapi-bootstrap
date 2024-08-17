from fastapi import Depends, APIRouter
from typing import Annotated
from starlette import status
from passlib.context import CryptContext
from src.auth.routes import get_current_user
from src.users.service import UserService
from src.users.dependencies import get_user_service
from src.users.schemas import UserVerification

user_router = APIRouter()

user_service_dependency = Annotated[UserService, Depends(get_user_service)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@user_router.get("", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependancy, user_service: user_service_dependency):
    return user_service.get_users(user.id)


@user_router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    user: user_dependancy,
    user_service: user_service_dependency,
    password_verification: UserVerification,
):
    return user_service.change_password(user.id, password_verification, bcrypt_context)
