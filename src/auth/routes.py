from datetime import datetime,timedelta,timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.db.databases import SessionLocal
from sqlalchemy.orm import session
from src.users.models import Users
from src.auth.schemas import UserRequest, Token
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

auth_router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependancy = Annotated[session, Depends(get_db)]

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

SECRET_KEY = '9ecc4622712c6baaa9ec196135885a5208a5598890c8c119853979efd6f74fa0'
ALGORITHM = 'HS256'


def authenticated_user(username:str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username:str, user_id:int, role: str, expires_delta: timedelta):
    encode = {
        'sub':username,
        'id':user_id,
        'role': role
    }
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized")
        return {"id": user_id, "username": username, "user_role": user_role}
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized")


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy,create_user_request: UserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username = create_user_request.username,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active=create_user_request.is_active
    )
    db.add(create_user_model)
    db.commit()
    return {"status": True, "message": "Successful"}

@auth_router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependancy):
    user = authenticated_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UnAuthorized")
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "Bearer"}