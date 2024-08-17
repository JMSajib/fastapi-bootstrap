from fastapi import Depends, HTTPException, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import session
from typing import Annotated
from starlette import status
from src.users.models import Users
from src.db.databases import get_db
from passlib.context import CryptContext
from src.auth.routes import get_current_user

user_router = APIRouter()

db_dependancy = Annotated[session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@user_router.get("", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependancy, db: db_dependancy):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@user_router.put("/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    user: user_dependancy, db: db_dependancy, password_verification: UserVerification
):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(
        password_verification.password, user_model.hashed_password
    ):
        raise HTTPException(status_code=401, detail='Password can not be changed')
    user_model.hashed_password = bcrypt_context.hash(password_verification.new_password)
    db.add(user_model)
    db.commit()
    return {"status": True, "message": "Success"}
