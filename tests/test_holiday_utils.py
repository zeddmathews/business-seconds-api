from datetime import date, timedelta
from app.utils.holiday_utils import calculate_easter, get_observed_date

def test_calculate_easter_known_date():
    assert calculate_easter(2025) == date(2025, 4, 20)

def test_get_observed_date_sunday_shift():
    sunday = date(2023, 12, 25)
    assert get_observed_date(sunday) == sunday

    sunday = date(2023, 12, 24)
    expected = sunday + timedelta(days=1)
    assert get_observed_date(sunday) == expected

def test_get_observed_date_weekday():
    weekday = date(2025, 12, 25)
    assert get_observed_date(weekday) == weekday