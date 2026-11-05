
import pytest


# 1. TENDER AND QUOTATION WORKFLOW

@pytest.mark.asyncio
async def test_tender_quotation_workflow(
    created_tender,
    created_quotation,
):

    assert created_tender["tender_id"] > 0

    assert (
        created_quotation["tender_id"]
        == created_tender["tender_id"]
    )

    assert created_quotation["status"] == "submitted"


# 2. QUOTATION AND EVALUATION WORKFLOW

@pytest.mark.asyncio
async def test_quotation_evaluation_workflow(
    created_quotation,
    created_evaluation,
):

    assert created_quotation["quotation_id"] > 0

    assert (
        created_evaluation["decision"]
        == "approved"
    )

    assert created_evaluation["total_score"] == 87


# 3. EVALUATION, SANCTION AND REPORT WORKFLOW

@pytest.mark.asyncio
async def test_evaluation_sanction_report_workflow(
    client,
    admin_headers,
    created_evaluation,
    created_sanction,
):

    assert created_evaluation["decision"] == "approved"

    assert created_sanction["sanction_id"] > 0

    response = await client.get(
        "/api/reports/sanctions",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) >= 1


