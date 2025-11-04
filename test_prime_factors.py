# file: tests/test_factors.py
import pytest
from prime_factors import (
    validate_user_input,
    is_prime,
    get_unique_prime_factors,
    print_prime_factors,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2", 2),
        ("12", 12),
        ("26541", 26541),
    ],
)
def test_valid_inputs(value, expected):
    assert validate_user_input(value) == expected


@pytest.mark.parametrize("value", ["1", "asdfasdf", "3.7", None, "", [], {}])
def test_invalid_inputs(capsys, value):
    validate_user_input(value)
    captured = capsys.readouterr()
    assert "Please" in captured.out


@pytest.mark.parametrize("value", ["0", "-1", "-300"])
def test_zero_or_negative_values(capsys, value):
    validate_user_input(value)
    captured = capsys.readouterr()
    assert "Number should not be zero or less" in captured.out


@pytest.mark.parametrize(
    "value, expected",
    [
        (3, True),
        (7, True),
        (983, True),
        (983, True),
        (8, False),
        (100, False),
    ],
)
def test_should_be_prime(value, expected):
    assert is_prime(value) == expected


@pytest.mark.parametrize(
    "value,expected",
    [
        (26541, [3, 983]),
        (10, [2, 5]),
        (987654, [2, 3, 97, 1697]),
    ],
)
def test_get_unique_prime_factors(value, expected):
    assert get_unique_prime_factors(value) == expected


@pytest.mark.parametrize("value", [[3, 983], [2, 3, 97, 1697]])
def test_print_prime_factors(capsys, value):
    print_prime_factors(value)
    captured = capsys.readouterr()
    for n in value:
        assert f"Prime factor found: {n}" in captured.out
