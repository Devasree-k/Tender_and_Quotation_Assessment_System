import pytest

#GET ALL EVALUATIONS
@pytest.mark.asyncio
async def test_get_all_evaluations(client, admin_headers):
    response = await client.get(
        "/api/evaluations/",
        headers=admin_headers
    )

    assert response.status_code == 200


#GET EVALUATION BY ID
@pytest.mark.asyncio
async def test_get_evaluation(
    client,
    admin_headers,
    created_evaluation,
):

    evaluation_id = created_evaluation["evaluation_id"]
    response = await client.get(
        f"/api/evaluations/{evaluation_id}",
        headers=admin_headers,
    )

    assert response.status_code == 200


#GET EVALUATION BY QUOTATION ID

@pytest.mark.asyncio
async def test_get_evaluation_by_quotation(
    client,
    admin_headers,
    created_evaluation,
    created_quotation,
):
    quotation_id = created_quotation["quotation_id"]
    response = await client.get(
        f"/api/evaluations/quotation/{quotation_id}",
        headers=admin_headers,
    )
    assert response.status_code == 200


# EVALUATION NOT FOUND

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


    