
from datetime import date, timedelta
from decimal import Decimal


def get_tender_payload():

    today = date.today()

    return {
        "tender_title": "Road Construction Project",
        "description": "Construction of a new public road.",
        "eligibility_criteria": "Minimum five years of experience.",
        "estimated_cost": "500000.00",
        "publish_date": today.isoformat(),
        "end_date": (today + timedelta(days=10)).isoformat(),
        "tender_type": "new_project",
        "completion_period": 180,
    }


# CREATE TENDER 

async def test_create_tender_success(client, admin_headers):

    response = await client.post(
        "/api/tenders/",
        json=get_tender_payload(),
        headers=admin_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["tender_title"] == "Road Construction Project"
    assert data["status"] == "open"
    assert data["publish_date"] == date.today().isoformat()
    assert data["end_date"] == (
        date.today() + timedelta(days=10)
    ).isoformat()


async def test_create_tender_invalid_cost(client, admin_headers):

    payload = get_tender_payload()
    payload["estimated_cost"] = "-100"

    response = await client.post(
        "/api/tenders/",
        json=payload,
        headers=admin_headers,
    )

    assert response.status_code == 422


async def test_create_tender_without_token(client):

    response = await client.post(
        "/api/tenders/",
        json=get_tender_payload(),
    )

    assert response.status_code == 401


# GET ALL TENDERS

async def test_get_all_tenders(client, admin_headers):

    response = await client.get(
        "/api/tenders/",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_get_tenders_with_pagination(
    client,
    admin_headers,
):
    response = await client.get(
        "/api/tenders/?page=1&limit=5",
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert len(response.json()) <= 5


# GET OPEN TENDERS 