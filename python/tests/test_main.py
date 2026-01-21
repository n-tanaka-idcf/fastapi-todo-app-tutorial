def test_list_tasks_returns_200(client):
    response = client.get("/tasks")

    assert response.status_code == 200


def test_create_task_returns_200(client):
    response = client.post("/tasks")

    assert response.status_code == 200


def test_update_task_returns_200(client):
    response = client.put("/tasks/1")

    assert response.status_code == 200


def test_delete_task_returns_200(client):
    response = client.delete("/tasks/1")

    assert response.status_code == 200


def test_mark_task_as_done_returns_200(client):
    response = client.put("/tasks/1/done")

    assert response.status_code == 200


def test_unmark_task_as_done_returns_200(client):
    response = client.delete("/tasks/1/done")

    assert response.status_code == 200
