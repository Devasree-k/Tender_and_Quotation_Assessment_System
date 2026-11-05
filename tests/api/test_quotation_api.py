import pytest


@pytest.mark.asyncio
async def test_get_my_quotations(client, vendor_headers):
    response = await client.get(
        "/api/quotations/my",
        headers=vendor_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_quotations(client, admin_headers):
    response = await client.get(
        "/api/quotations/",
        headers=admin_headers
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_quotation_not_found(client, admin_headers):
    response = await client.get(
        "/api/quotations/999999",
        headers=admin_headers
    )

    assert response.status_code == 404

    