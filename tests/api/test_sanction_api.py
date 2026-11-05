import pytest


@pytest.mark.asyncio
async def test_get_all_sanctions(client, admin_headers):
    response = await client.get(
        "/api/sanctions/",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_sanction_not_found(client, admin_headers):
    response = await client.get(
        "/api/sanctions/999999",
        headers=admin_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_sanctions_without_token(client):
    response = await client.get("/api/sanctions/")

    assert response.status_code in [401, 403]