import json

import pytest

from backend import app as app_module
from backend import database
from backend.database import init_db


@pytest.fixture(autouse=True)
def setup_database(tmp_path, monkeypatch):
    temp_db = tmp_path / "test_data.db"
    monkeypatch.setattr(database, "DB_PATH", temp_db)
    init_db()
    return temp_db


def test_register_login_profile_endpoints():
    client = app_module.app.test_client()
    register_response = client.post(
        "/api/register",
        json={"name": "Test User", "email": "test@example.com", "password": "Password123"},
    )
    assert register_response.status_code == 201
    assert register_response.get_json()["success"] is True

    login_response = client.post(
        "/api/login",
        json={"email": "test@example.com", "password": "Password123"},
    )
    assert login_response.status_code == 200
    assert login_response.get_json()["success"] is True
    user = login_response.get_json()["user"]
    assert user["email"] == "test@example.com"

    profile_response = client.post(
        "/api/profile",
        json={
            "user_id": user["id"],
            "profile": {
                "age": 24,
                "gender": "Male",
                "height": 175,
                "weight": 70,
                "fitness_goal": "Maintenance",
                "activity_level": "Moderate",
                "budget": "Medium",
                "dietary_preference": "Balanced",
                "available_equipment": "Bodyweight",
                "health_conditions": "None",
            },
        },
    )
    assert profile_response.status_code == 200
    result = profile_response.get_json()
    assert result["success"] is True
    assert "recommendation" in result
