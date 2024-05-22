from fastapi.testclient import TestClient
import pytest
from api.db.db_connection import get_db
from api.db.mock_db import create_test_tables, get_test_db
from api.db.modals import CreateUser
from api.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app=app)


def test_create_db():
    test_db_created = create_test_tables()
    assert test_db_created == "Tables created.."
    print("xxxxxxxxxxxxxx New Tables Created in DB ")


def test_create_user(client: TestClient) -> None:
    app.dependency_overrides[get_db] = get_test_db

    email = "test_email@test.com"
    username = "test_username"
    password = "test_user_password"
    user_in = CreateUser(username=username, email=email, password=password)

    response = client.post(
        "/api/v1/create_user",
        json={
            "username": user_in.username,
            "email": user_in.email,
            "password": user_in.password,
        },
    )
    print(response.json())
    # app.dependency_overrides.clear()
    data = response.json()
    print("xxxxxxx User Created xxxxxxxx", data)

    assert response.status_code == 200
    assert data["password"] != password


# def test_create_random_todo():
#     try:
#         app.dependency_overrides[SessionDep] = SessionTestDep
#         test_user = create_random_user()

#         assert test_user.id is not None
#         mock_token = create_access_token(test_user.id, timedelta(minutes=30))
#         app.dependency_overrides[CurrentUser] = lambda:test_user
#         client = TestClient(app=app)
#         title = random_lower_string()
#         new_todo = CreateTodo(title=title).model_dump_json()
#         response = client.post("/api/v1/create_todo", json=new_todo,
#                                headers={"Authorization": f"bearer {mock_token}"})
#         print('xxxxxxxxxxxxxxxxxxxxxx',response.json())
#         assert response.status_code == 200
#         assert response.json()["title"] == title  # Example assertion, adjust as needed

#     finally:
#         app.dependency_overrides = {}
