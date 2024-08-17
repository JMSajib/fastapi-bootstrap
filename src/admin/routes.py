from fastapi import Depends, HTTPException, APIRouter, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import session
from typing import Annotated
from starlette import status
from src.todo.models import Todos
from src.db.databases import SessionLocal
from src.auth.routes import get_current_user

admin_router = APIRouter(
    prefix="/admin",
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependancy = Annotated[session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]


@admin_router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependancy, db: db_dependancy):
    if not user or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

@admin_router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependancy, db:db_dependancy,todo_id: int = Path(gt=0)):
    if not user or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
