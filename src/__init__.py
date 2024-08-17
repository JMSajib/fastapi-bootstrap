from fastapi import FastAPI
from src.config import settings

from src.auth.routes import auth_router
from src.todo.routes import todo_router
from src.admin.routes import admin_router
from src.users.routes import user_router

app = FastAPI(
    title="Todo App",
    description="A REST API for Todo Application",
    version=settings.API_VERSION
)
# Base.metadata.create_all(bind=engine)

API_PREFIX = f"/api/{settings.API_VERSION}"

app.include_router(auth_router, prefix=f"{API_PREFIX}/auth", tags=['auth'])
app.include_router(todo_router, prefix=f"{API_PREFIX}/todo", tags=['todo'])
app.include_router(admin_router, prefix=f"{API_PREFIX}/admin", tags=['admin'])
app.include_router(user_router, prefix=f"{API_PREFIX}/user", tags=['users'])