import pytest


@pytest.mark.asyncio
async def test_dashboard_report(client, admin_headers):
    response = await client.get(
        "/api/reports/dashboard",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_tender_report(client, admin_headers):
    response = await client.get(
        "/api/reports/tenders",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_evaluation_report(client, admin_headers):
    response = await client.get(
        "/api/reports/evaluations",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_sanction_report(client, admin_headers):
    response = await client.get(
        "/api/reports/sanctions",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_dashboard_without_token(client):
    response = await client.get("/api/reports/dashboard")

    assert response.status_code in [401, 403]


    