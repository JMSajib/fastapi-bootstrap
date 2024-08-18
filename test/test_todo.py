from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from fastapi import status

from src.auth.routes import get_current_user
from src.db.databases import Base, get_db
from src import app

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
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

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

clien = TestClient(app)

def test_read_all_authenticated():
    response = clien.get("/api/v1/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []
