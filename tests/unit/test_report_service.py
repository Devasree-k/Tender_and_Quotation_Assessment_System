
from unittest.mock import AsyncMock

import pytest

from app.services.report_service import ReportService


@pytest.fixture
def service():

    repository = AsyncMock()

    return ReportService(repository)


# 1. DASHBOARD

@pytest.mark.asyncio
async def test_dashboard_report(service):

    service.repository.get_dashboard_report.return_value = {
        "total_tenders": 5,
        "total_quotations": 10,
    }

    result = await service.get_dashboard_report()

    assert result["total_tenders"] == 5
    assert result["total_quotations"] == 10


# 2. TENDER REPORT

@pytest.mark.asyncio
async def test_tender_report(service):

    service.repository.get_tender_report.return_value = [
        {"tender_id": 1, "quotation_count": 3}
    ]

    result = await service.get_tender_report(tender_id=1)

    assert len(result) == 1
    assert result[0]["tender_id"] == 1


# 3. EVALUATION REPORT

@pytest.mark.asyncio
async def test_evaluation_report(service):

    service.repository.get_evaluation_report.return_value = [
        {"decision": "approved", "count": 2}
    ]

    result = await service.get_evaluation_report(
        decision="approved"
    )

    assert result[0]["decision"] == "approved"


# 4. SANCTION REPORT

@pytest.mark.asyncio
async def test_sanction_report(service):

    service.repository.get_sanction_report.return_value = [
        {"tender_id": 1, "sanctioned_amount": 400000}
    ]

    result = await service.get_sanction_report(tender_id=1)

    assert result[0]["tender_id"] == 1
    assert result[0]["sanctioned_amount"] == 400000
