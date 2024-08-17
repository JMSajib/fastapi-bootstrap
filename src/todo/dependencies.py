from sqlalchemy.orm import Session
from fastapi import Depends
from src.db.databases import get_db
from src.todo.service import TodoService


def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(db)
