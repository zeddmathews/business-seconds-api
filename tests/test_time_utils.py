import pytest
from datetime import datetime, time, timedelta
from app.utils.time_utils import calculate_business_seconds

@pytest.mark.asyncio
async def test_business_day():
    start = datetime(2025, 7, 21, 9, 0, 0)
    end = datetime(2025, 7, 21, 10, 0, 0)
    seconds = await calculate_business_seconds(start, end, None)
    assert seconds == 3600

@pytest.mark.asyncio
async def test_weekend_coverage():
    start = datetime(2025, 7, 19, 9, 0, 0)
    end = datetime(2025, 7, 21, 9, 0, 0)
    seconds = await calculate_business_seconds(start, end, None)
    assert seconds == 3600

@pytest.mark.asyncio
async def test_non_business_hours():
    start = datetime(2025, 7, 21, 7, 0, 0)
    end = datetime(2025, 7, 21, 8, 30, 0)
    seconds = await calculate_business_seconds(start, end, None)
    assert seconds == 1800

@pytest.mark.asyncio
async def test_multiple_days():
    start = datetime(2025, 7, 21, 16, 0, 0)
    end = datetime(2025, 7, 22, 10, 0, 0)
    seconds = await calculate_business_seconds(start, end, None)
    assert seconds == 10800


@pytest.mark.asyncio
async def test_zero_duration():
    dt = datetime(2025, 7, 21, 9, 0, 0)
    seconds = await calculate_business_seconds(dt, dt, None)
    assert seconds == 0