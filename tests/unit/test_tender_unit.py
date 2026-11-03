
from datetime import date, timedelta
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions.exception import (
    InvalidTenderStatusException,
    TenderBusinessRuleException,
    TenderNotFoundException,
)
from app.services.tender_service import TenderService


class FakeTender:

    def __init__(
        self,
        tender_id=1,
        status="open",
        publish_date=None,
        end_date=None,
    ):

        self.tender_id = tender_id
        self.status = status
        self.publish_date = publish_date or date.today()
        self.end_date = end_date or (
            date.today() + timedelta(days=10)
        )


class FakeTenderRepository:

    def __init__(self):

        self.tender = FakeTender()

        self.create = AsyncMock(return_value=self.tender)
        self.get_by_id = AsyncMock(return_value=self.tender)
        self.get_all = AsyncMock(return_value=[self.tender])
        self.get_open_tenders = AsyncMock(
            return_value=[self.tender]
        )
        self.update = AsyncMock(return_value=self.tender)
        self.commit = AsyncMock()
        self.rollback = AsyncMock()


@pytest.fixture
def repository():
    return FakeTenderRepository()


@pytest.fixture
def service(repository):

    return TenderService(repository)


# GET TENDER
@pytest.mark.asyncio
async def test_get_tender_success(service, repository):
    result = await service.get_tender(1)
    assert result.tender_id == 1
    repository.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_tender_not_found(service, repository):
    repository.get_by_id.return_value = None
    with pytest.raises(TenderNotFoundException):
        await service.get_tender(999)


# DATE VALIDATION

@pytest.mark.asyncio
def test_validate_dates_success(service):
    publish_date = date.today()
    end_date = publish_date + timedelta(days=10)
    service.validate_dates(publish_date, end_date)


@pytest.mark.asyncio
def test_validate_dates_invalid(service):
    publish_date = date.today()
    end_date = publish_date
    with pytest.raises(TenderBusinessRuleException):

        service.validate_dates(publish_date, end_date)


       
# GET TENDERS

@pytest.mark.asyncio
async def test_get_tenders_pagination(service, repository):

    await service.get_tenders(
        page=2,
        limit=5,
    )

    repository.get_all.assert_called_once_with(
        skip=5,
        limit=5,
        status=None,
        tender_type=None,
    )


# UPDATE TENDER
@pytest.mark.asyncio
async def test_update_tender_closed_not_allowed( service,repository,):
    
    repository.tender.status = "closed"
    update_data = { "tender_title": "Updated Tender",}

    with pytest.raises(TenderBusinessRuleException):
        await service.update_tender(
            tender_id=1,
            update_data=update_data,
        )


# STATUS TRANSITION
@pytest.mark.asyncio
async def test_invalid_status_transition(
    service,
    repository,
):

    repository.tender.status = "open"
    with pytest.raises(InvalidTenderStatusException):
        await service.update_tender_status(
            tender_id=1,
            new_status="assigned",
        )

@pytest.mark.asyncio
async def test_valid_status_transition( service, repository,):
    repository.tender.status = "open"

    await service.update_tender_status(
        tender_id=1,
        new_status="closed",
    )
    repository.update.assert_called_once_with(
        repository.tender,
        {"status": "closed"},
    )
    repository.commit.assert_called_once()

