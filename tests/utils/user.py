
from fastapi.testclient import TestClient
from api.settings import API_V1_STR
from typing import Dict

def user_authentication_headers(client: TestClient, email: str, password: str) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{API_V1_STR}/access-token", data=data)
    print('xxxxxxxxxxxxxxxxxxxxxxxxx',r.json())
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
