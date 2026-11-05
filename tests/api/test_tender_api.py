
import pytest


# 1. CREATE TENDER

@pytest.mark.asyncio
async def test_create_tender(
    client,
    admin_headers,
    sample_tender_data,
):

    response = await client.post(
        "/api/tenders/",
        headers=admin_headers,
        json=sample_tender_data,
    )

    assert response.status_code == 201
    assert response.json()["tender_title"] == "Test Road Maintenance"


# 2. LIST TENDERS

@pytest.mark.asyncio
async def test_list_tenders(
    client,
    admin_headers,
    created_tender,
):

    response = await client.get(
        "/api/tenders/",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


# 3. GET OPEN TENDERS

@pytest.mark.asyncio
async def test_get_open_tenders(
    client,
    admin_headers,
    created_tender,
):

    response = await client.get(
        "/api/tenders/open",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


# 4. GET TENDER BY ID

@pytest.mark.asyncio
async def test_get_tender(
    client,
    admin_headers,
    created_tender,
):

    tender_id = created_tender["tender_id"]

    response = await client.get(
        f"/api/tenders/{tender_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200


# 5. INVALID TENDER DATA

@pytest.mark.asyncio
async def test_create_tender_invalid_data(
    client,
    admin_headers,
):

    response = await client.post(
        "/api/tenders/",
        headers=admin_headers,
        json={},
    )

    assert response.status_code == 422


# 6. UNAUTHORIZED TENDER CREATION

@pytest.mark.asyncio
async def test_create_tender_without_token(
    client,
    sample_tender_data,
):

    response = await client.post(
        "/api/tenders/",
        json=sample_tender_data,
    )

    assert response.status_code in (401, 403)
