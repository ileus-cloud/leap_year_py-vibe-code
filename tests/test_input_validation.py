import pytest

from leap import parse_positive_year


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2024", 2024),
        (" 2024 ", 2024),
        ("0004", 4),
        ("\t2024\n", 2024),
    ],
)
def test_parse_positive_year_accepts_valid_input(value, expected):
    assert parse_positive_year(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "",
        "   ",
        "abc",
        "2024abc",
        "-1",
        "0",
        "2024.5",
    ],
)
def test_parse_positive_year_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        parse_positive_year(value)


@pytest.mark.xfail(
    reason="Current implementation removes inner spaces, so '20 24' becomes 2024. Treat as requirements question / potential bug.",
    strict=True,
)
def test_parse_positive_year_rejects_inner_spaces():
    with pytest.raises(ValueError):
        parse_positive_year("20 24")
