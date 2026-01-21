def test_list_tasks_returns_200(client):
    create_response = client.post("/tasks", json={"title": "1つ目のToDoタスク"})

    assert create_response.status_code == 200

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "1つ目のToDoタスク",
            "done": False,
        }
    ]


def test_create_task_returns_200(client):
    response = client.post("/tasks", json={"title": "新しいタスク"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "新しいタスク"}


def test_update_task_returns_200(client):
    create_response = client.post("/tasks", json={"title": "更新前タスク"})

    assert create_response.status_code == 200

    response = client.put("/tasks/1", json={"title": "更新後タスク"})

    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "更新後タスク"}


def test_delete_task_returns_200(client):
    create_response = client.post("/tasks", json={"title": "削除対象タスク"})

    assert create_response.status_code == 200

    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json() is None


def test_mark_task_as_done_returns_200(client):
    create_response = client.post("/tasks", json={"title": "完了対象タスク"})

    assert create_response.status_code == 200

    response = client.put("/tasks/1/done")

    assert response.status_code == 200
    assert response.json() == {"id": 1}


def test_unmark_task_as_done_returns_200(client):
    create_response = client.post("/tasks", json={"title": "未完了戻し対象タスク"})

    assert create_response.status_code == 200

    mark_response = client.put("/tasks/1/done")

    assert mark_response.status_code == 200

    response = client.delete("/tasks/1/done")

    assert response.status_code == 200
    assert response.json() is None
