
def register_and_login(client, username):
    register_response = client.post(
        "/users/register/",
        json={
            "username": username,
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123",
        },
    )
    assert register_response.status_code == 200

    user_id = register_response.json()["id"]

    login_response = client.post(
        "/users/login/",
        data={
            "username": username,
            "password": "TestPassword123",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return token, user_id


def create_project(client, token, name="Test Project"):
    return client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
            "description": "Project for task tests",
        },
    )


def create_task(client, token, project_id, assigned_to, title="Test Task"):
    return client.post(
        f"/projects/{project_id}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": title,
            "description": "Task created during testing",
            "assigned_to": assigned_to,
            "status": "todo",
            "priority": "medium",
        },
    )


def test_create_task(client):
    token, user_id = register_and_login(client, "task_creator")
    project_response = create_project(client, token)
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]
    response = create_task(client, token, project_id, user_id)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["project_id"] == project_id
    assert data["assigned_to"] == user_id
    assert data["created_by"] == user_id


def test_get_tasks(client):
    token, user_id = register_and_login(client, "task_list_user")
    project_response = create_project(client, token)
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]
    task_response = create_task(client, token, project_id, user_id)
    assert task_response.status_code == 200

    response = client.get(
        f"/projects/{project_id}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Task"


def test_get_nonexistent_task(client):
    token, _ = register_and_login(client, "task_reader")
    project_response = create_project(client, token)
    project_id = project_response.json()["id"]

    response = client.get(
        f"/projects/{project_id}/tasks/9999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_create_task_without_token(client):
    response = client.post(
        "/projects/1/tasks/",
        json={
            "title": "Unauthorized Task",
            "assigned_to": 1,
        },
    )

    assert response.status_code == 401


def test_non_creator_cannot_update_task(client):
    creator_token, creator_id = register_and_login(
        client, "task_owner"
    )
    project_response = create_project(client, creator_token)
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]
    task_response = create_task(
        client, creator_token, project_id, creator_id,
        title="Protected Task",
    )
    assert task_response.status_code == 200

    task_id = task_response.json()["id"]
    other_token, _ = register_and_login(client, "task_other_user")

    response = client.put(
        f"/projects/{project_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {other_token}"},
        json={"title": "Changed Task"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this project"
    )


def test_non_creator_cannot_delete_task(client):
    creator_token, creator_id = register_and_login(
        client, "task_delete_owner"
    )
    project_response = create_project(client, creator_token)
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]
    task_response = create_task(
        client, creator_token, project_id, creator_id,
        title="Protected Task",
    )
    assert task_response.status_code == 200

    task_id = task_response.json()["id"]
    other_token, _ = register_and_login(
        client, "task_delete_other"
    )

    response = client.delete(
        f"/projects/{project_id}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You do not have access to this project"
    )


def test_create_task_with_nonexistent_assignee(client):
    token, _ = register_and_login(
        client, "task_missing_assignee"
    )
    project_response = create_project(client, token)
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    response = create_task(
        client, token, project_id, 9999,
        title="Invalid Assignee Task",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Assigned user not found"


def test_create_task_for_non_member(client):
    token, _ = register_and_login(
        client, "task_membership_owner"
    )
    project_response = create_project(client, token)
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    _, non_member_id = register_and_login(
        client, "task_non_member"
    )

    response = create_task(
        client, token, project_id, non_member_id,
        title="Non Member Task",
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Assigned user is not a member of this project"
    )
