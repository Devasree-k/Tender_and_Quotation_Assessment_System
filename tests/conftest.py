
import os
from datetime import date, timedelta
from decimal import Decimal
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from app.api.dependencies.database import get_db
from app.main import app
from app.models.user_model import User

from app.core.security import hash_password

from app.schemas.evaluation_schema import EvaluationCreate
from tests.test_database import (
    test_engine,
    TestSessionLocal,
    create_test_tables,
    drop_test_tables,
)

# DATABASE FIXTURE

@pytest_asyncio.fixture
async def test_db():
    await create_test_tables()
    async with TestSessionLocal() as session:

        # Create test admin
        admin = User(
            username="testadmin",
            email="admin@test.com",
            hashed_password=hash_password("TestAdmin@123"),
            role="admin",
            is_active=True,
        )

        session.add(admin)
        await session.commit()
        yield session
    await drop_test_tables()
    await test_engine.dispose()


# API CLIENT

@pytest_asyncio.fixture
async def client(test_db):
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()


# AUTHENTICATION FIXTURES

@pytest.fixture
def admin_credentials():
    return {
        "username":  "testadmin",
        "password": "TestAdmin@123",
    }


@pytest_asyncio.fixture
async def admin_token(client, admin_credentials):
    response = await client.post(
        "/api/auth/login",
        data=admin_credentials,
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token):
    return {
        "Authorization": f"Bearer {admin_token}"
    }

# Vendor registration

@pytest.fixture
def vendor_registration_data():

    return {
        "user": {
            "username": "testvendor",
            "email": "vendor@test.com",
            "hash_password": "Vendor@12345",
        },
        "vendor": {
            "company_name": "Test Construction",
            "owner_name": "Test Owner",
            "company_phone": "9876543210",
            "pro_name": "Test PRO",
            "pro_phone": "9876543211",
            "registration_id": "TEST-REG-001",
            "company_experience": 5,
            "company_category": "startup",
            "company_address": "Coimbatore",
        },
    }


@pytest_asyncio.fixture
async def vendor_token(client, vendor_registration_data,):
    register_response = await client.post(
        "/api/auth/register",
        json=vendor_registration_data,
    )
    assert register_response.status_code == 201, register_response.text
    login_response = await client.post(
        "/api/auth/login",
        data={
            "username": "testvendor",
            "password": "Vendor@12345",
        },
    )
    assert login_response.status_code == 200, login_response.text
    return login_response.json()["access_token"]


@pytest.fixture
def vendor_headers(vendor_token):
    return {"Authorization": f"Bearer {vendor_token}"}



# COMMON TEST DATA
@pytest.fixture
def sample_tender_data():

    today = date.today()

    return {
        "tender_title": "Test Road Maintenance",
        "description": "Testing tender creation",
        "eligibility_criteria": "Registered construction company",
        "estimated_cost": 500000,
        "publish_date": today.isoformat(),
        "end_date": (today + timedelta(days=15)).isoformat(),
        "tender_type": "new_project",
        "completion_period": 90,
    }

@pytest.fixture
def sample_quotation_data():

    return {
        "tender_id": 1,
        "amount_quoted": 450000,
        "proposal": "We can complete the project within 90 days.",
    }


@pytest.fixture
def sample_evaluation_data():
    return {
        "eligibility_score": "25",
        "company_profile_score": "27",
        "proposal_score": "35",
        "eligibility_status": "eligible",
        "decision": "approved",
        "remarks": "Good proposal",
    }

@pytest.fixture
def sample_sanction_data():

    return {
        "quotation_id": 1,
        "amount": 450000,
    }


# =========================================================
# MOCK REPOSITORY FIXTURES
# =========================================================

@pytest.fixture
def mock_tender_repository():

    repository = AsyncMock()

    repository.create = AsyncMock()
    repository.get_by_id = AsyncMock()
    repository.get_all = AsyncMock()
    repository.get_open_tenders = AsyncMock()
    repository.update = AsyncMock()
    repository.commit = AsyncMock()
    repository.rollback = AsyncMock()

    return repository


@pytest.fixture
def mock_quotation_repository():

    repository = AsyncMock()

    repository.create = AsyncMock()
    repository.get_by_id = AsyncMock()
    repository.get_by_tender_vendor = AsyncMock()
    repository.get_by_vendor = AsyncMock()
    repository.get_all = AsyncMock()
    repository.get_vendor_id_by_user_id = AsyncMock()
    repository.get_quotation_details = AsyncMock()
    repository.commit = AsyncMock()
    repository.rollback = AsyncMock()

    return repository


@pytest.fixture
def mock_evaluation_repository():

    repository = AsyncMock()

    repository.create = AsyncMock()
    repository.get_by_id = AsyncMock()
    repository.get_by_quotation_id = AsyncMock()
    repository.get_all = AsyncMock()
    repository.commit = AsyncMock()
    repository.rollback = AsyncMock()

    return repository


@pytest.fixture
def mock_sanction_repository():
    repository = AsyncMock()
    repository.create = AsyncMock()
    repository.get_by_id = AsyncMock()
    repository.get_by_quotation_id = AsyncMock()
    repository.get_all = AsyncMock()
    repository.update_tender_status = AsyncMock()
    repository.commit = AsyncMock()
    repository.rollback = AsyncMock()
    return repository


# COMMON MODEL-LIKE OBJECTS

@pytest.fixture
def fake_tender():
    class FakeTender:
        tender_id = 1
        tender_title = "Test Tender"
        status = "open"
        publish_date = date.today()
        end_date = date.today() + timedelta(days=10)
    return FakeTender()


@pytest.fixture
def fake_quotation():
    class FakeQuotation:
        quotation_id = 1
        tender_id = 10
        vendor_id = 5
        amount_quoted = Decimal("450000.00")
        status = "submitted"
    return FakeQuotation()


@pytest.fixture
def fake_evaluation():
    class FakeEvaluation:
        evaluation_id = 1
        quotation_id = 1
        total_score = Decimal("87")
        decision = "approved"
    return FakeEvaluation()


@pytest.fixture
def fake_sanction():

    class FakeSanction:

        sanction_id = 1
        quotation_id = 1
        tender_id = 10
        sanctioned_amount = Decimal("450000.00")

    return FakeSanction()


@pytest.fixture
def mock_email_service():
    return AsyncMock()

