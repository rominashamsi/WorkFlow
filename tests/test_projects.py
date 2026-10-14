
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

    login_response = client.post(
        "/users/login/",
        data={
            "username": username,
            "password": "TestPassword123",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    return token


def create_project(client, token, name="Test Project"):
    return client.post(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name,
            "description": "Project created during testing",
        },
    )


def test_create_project(client):
    token = register_and_login(client, "project_creator")
    response = create_project(client, token)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"
    assert data["description"] == "Project created during testing"
    assert "id" in data
    assert "created_by" in data


def test_create_project_without_token(client):
    response = client.post(
        "/projects/",
        json={
            "name": "Unauthorized Project",
            "description": "Should not be created",
        },
    )

    assert response.status_code == 401


def test_create_duplicate_project(client):
    token = register_and_login(client, "duplicate_project_user")

    first_response = create_project(client, token, "My Project")
    assert first_response.status_code == 200

    second_response = create_project(client, token, "My Project")
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == (
        "You already have a project with this name"
    )


def test_get_nonexistent_project(client):
    token = register_and_login(client, "project_reader")

    response = client.get(
        "/projects/9999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_non_creator_cannot_update_project(client):
    creator_token = register_and_login(client, "project_owner")
    project_response = create_project(
        client, creator_token, "Owner Project"
    )
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]
    other_token = register_and_login(client, "other_project_user")

    response = client.put(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {other_token}"},
        json={"name": "Changed Project"},
    )

    assert response.status_code == 403


def test_non_creator_cannot_delete_project(client):
    creator_token = register_and_login(client, "delete_project_owner")
    project_response = create_project(
        client, creator_token, "Protected Project"
    )
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]
    other_token = register_and_login(client, "delete_project_other")

    response = client.delete(
        f"/projects/{project_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 403


def test_project_creator_can_add_member(client):
    creator_token = register_and_login(client, "member_project_owner")
    project_response = create_project(
        client, creator_token, "Team Project"
    )
    assert project_response.status_code == 200

    project_id = project_response.json()["id"]

    member_response = client.post(
        "/users/register/",
        json={
            "username": "new_project_member",
            "first_name": "New",
            "last_name": "Member",
            "password": "TestPassword123",
        },
    )
    assert member_response.status_code == 200
    member_id = member_response.json()["id"]

    response = client.post(
        f"/projects/{project_id}/members",
        headers={"Authorization": f"Bearer {creator_token}"},
        json={"user_id": member_id},
    )

    assert response.status_code == 200
    assert response.json()["project_id"] == project_id
    assert response.json()["user_id"] == member_id
