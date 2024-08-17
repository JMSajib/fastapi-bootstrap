from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.todo.models import Todos


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_todos(self):
        return self.db.query(Todos).all()

    def delete_todo_by_id(self, todo_id: int):
        todo_model = self.db.query(Todos).filter(Todos.id == todo_id).first()
        if not todo_model:
            raise HTTPException(status_code=404, detail="Todo not found")
        self.db.query(Todos).filter(Todos.id == todo_id).delete()
        self.db.commit()
