from datetime import datetime, time, timedelta
from app.utils.holiday_utils import is_public_holiday
import asyncpg

async def calculate_business_seconds(start: datetime, end: datetime, conn: asyncpg.Connection) -> int:
    BUSINESS_START = time(8, 0, 0)
    BUSINESS_END = time(17, 0, 0)

    total_elapsed = 0
    current = start

    while current < end:
        if current.weekday() >= 5:
            current += timedelta(days=(7 - current.weekday()))
            current = datetime.combine(current.date(), BUSINESS_START)
            continue

        if await is_public_holiday(conn, current.date()):
            current += timedelta(days=1)
            current = datetime.combine(current.date(), BUSINESS_START)
            continue
        
        start_of_day = datetime.combine(current.date(), BUSINESS_START)
        end_of_day = datetime.combine(current.date(), BUSINESS_END)

        effective_start = max(current, start_of_day)
        effective_end = min(end, end_of_day)

        if effective_start < effective_end:
            total_elapsed += (effective_end - effective_start).total_seconds()

        current = datetime.combine((current + timedelta(days=1)).date(), BUSINESS_START)

    return int(total_elapsed)