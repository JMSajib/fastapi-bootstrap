from fastapi import Depends, APIRouter, Path
from sqlalchemy.orm import session
from typing import Annotated
from starlette import status
from src.db.databases import get_db
from src.admin.service import AdminService
from src.auth.dependencies import is_admin

admin_router = APIRouter()

# Dependencies
db_dependency = Annotated[session, Depends(get_db)]
admin_dependency = Annotated[dict, Depends(is_admin)]


def get_admin_service(db: session = Depends(get_db)) -> AdminService:
    return AdminService(db)


# Routes
@admin_router.get("/todo", status_code=status.HTTP_200_OK)
async def read_all(
    user: admin_dependency,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
):
    return admin_service.get_all_todos()


@admin_router.delete("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    user: admin_dependency,
    admin_service: Annotated[AdminService, Depends(get_admin_service)],
    todo_id: int = Path(gt=0),
):
    return admin_service.delete_todo_by_id(todo_id)
