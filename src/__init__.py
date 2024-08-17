from fastapi import FastAPI
from src.db.databases import Base, engine

from src.auth.routes import auth_router
from src.todo.routes import todo_router
from src.admin.routes import admin_router
from src.users.routes import user_router

app = FastAPI()

# Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(todo_router)
app.include_router(admin_router)
app.include_router(user_router)