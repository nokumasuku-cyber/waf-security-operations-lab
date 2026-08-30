from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "WAF Security Operations Lab is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_search():
    response = client.get("/api/search?q=network security")

    assert response.status_code == 200
    assert response.json()["query"] == "network security"


def test_profile():
    response = client.get("/api/profile/noku")

    assert response.status_code == 200
    assert response.json()["username"] == "noku"


def test_login():
    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"