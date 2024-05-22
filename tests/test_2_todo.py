from typing import Dict
from fastapi.testclient import TestClient
import pytest
from api.db.db_connection import get_db
from api.db.mock_db import drop_test_tables, get_test_db
from api.deps import CurrentUser, get_current_test_user
from api.main import app


app.dependency_overrides[get_db] = get_test_db
app.dependency_overrides[CurrentUser] = get_current_test_user


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


@pytest.fixture(scope="module")
def test_user():
    return {"username": "test_email@test.com", "password": "test_user_password"}


@pytest.fixture(scope="module")
def token(client: TestClient, test_user: Dict[str, str]):
    response = client.post("/api/v1/access-token", data=test_user)
    assert response.status_code == 200
    token = response.json()["access_token"]
    print("xxxxxxxxxxxxxxxxxxxxx", token)
    assert token is not None
    return token


def test_create_todos(client: TestClient, token: str):
    print("xxxxxxxxxxxxxxxxxxxxx", token)
    response = client.post(
        "/api/v1/create_todo",
        json={"title": "Test todo", "completed": False},
        headers={"Authorization": f"bearer {token}"},
    )
    print("xxxxxxxxxxxxxxxxxxxxxxxxx", response)
    print(response.json())
    assert response.status_code == 200


def test_read_todos(client: TestClient, token: str):
    response = client.get("/api/v1/todos", headers={"Authorization": f"bearer {token}"})
    assert response.status_code == 200


def test_update_todos(client: TestClient, token: str):
    response = client.put(
        f"/api/v1/todos/{1}",
        params={"todo_id": 1},
        json={"title": "Test todo updated", "completed": True},
        headers={"Authorization": f"bearer {token}"},
    )
    print(response.json())

    assert response.status_code == 200
    app.dependency_overrides.clear()


def test_drop_tables():
    db_dropped = drop_test_tables()
    assert db_dropped == "Tables dropped.."
    print("xxxxxxxxxxxxxx ALL Tables Droped in DB ")
