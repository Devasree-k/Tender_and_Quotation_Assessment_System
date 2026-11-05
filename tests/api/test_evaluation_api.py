import pytest


@pytest.mark.asyncio
async def test_get_all_evaluations(client, admin_headers):
    response = await client.get(
        "/api/evaluations/",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_evaluation_not_found(client, admin_headers):
    response = await client.get(
        "/api/evaluations/999999",
        headers=admin_headers
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_evaluations_without_token(client):
    response = await client.get("/api/evaluations/")

    assert response.status_code in [401, 403]


    