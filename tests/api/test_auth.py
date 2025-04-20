import pytest

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.json["success"] is True
    assert "user" in response.json
    assert response.json["user"]["username"] == "newuser"

@pytest.mark.asyncio
async def test_register_duplicate_username(client):
    await client.post(
        "/api/auth/register",
        json={
            "username": "dupuser",
            "email": "dupuser@example.com",
            "password": "password123",
        },
    )
    response = await client.post(
        "/api/auth/register",
        json={
            "username": "dupuser",
            "email": "another@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert response.json["success"] is False
    assert "Username already exists" in response.json["message"]

@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "password123",
        },
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert "user" in response.json
    assert response.json["user"]["username"] == "loginuser"

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post(
        "/api/auth/register",
        json={
            "username": "wrongpass",
            "email": "wrongpass@example.com",
            "password": "password123",
        },
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json["success"] is False
    assert "Invalid credentials" in response.json["message"]

@pytest.mark.asyncio
async def test_change_password(client, auth_header):
    response = await client.post(
        "/api/auth/change-password",
        json={"old_password": "password123", "new_password": "newpassword123"},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json["success"] is True
    response = await client.post(
        "/api/auth/login", json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 401
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "newpassword123"},
    )
    assert response.status_code == 200
