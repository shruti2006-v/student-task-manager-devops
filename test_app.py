import app as task_app


def setup_function():
    task_app.tasks[:] = [
        {"id": 1, "title": "Sample task", "done": False},
        {"id": 2, "title": "Completed task", "done": True},
    ]
    task_app.next_id = 3


def test_home_page_displays_tasks():
    client = task_app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Task Manager" in response.data
    assert b"Sample task" in response.data


def test_add_task():
    client = task_app.app.test_client()
    response = client.post("/add", data={"title": "Study Docker"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Study Docker" in response.data


def test_blank_task_is_not_added():
    client = task_app.app.test_client()
    client.post("/add", data={"title": "   "}, follow_redirects=True)
    assert len(task_app.tasks) == 2


def test_toggle_task():
    client = task_app.app.test_client()
    client.post("/toggle/1")
    assert task_app.tasks[0]["done"] is True


def test_delete_task():
    client = task_app.app.test_client()
    client.post("/delete/1")
    assert all(task["id"] != 1 for task in task_app.tasks)


def test_health_endpoint():
    response = task_app.app.test_client().get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
