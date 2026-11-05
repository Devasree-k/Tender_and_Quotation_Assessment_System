
from unittest.mock import AsyncMock

import pytest

from app.services.sanction_service import SanctionService

from app.core.exceptions.exception import SanctionBusinessRuleException


@pytest.fixture
def service(mock_sanction_repository, mock_email_service):

    service = SanctionService(mock_sanction_repository,mock_email_service)
    return service


# 1. DUPLICATE SANCTION

@pytest.mark.asyncio
async def test_duplicate_sanction_rejected(service, mock_sanction_repository):

    mock_sanction_repository.get_by_tender.return_value = object()
    with pytest.raises(SanctionBusinessRuleException):

        await service.create_sanction(
            quotation_id=1,
            amount=450000,
            admin_id=100,
        )
        
