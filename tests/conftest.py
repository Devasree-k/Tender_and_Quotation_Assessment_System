import pytest
from httpx import ASGITransport, AsyncClient

from app.api.dependencies.database import get_db
from app.main import app


@pytest.fixture()
def test_db():
    raise NotImplementedError("Connect your existing test db fixture.")

@pytest.fixture()
async def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()



@pytest.fixture()
async def admin_token(client):

    response = await client.post(
        "/api/auth/login",
        data={
            "username": "your_test_admin_username",
            "password": "your_test_admin_password",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture()
async def admin_headers(admin_token):

    return {
        "Authorization": f"Bearer {admin_token}"
    }

