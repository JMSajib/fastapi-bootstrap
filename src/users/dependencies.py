from sqlalchemy.orm import Session
from fastapi import Depends
from src.db.databases import get_db
from src.users.service import UserService


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)
