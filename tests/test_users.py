
def test_register_user(client):
    response = client.post(
        "/users/register/",
        json={
            "username": "pytest_user_001",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "pytest_user_001"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert "password" not in data


def test_login_user(client):
    register_response = client.post(
        "/users/register/",
        json={
            "username": "pytest_login_user",
            "first_name": "Test",
            "last_name": "Login",
            "password": "TestPassword123",
        },
    )

    assert register_response.status_code == 200

    login_response = client.post(
        "/users/login/",
        data={
            "username": "pytest_login_user",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    
def test_register_duplicate_username(client):
    user_data = {
        "username": "duplicate_user",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPassword123",
    }

    first_response = client.post(
        "/users/register/",
        json=user_data,
    )
    assert first_response.status_code == 200

    second_response = client.post(
        "/users/register/",
        json=user_data,
    )
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Username already exists"


def test_login_invalid_credentials(client):
    response = client.post(
        "/users/login/",
        data={
            "username": "unknown_user",
            "password": "WrongPassword123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"
    

    
def test_get_current_user(client):
    # Register a user
    client.post(
        "/users/register/",
        json={
            "username": "pytest_me_user",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123",
        },
    )

    # Log in and get the token
    login_response = client.post(
        "/users/login/",
        data={
            "username": "pytest_me_user",
            "password": "TestPassword123",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Request the current user's profile
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "pytest_me_user"
    assert "password" not in data
    
def test_get_current_user_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401

def test_get_projects_without_token(client):
    response = client.get("/projects/")
    assert response.status_code == 401
    
def test_get_projects_with_token(client):
    client.post(
        "/users/register/",
        json={
            "username": "pytest_project_user",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123",
        },
    )

    login_response = client.post(
        "/users/login/",
        data={
            "username": "pytest_project_user",
            "password": "TestPassword123",
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/projects/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

