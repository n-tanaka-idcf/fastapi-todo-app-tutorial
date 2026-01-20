from api.main import app
from fastapi.testclient import TestClient


def test_hello_returns_message():
    client = TestClient(app)

    response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "hello, world!"}


def test_hello_disallows_post():
    client = TestClient(app)

    response = client.post("/hello")

    assert response.status_code == 405
