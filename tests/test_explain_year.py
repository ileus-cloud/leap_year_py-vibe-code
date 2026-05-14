import pytest

from leap import explain_year


@pytest.mark.parametrize(
    ("year", "expected_text"),
    [
        (2000, "2000 - високосный год, потому что он делится на 400."),
        (1900, "1900 - не високосный год, потому что он делится на 100, но не делится на 400."),
        (2024, "2024 - високосный год, потому что он делится на 4 и не делится на 100."),
        (2023, "2023 - не високосный год, потому что он не делится на 4."),
    ],
)
def test_explain_year_returns_expected_message(year, expected_text):
    assert explain_year(year) == expected_text
