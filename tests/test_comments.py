
def register_and_login(client, username):
    response = client.post(
        "/users/register/",
        json={
            "username": username,
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.post(
        "/users/login/",
        data={
            "username": username,
            "password": "TestPassword123",
        },
    )
    assert response.status_code == 200

    return response.json()["access_token"], user_id


def create_project(client, token, name="Test Project"):
    return client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
            "description": "Project for comment tests",
        },
    )


def create_task(client, token, project_id, user_id):
    return client.post(
        f"/projects/{project_id}/tasks/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Task",
            "description": "Task for comment tests",
            "assigned_to": user_id,
            "status": "todo",
            "priority": "medium",
        },
    )


def create_comment(client, token, project_id, task_id, content="Test comment"):
    return client.post(
        f"/projects/{project_id}/tasks/{task_id}/comments/",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": content},
    )


def test_create_and_get_comments(client):
    token, user_id = register_and_login(client, "comment_creator")
    project_response = create_project(client, token)
    assert project_response.status_code == 200
    project_id = project_response.json()["id"]

    task_response = create_task(client, token, project_id, user_id)
    assert task_response.status_code == 200
    task_id = task_response.json()["id"]

    create_response = create_comment(
        client, token, project_id, task_id, "Hello WorkFlow"
    )
    assert create_response.status_code == 200
    assert create_response.json()["content"] == "Hello WorkFlow"
    assert create_response.json()["user_id"] == user_id

    list_response = client.get(
        f"/projects/{project_id}/tasks/{task_id}/comments/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["content"] == "Hello WorkFlow"


def test_create_comment_without_token(client):
    response = client.post(
        "/projects/1/tasks/1/comments/",
        json={"content": "Unauthorized comment"},
    )
    assert response.status_code == 401


def test_update_own_comment(client):
    token, user_id = register_and_login(client, "comment_editor")
    project_id = create_project(client, token).json()["id"]
    task_id = create_task(
        client, token, project_id, user_id
    ).json()["id"]

    comment_response = create_comment(
        client, token, project_id, task_id, "Original content"
    )
    assert comment_response.status_code == 200
    comment_id = comment_response.json()["id"]

    response = client.put(
        f"/projects/{project_id}/tasks/{task_id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": "Updated content"},
    )

    assert response.status_code == 200
    assert response.json()["content"] == "Updated content"



def test_cannot_update_another_users_comment(client):
    owner_token, owner_id = register_and_login(
        client, "comment_owner"
    )
    project_id = create_project(client, owner_token).json()["id"]
    task_id = create_task(
        client, owner_token, project_id, owner_id
    ).json()["id"]

    comment_response = create_comment(
        client, owner_token, project_id, task_id
    )
    assert comment_response.status_code == 200
    comment_id = comment_response.json()["id"]

    other_token, other_id = register_and_login(
        client, "comment_other_user"
    )

    # Add the other user to the project
    member_response = client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"user_id": other_id},
    )
    assert member_response.status_code == 200

    response = client.put(
        f"/projects/{project_id}/tasks/{task_id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {other_token}"},
        json={"content": "Trying to edit another user's comment"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only update your own comments"
    )



def test_delete_own_comment(client):
    token, user_id = register_and_login(client, "comment_deleter")
    project_id = create_project(client, token).json()["id"]
    task_id = create_task(
        client, token, project_id, user_id
    ).json()["id"]

    comment_response = create_comment(
        client, token, project_id, task_id
    )
    assert comment_response.status_code == 200
    comment_id = comment_response.json()["id"]

    response = client.delete(
        f"/projects/{project_id}/tasks/{task_id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Comment deleted successfully"



def test_cannot_delete_another_users_comment(client):
    owner_token, owner_id = register_and_login(
        client, "comment_delete_owner"
    )
    project_id = create_project(client, owner_token).json()["id"]
    task_id = create_task(
        client, owner_token, project_id, owner_id
    ).json()["id"]

    comment_response = create_comment(
        client, owner_token, project_id, task_id
    )
    assert comment_response.status_code == 200
    comment_id = comment_response.json()["id"]

    other_token, other_id = register_and_login(
        client, "comment_delete_other"
    )

    # Add the other user to the project
    member_response = client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"user_id": other_id},
    )
    assert member_response.status_code == 200

    response = client.delete(
        f"/projects/{project_id}/tasks/{task_id}/comments/{comment_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == (
        "You can only delete your own comments"
    )