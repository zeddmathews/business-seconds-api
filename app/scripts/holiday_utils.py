import asyncpg
from datetime import date, timedelta

FIXED_HOLIDAYS = [
    (1, 1, "New Year's Day"),
    (3, 21, "Human Rights Day"),
    (4, 27, "Freedom Day"),
    (5, 1, "Workers' Day"),
    (6, 16, "Youth Day"),
    (8, 9, "National Women's Day"),
    (9, 24, "Heritage Day"),
    (12, 16, "Day of Reconciliation"),
    (12, 25, "Christmas Day"),
    (12, 26, "Day of Goodwill"),
]

def calculate_easter(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def get_observed_date(holi_date: date) -> date:
    if holi_date.weekday() == 6:
        return holi_date + timedelta(days=1)
    return holi_date

async def seed_public_holidays(conn: asyncpg.Connection, year_start: int, years: int = 10):
    async def insert_holiday(holi_date: date, observed_date: date, holi_name: str):
        day_of_week = holi_date.strftime('%A')
        await conn.execute(
            """
            INSERT INTO public_holidays (holi_date, observed_date, holi_name, day_of_week)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (holi_date) DO NOTHING
            """,
            holi_date, observed_date, holi_name, day_of_week
        )

    for year in range(year_start, year_start + years):
        for month, day, name in FIXED_HOLIDAYS:
            try:
                actual_date = date(year, month, day)
            except ValueError:
                continue

            observed_date = get_observed_date(actual_date)
            await insert_holiday(actual_date, observed_date, name)

        easter = calculate_easter(year)
        good_friday = easter - timedelta(days=2)
        family_day = easter + timedelta(days=1)

        await insert_holiday(good_friday, get_observed_date(good_friday), "Good Friday")
        await insert_holiday(family_day, get_observed_date(family_day), "Family Day")