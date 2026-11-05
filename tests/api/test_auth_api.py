
import pytest


# 1. REGISTER VENDOR

@pytest.mark.asyncio
async def test_register_vendor(
    client,
    vendor_registration_data,
):

    response = await client.post(
        "/api/auth/register",
        json=vendor_registration_data,
    )

    assert response.status_code == 201


# 2. DUPLICATE REGISTRATION

@pytest.mark.asyncio
async def test_duplicate_vendor_registration(
    client,
    vendor_registration_data,
):

    await client.post(
        "/api/auth/register",
        json=vendor_registration_data,
    )

    response = await client.post(
        "/api/auth/register",
        json=vendor_registration_data,
    )

    assert response.status_code in (400, 409)


# 3. ADMIN LOGIN

@pytest.mark.asyncio
async def test_admin_login(
    client,
    admin_credentials,
):

    response = await client.post(
        "/api/auth/login",
        data=admin_credentials,
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


# 4. INVALID LOGIN

@pytest.mark.asyncio
async def test_invalid_login(client):

    response = await client.post(
        "/api/auth/login",
        data={
            "username": "wronguser",
            "password": "wrongpassword",
        },
    )

    assert response.status_code in (400, 401)


# 5. GET CURRENT PROFILE

@pytest.mark.asyncio
async def test_get_current_profile(
    client,
    admin_headers,
):

    response = await client.get(
        "/api/auth/me",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


# 6. REFRESH TOKEN

@pytest.mark.asyncio
async def test_refresh_token(
    client,
    admin_credentials,
):

    login = await client.post(
        "/api/auth/login",
        data=admin_credentials,
    )

    refresh_token = login.json()["refresh_token"]

    response = await client.post(
        "/api/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
