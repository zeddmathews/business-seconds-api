import pytest

@pytest.mark.asyncio
async def test_is_holiday_endpoint(client):
    response = await client.get('/is-holiday?date=2025-01-01')
    assert response.status_code == 200
    data = await response.get_json()
    assert data['is_holiday'] is True

    response = await client.get('/is-holiday?date=2025-01-02')
    assert response.status_code == 200
    data = await response.get_json()
    assert data['is_holiday'] is False

    response = await client.get('/is-holiday')
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_business_seconds_endpoint(client):
    response = await client.get('/business_seconds?start_time=2025-07-21T09:00:00&end_time=2025-07-21T10:00:00')
    assert response.status_code == 200
    data = await response.get_json()
    assert data['total_business_seconds'] == 3600

    response = await client.get('/business_seconds?start_time=2025-07-21T10:00:00&end_time=2025-07-21T09:00:00')
    assert response.status_code == 400

    response = await client.get('/business_seconds')
    assert response.status_code == 400