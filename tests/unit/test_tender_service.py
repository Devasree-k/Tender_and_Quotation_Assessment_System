
import pytest
from datetime import date, timedelta

from app.services.tender_service import TenderService

from app.core.exceptions.exception import (
    InvalidTenderStatusException,
    TenderBusinessRuleException,
    TenderNotFoundException,
)


@pytest.fixture
def tender_service(mock_tender_repository):

    return TenderService(mock_tender_repository)


# GET TENDER

@pytest.mark.asyncio
async def test_get_tender_success(
    tender_service,
    mock_tender_repository,
    fake_tender,
):

    mock_tender_repository.get_by_id.return_value = fake_tender
    result = await tender_service.get_tender(1)
    assert result.tender_id == 1
    mock_tender_repository.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_tender_not_found(
    tender_service,
    mock_tender_repository,
):

    mock_tender_repository.get_by_id.return_value = None
    with pytest.raises(TenderNotFoundException):
        await tender_service.get_tender(999)


# DATE VALIDATION

def test_validate_dates_success(tender_service):
    publish_date = date.today()
    end_date = publish_date + timedelta(days=10)
    tender_service.validate_dates(publish_date, end_date)


def test_validate_dates_invalid(tender_service):
    publish_date = date.today()
    end_date = publish_date
    with pytest.raises(TenderBusinessRuleException):
        tender_service.validate_dates(publish_date, end_date)


# GET TENDERS

@pytest.mark.asyncio
async def test_get_tenders_pagination(
    tender_service,
    mock_tender_repository,
):
    await tender_service.get_tenders(page=2, limit=5)
    mock_tender_repository.get_all.assert_awaited_once_with(skip=5, limit=5, status=None, tender_type=None,)


# UPDATE TENDER

@pytest.mark.asyncio
async def test_update_tender_closed_not_allowed(
    tender_service,
    mock_tender_repository,
    fake_tender,
):

    fake_tender.status = "closed"
    mock_tender_repository.get_by_id.return_value = fake_tender

    with pytest.raises(TenderBusinessRuleException):
        await tender_service.update_tender(
            tender_id=1,
            update_data={"tender_title": "Updated Tender"},
        )


# STATUS TRANSITION

@pytest.mark.asyncio
async def test_invalid_status_transition(
    tender_service,
    mock_tender_repository,
    fake_tender,
):

    fake_tender.status = "open"

    mock_tender_repository.get_by_id.return_value = fake_tender

    with pytest.raises(InvalidTenderStatusException):

        await tender_service.update_tender_status(
            tender_id=1,
            new_status="assigned",
        )


@pytest.mark.asyncio
async def test_valid_status_transition(
    tender_service,
    mock_tender_repository,
    fake_tender,
):

    fake_tender.status = "open"

    mock_tender_repository.get_by_id.return_value = fake_tender
    mock_tender_repository.update.return_value = fake_tender

    await tender_service.update_tender_status(
        tender_id=1,
        new_status="closed",
    )

    mock_tender_repository.update.assert_awaited_once_with(
        fake_tender,
        {"status": "closed"},
    )

    mock_tender_repository.commit.assert_awaited_once()
