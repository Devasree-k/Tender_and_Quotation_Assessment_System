
import pytest


# 1. SUBMIT QUOTATION

@pytest.mark.asyncio
async def test_submit_quotation(created_quotation):

    assert created_quotation["quotation_id"] > 0
    assert created_quotation["status"] == "submitted"


# 2. GET MY QUOTATIONS
@pytest.mark.asyncio
async def test_get_my_quotations(client, vendor_headers):
    response = await client.get("/api/quotations/my",headers=vendor_headers)
    assert response.status_code == 200


# 3. ADMIN GET ALL QUOTATIONS
@pytest.mark.asyncio
async def test_get_all_quotations(client, admin_headers):
    response = await client.get(
        "/api/quotations/",
        headers=admin_headers
    )
    assert response.status_code == 200


# 4. GET QUOTATION BY ID
@pytest.mark.asyncio
async def test_get_quotation(
    client,
    vendor_headers,
    created_quotation,
):
    quotation_id = created_quotation["quotation_id"]
    response = await client.get(
        f"/api/quotations/{quotation_id}",
        headers=vendor_headers,
    )
    assert response.status_code == 200


# 5. WITHDRAW QUOTATION

@pytest.mark.asyncio
async def test_withdraw_quotation(
    client,
    vendor_headers,
    created_quotation,
):
    quotation_id = created_quotation["quotation_id"]
    response = await client.patch(
        f"/api/quotations/{quotation_id}/withdraw",
        headers=vendor_headers,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "withdrawn"


# 6. INVALID QUOTATION ID
@pytest.mark.asyncio
async def test_get_quotation_not_found(client, admin_headers):
    response = await client.get(
        "/api/quotations/999999",
        headers=admin_headers
    )
    assert response.status_code == 404

    