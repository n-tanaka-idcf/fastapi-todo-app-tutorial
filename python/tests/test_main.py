def test_hello_returns_message(client):
    response = client.get("/hello")

    assert response.status_code == 200
    assert response.json() == {"message": "hello, world!"}


def test_hello_disallows_post(client):
    response = client.post("/hello")

    assert response.status_code == 405
