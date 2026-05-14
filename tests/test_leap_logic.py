import pytest

from leap import is_leap_year


@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (1, False),
        (4, True),
        (99, False),
        (100, False),
        (101, False),
        (399, False),
        (400, True),
        (401, False),
        (1896, True),
        (1900, False),
        (1904, True),
        (1999, False),
        (2000, True),
        (2001, False),
        (2023, False),
        (2024, True),
    ],
)
def test_is_leap_year_returns_expected_result(year, expected):
    assert is_leap_year(year) is expected
