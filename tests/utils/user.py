
from fastapi.testclient import TestClient
from api.config import API_V1_STR
from typing import Dict

from api.db.mock_db import SessionTestDep
from api.db.modals import CreateUser, Users
from api.router.user import create_user
from tests.utils.utils import random_email, random_lower_string




def user_authentication_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{API_V1_STR}/login/access-token", data=data) # type: ignore
    response = r.json() # type: ignore
    auth_token = response["access_token"] # type: ignore
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def create_random_user(db: SessionTestDep) -> Users:
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()
    user_in = CreateUser(username=username,email=email, password=password)
    user = create_user(session=db, user=user_in)
    return user
