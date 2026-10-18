

import pytest

from helpers import load_module

d2b = load_module("decimal_to_binary")


# ---------------------------------------------------------------------------
# decimal_to_binary_iterative  (8 tests)
# classes: zero | small positive | medium positive | large positive |
#          negative | float input | string input
# ---------------------------------------------------------------------------
@pytest.mark.ecp
@pytest.mark.parametrize(
    "num, expected",
    [
        (0, "0b0"),  # zero
        (5, "0b101"),  # small positive
        (35, "0b100011"),  # medium positive
        (1023, "0b1111111111"),  # large positive (all ones)
        (-2, "-0b10"),  # small negative
        (-40, "-0b101000"),  # larger negative
    ],
)
def test_iterative_valid_classes(num, expected):
    assert d2b.decimal_to_binary_iterative(num) == expected


@pytest.mark.ecp
@pytest.mark.negative
@pytest.mark.parametrize("bad_input", [16.16, "0xff"])  # float class, string class
def test_iterative_invalid_classes(bad_input):
    with pytest.raises(TypeError):
        d2b.decimal_to_binary_iterative(bad_input)


# ---------------------------------------------------------------------------
# decimal_to_binary_recursive_helper  (7 tests)
# classes: int | numeric string | whitespace-padded numeric string |
#          non-numeric string
# ---------------------------------------------------------------------------
@pytest.mark.ecp
@pytest.mark.parametrize(
    "value, expected",
    [
        (1000, "1111101000"),  # int
        (255, "11111111"),  # int, all ones
        (100, "1100100"),  # int
        (16, "10000"),  # int, power of two
        ("72", "1001000"),  # numeric string
        (" 9 ", "1001"),  # numeric string with spaces
    ],
)
def test_helper_valid_classes(value, expected):
    assert d2b.decimal_to_binary_recursive_helper(value) == expected


@pytest.mark.ecp
@pytest.mark.negative
def test_helper_non_numeric_string_class():
    with pytest.raises(ValueError):
        d2b.decimal_to_binary_recursive_helper("number")


# ---------------------------------------------------------------------------
# decimal_to_binary_recursive  (8 tests)
# classes: zero | positive | negative | padded string | float | words
# ---------------------------------------------------------------------------
@pytest.mark.ecp
@pytest.mark.parametrize(
    "number, expected",
    [
        (0, "0b0"),  # zero
        (40, "0b101000"),  # positive int
        (-40, "-0b101000"),  # negative int
        ("  25 ", "0b11001"),  # string with surrounding spaces
        (1000, "0b1111101000"),  # larger positive
        ("7", "0b111"),  # numeric string
    ],
)
def test_recursive_valid_classes(number, expected):
    assert d2b.decimal_to_binary_recursive(number) == expected


@pytest.mark.ecp
@pytest.mark.negative
@pytest.mark.parametrize("bad_input", ["forty", 40.8])  # words class, float class
def test_recursive_invalid_classes(bad_input):
    with pytest.raises(ValueError):
        d2b.decimal_to_binary_recursive(bad_input)


# ---------------------------------------------------------------------------
# MODULE-LEVEL tests for decimal_to_binary.py  (8 tests)
# Both implementations must agree with Python's built-in bin().
# ---------------------------------------------------------------------------
@pytest.mark.module
@pytest.mark.parametrize("n", [0, 10, 255, 1024])
def test_module_iterative_matches_builtin_bin(n):
    assert d2b.decimal_to_binary_iterative(n) == bin(n)


@pytest.mark.module
@pytest.mark.parametrize("n", [3, 64, 500, 4095])
def test_module_recursive_matches_iterative(n):
    assert d2b.decimal_to_binary_recursive(n) == d2b.decimal_to_binary_iterative(n)
