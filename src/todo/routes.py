from fastapi import Depends, Path, APIRouter
from typing import Annotated
from starlette import status
from src.auth.routes import get_current_user
from src.todo.schemas import TodoRequest
from src.todo.service import TodoService
from src.todo.dependencies import get_todo_service

todo_router = APIRouter()

# dependency
user_dependency = Annotated[dict, Depends(get_current_user)]
todo_service_dependency = Annotated[TodoService, Depends(get_todo_service)]


@todo_router.get("", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, todo_service: todo_service_dependency):
    return todo_service.get_all_todos(user.id)


@todo_router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    user: user_dependency,
    todo_service: todo_service_dependency,
    todo_id: int = Path(gt=0),
):
    return todo_service.get_todo_by_id(todo_id, user.id)


@todo_router.post("", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    todo_service: todo_service_dependency,
    todo_request: TodoRequest,
):
    todo_service.create_todo(todo_request, user.id)


@todo_router.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo(
    user: user_dependency,
    todo_service: todo_service_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0),
):
    return todo_service.update_todo(todo_id, todo_request, user.id)


@todo_router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: user_dependency,
    todo_service: todo_service_dependency,
    todo_id: int = Path(gt=0),
):
    todo_service.delete_todo_by_id(todo_id, user.id)
