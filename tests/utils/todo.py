from datetime import timedelta
from typing import Any
from fastapi.testclient import TestClient
from sqlmodel import Session

from api.core.security import create_access_token
from api.db.mock_db import SessionTestDep
from api.db.modals import CreateTodo
from api.deps import CurrentUser, SessionDep
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string
from api.main import app




def create_random_todo(db: Session):
    app.dependency_overrides[SessionDep] = SessionTestDep
    test_user = create_random_user(db)
    
    assert test_user.id is not None
    mock_token = create_access_token(test_user.id, timedelta(minutes=30))
    app.dependency_overrides[CurrentUser] = lambda: test_user
    client = TestClient(app=app)
    title = random_lower_string()
    new_todo = CreateTodo(title=title )
    response:Any = client.post("/api/v1/todos/", json=new_todo, # type: ignore
                           headers={"Authorization": f"bearer {mock_token}"})
    print(response.json())
    assert response.status_code == 200
    app.dependency_overrides = {}



  