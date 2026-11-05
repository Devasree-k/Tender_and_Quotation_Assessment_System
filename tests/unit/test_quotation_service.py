
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.services.quotation_service import QuotationService

from app.core.exceptions.exception import (
    QuotationBusinessRuleException,
    QuotationNotFoundException,
    QuotationAccessDeniedException,
    TenderNotFoundException,
)


@pytest.fixture
def service(
    mock_quotation_repository,
    mock_tender_repository,
):

    return QuotationService(
        mock_quotation_repository,
        mock_tender_repository,
    )


@pytest.fixture
def fake_open_tender():

    class Tender:

        tender_id = 1
        status = "open"
        publish_date = date.today()
        end_date = date.today() + timedelta(days=10)

    return Tender()


# 1. VENDOR PROFILE NOT FOUND

@pytest.mark.asyncio
async def test_vendor_profile_not_found(
    service,
    mock_quotation_repository,
):

    mock_quotation_repository.get_vendor_id_by_user_id.return_value = None

    with pytest.raises(QuotationBusinessRuleException):

        await service.submit_quotation(
            tender_id=1,
            user_id=100,
            amount_quoted=Decimal("400000"),
            proposal="Test proposal for tender",
            document=None,
        )


# 2. TENDER NOT FOUND

@pytest.mark.asyncio
async def test_tender_not_found(
    service,
    mock_quotation_repository,
    mock_tender_repository,
):

    mock_quotation_repository.get_vendor_id_by_user_id.return_value = 5
    mock_tender_repository.get_by_tender_vendor.return_value = None

    mock_tender_repository.get_by_id.return_value = None

    with pytest.raises(TenderNotFoundException):

        await service.submit_quotation(
            tender_id=999,
            user_id=100,
            amount_quoted=Decimal("400000"),
            proposal="Test proposal for tender",
            document=None,
        )


# 3. TENDER NOT OPEN

@pytest.mark.asyncio
async def test_closed_tender_rejected(
    service,
    mock_quotation_repository,
    mock_tender_repository,
    fake_open_tender,
):

    fake_open_tender.status = "closed"

    mock_quotation_repository.get_vendor_id_by_user_id.return_value = 5
    mock_tender_repository.get_by_tender_vendor.return_value = None

    mock_tender_repository.get_by_id.return_value = fake_open_tender

    with pytest.raises(QuotationBusinessRuleException):

        await service.submit_quotation(
            tender_id=1,
            user_id=100,
            amount_quoted=Decimal("400000"),
            proposal="Test proposal for tender",
            document=None,
        )


# 4. DUPLICATE QUOTATION

@pytest.mark.asyncio
async def test_duplicate_quotation_rejected(
    service,
    mock_quotation_repository,
    mock_tender_repository,
    fake_open_tender,
):

    mock_quotation_repository.get_vendor_id_by_user_id.return_value = 5
    mock_tender_repository.get_by_tender_vendor.return_value = (
        object()
    )

    mock_tender_repository.get_by_id.return_value = fake_open_tender

    with pytest.raises(QuotationBusinessRuleException):

        await service.submit_quotation(
            tender_id=1,
            user_id=100,
            amount_quoted=Decimal("400000"),
            proposal="Test proposal for tender",
            document=None,
        )


# 5. GET QUOTATION NOT FOUND

@pytest.mark.asyncio
async def test_get_quotation_not_found(
    service,
    mock_quotation_repository,
):

    mock_quotation_repository.get_by_id.return_value = None

    with pytest.raises(QuotationNotFoundException):

        await service.get_quotation(
            quotation_id=999,
            user_id=100,
            role="admin",
        )


# 6. VENDOR CANNOT ACCESS ANOTHER VENDOR'S QUOTATION

@pytest.mark.asyncio
async def test_vendor_access_denied(
    service,
    mock_quotation_repository,
    fake_quotation,
):

    fake_quotation.vendor_id = 5

    mock_quotation_repository.get_by_id.return_value = fake_quotation
    mock_quotation_repository.get_vendor_id_by_user_id.return_value = 10

    with pytest.raises(QuotationAccessDeniedException):

        await service.get_quotation(
            quotation_id=1,
            user_id=100,
            role="vendor",
        )
    