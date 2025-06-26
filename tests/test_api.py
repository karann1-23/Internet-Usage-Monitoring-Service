from fastapi.testclient import TestClient
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_top_users():
    response = client.get("/top-users")
    assert response.status_code == 200
    assert "users" in response.json()

def test_user_details():
    # Use a username and timestamp that exist in your data
    response = client.get("/user-details?name=gutturalTuna3&timestamp=2022-12-05%2000:00")
    assert response.status_code == 200
    assert "username" in response.json()