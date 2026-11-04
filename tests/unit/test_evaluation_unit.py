from decimal import Decimal
from unittest.mock import AsyncMock

import pytest

from app.services.evaluation_service import EvaluationService
from app.schemas.evaluation_schema import EvaluationCreate

from app.core.exceptions.exception import EvaluationBusinessRuleException


@pytest.fixture
def service():

    db = AsyncMock()
    service = EvaluationService(db)

    service.quotation_repository = AsyncMock()
    service.tender_repository = AsyncMock()
    service.evaluation_repository = AsyncMock()

    return service


@pytest.fixture
def evaluation_data():

    return EvaluationCreate(
        eligibility_score=Decimal("25"),
        company_profile_score=Decimal("27"),
        proposal_score=Decimal("35"),
        eligibility_status="eligible",
        decision="approved",
        remarks="Good proposal",
    )


@pytest.fixture
def quotation():

    class QuotationObject:
        quotation_id = 1
        tender_id = 10
        vendor_id = 5
        status = "submitted"

    return QuotationObject()


@pytest.fixture
def tender():

    class TenderObject:
        tender_id = 10
        status = "closed"

    return TenderObject()


async def test_create_evaluation_success(
    service,
    evaluation_data,
    quotation,
    tender,
):

    service.quotation_repository.get_by_id.return_value = quotation

    service.tender_repository.get_by_id.return_value = tender

    service.evaluation_repository.get_by_quotation_id.return_value = None

    service.evaluation_repository.create.side_effect = (
        lambda evaluation: evaluation
    )

    result = await service.create_evaluation(
        quotation_id=1,
        evaluation_data=evaluation_data,
        admin_id=100,
    )

    assert result.total_score == Decimal("87")

    assert result.evaluated_by == 100

    assert quotation.status == "approved"

    service.db.commit.assert_awaited_once()


async def test_evaluation_for_ineligible_vendor_rejected(
    service,
    quotation,
    tender,
):

    service.quotation_repository.get_by_id.return_value = quotation

    service.tender_repository.get_by_id.return_value = tender

    service.evaluation_repository.get_by_quotation_id.return_value = None

    data = EvaluationCreate(
        eligibility_score=Decimal("10"),
        company_profile_score=Decimal("15"),
        proposal_score=Decimal("20"),
        eligibility_status="not_eligible",
        decision="approved",
    )

    with pytest.raises(EvaluationBusinessRuleException):

        await service.create_evaluation(
            quotation_id=1,
            evaluation_data=data,
            admin_id=100,
        )


async def test_duplicate_evaluation(
    service,
    evaluation_data,
    quotation,
    tender,
):

    service.quotation_repository.get_by_id.return_value = quotation

    service.tender_repository.get_by_id.return_value = tender

    service.evaluation_repository.get_by_quotation_id.return_value = object()

    with pytest.raises(EvaluationBusinessRuleException):

        await service.create_evaluation(
            quotation_id=1,
            evaluation_data=evaluation_data,
            admin_id=100,
        )


async def test_tender_must_be_closed_or_under_evaluation(
    service,
    evaluation_data,
    quotation,
):

    service.quotation_repository.get_by_id.return_value = quotation

    class OpenTender:
        tender_id = 10
        status = "open"

    service.tender_repository.get_by_id.return_value = OpenTender()

    with pytest.raises(EvaluationBusinessRuleException):

        await service.create_evaluation(
            quotation_id=1,
            evaluation_data=evaluation_data,
            admin_id=100,
        )


async def test_quotation_not_found( service, evaluation_data):

    service.quotation_repository.get_by_id.return_value = None

    with pytest.raises(Exception):

        await service.create_evaluation(
            quotation_id=999,
            evaluation_data=evaluation_data,
            admin_id=100,
        )

