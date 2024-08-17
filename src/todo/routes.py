from fastapi import Depends, HTTPException, Path, APIRouter
from sqlalchemy.orm import session
from typing import Annotated
from starlette import status
from src.todo.models import Todos
from src.db.databases import get_db
from src.auth.routes import get_current_user
from src.todo.schemas import TodoRequest

todo_router = APIRouter()

# dependancy
db_dependancy = Annotated[session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(get_current_user)]


@todo_router.get("", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependancy,db: db_dependancy):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@todo_router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependancy,db:db_dependancy, todo_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@todo_router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependancy,db: db_dependancy, todo_request: TodoRequest):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()
    return {"message": "Successful", "data": todo_request}


@todo_router.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependancy,db: db_dependancy, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@todo_router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependancy, db:db_dependancy,todo_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()