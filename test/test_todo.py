from fastapi import status
from src.auth.routes import get_current_user
from src.db.databases import get_db

from src import app
from test.utils import clien, test_todo, override_get_current_user, override_get_db, TestingSessionLocal
from src.todo.models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = clien.get("/api/v1/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []


def test_read_one_authenticated(test_todo):
    response = clien.get("/api/v1/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []


def test_read_one_not_found_authenticated(test_todo):
    response = clien.get("/api/v1/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    response_data = response.json()
    assert response_data.get('detail') == "Todo not found"


def test_create_tod(test_todo):
    request_data = {
        'title': "New Todo",
        'description': 'new Description Todo',
        'priority': 3,
        'complete': False,
        'owner_id': 1,
    }
    response = clien.post('/api/v1/todo', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')


def test_update_todo(test_todo):
    request_data = {
        'title': 'Change Title',
        'description': 'Change Description',
        'priority': 5,
        'complete': False,
    }

    response = clien.put('/api/v1/todo/1', json=request_data)
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')


def test_delete_todo(test_todo):
    response = clien.delete('/api/v1/todo/1')
    assert response.status_code == status.HTTP_200_OK
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_not_found_todo(test_todo):
    response = clien.delete('/api/v1/todo/100')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get('detail') == 'Todo not found'
