from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.todo.models import Todos
from src.todo.schemas import TodoRequest


class TodoService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_todos(self, user_id: int):
        return self.db.query(Todos).filter(Todos.owner_id == user_id).all()

    def get_todo_by_id(self, todo_id: int, user_id: int):
        todo = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == user_id)
            .first()
        )
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

    def create_todo(self, todo_request: TodoRequest, user_id: int):
        todo_model = Todos(**todo_request.model_dump(), owner_id=user_id)
        self.db.add(todo_model)
        self.db.commit()
        return todo_model

    def update_todo(self, todo_id: int, todo_request: TodoRequest, user_id: int):
        todo_model = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == user_id)
            .first()
        )
        if not todo_model:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_model.title = todo_request.title
        todo_model.description = todo_request.description
        todo_model.priority = todo_request.priority
        todo_model.complete = todo_request.complete
        self.db.add(todo_model)
        self.db.commit()
        return todo_model

    def delete_todo_by_id(self, todo_id: int, user_id: int):
        todo_model = (
            self.db.query(Todos)
            .filter(Todos.id == todo_id)
            .filter(Todos.owner_id == user_id)
            .first()
        )
        if not todo_model:
            raise HTTPException(status_code=404, detail="Todo not found")
        self.db.query(Todos).filter(Todos.id == todo_id).filter(
            Todos.owner_id == user_id
        ).delete()
        self.db.commit()
        return {"detail": "Todo deleted"}
