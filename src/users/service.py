from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.users.models import Users
from src.users.schemas import UserVerification


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self, user_id: int):
        return self.db.query(Users).filter(Users.id == user_id).first()

    def change_password(
        self, user_id: int, password_verification: UserVerification, bcrypt_context
    ):
        user_model = self.db.query(Users).filter(Users.id == user_id).first()
        if not bcrypt_context.verify(
            password_verification.password, user_model.hashed_password
        ):
            raise HTTPException(status_code=401, detail='Password can not be changed')
        user_model.hashed_password = bcrypt_context.hash(
            password_verification.new_password
        )
        self.db.add(user_model)
        self.db.commit()
        return {"status": True, "message": "Success"}
