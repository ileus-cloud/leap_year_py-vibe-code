import pytest

from leap import next_leap_years


@pytest.mark.parametrize(
    ("start_year", "expected_years"),
    [
        (2023, [2024, 2028, 2032, 2036, 2040]),
        (2024, [2028, 2032, 2036, 2040, 2044]),
        (1899, [1904, 1908, 1912, 1916, 1920]),
        (1999, [2000, 2004, 2008, 2012, 2016]),
    ],
)
def test_next_leap_years_returns_next_five_years(start_year, expected_years):
    assert next_leap_years(start_year) == expected_years


@pytest.mark.parametrize(
    ("count", "expected_years"),
    [
        (0, []),
        (-1, []),
    ],
)
def test_next_leap_years_returns_empty_list_for_non_positive_count(count, expected_years):
    assert next_leap_years(2024, count=count) == expected_years


def test_next_leap_years_returns_requested_count():
    assert next_leap_years(2023, count=3) == [2024, 2028, 2032]
