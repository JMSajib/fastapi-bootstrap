from src import app
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.db.databases import Base
from src.todo.models import Todos
import pytest

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class FakeUser:
    def __init__(self, username: str, user_id: int, user_role: str):
        self.username = username
        self.id = user_id
        self.user_role = user_role


def override_get_current_user():
    return FakeUser(username="sajib", user_id=1, user_role="admin")


clien = TestClient(app)


@pytest.fixture(scope='function')
def test_todo():
    todo = Todos(
        title='Learn to Code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1,
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()
