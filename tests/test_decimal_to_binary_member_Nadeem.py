
import pytest

from helpers import load_module

d2b = load_module("decimal_to_binary")


# ---------------------------------------------------------------------------
# decimal_to_binary_iterative  (8 tests)
# boundaries: -1 | 0 | 1 | 2 | 3 | 7 | 8 (bit-length changes at 1, 2, 4, 8)
# ---------------------------------------------------------------------------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "num, expected",
    [
        (-1, "-0b1"),  # just below zero
        (0, "0b0"),  # zero boundary
        (1, "0b1"),  # just above zero
        (2, "0b10"),  # first 2-bit number
        (3, "0b11"),  # last 2-bit number
        (7, "0b111"),  # last 3-bit number
        (8, "0b1000"),  # first 4-bit number
    ],
)
def test_iterative_boundaries(num, expected):
    assert d2b.decimal_to_binary_iterative(num) == expected


@pytest.mark.negative
def test_iterative_rejects_none():
    with pytest.raises(TypeError):
        d2b.decimal_to_binary_iterative(None)


# ---------------------------------------------------------------------------
# decimal_to_binary_recursive_helper  (8 tests)
# boundaries: 0 and 1 are the recursion exit cases; 2, 3, 4 are the first
# values that need recursion.
# ---------------------------------------------------------------------------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0"),  # exit case
        (1, "1"),  # exit case
        (2, "10"),  # first value that recurses
        (3, "11"),
        (4, "100"),
    ],
)
def test_helper_boundaries(value, expected):
    assert d2b.decimal_to_binary_recursive_helper(value) == expected


@pytest.mark.negative
@pytest.mark.parametrize("bad_input", ["number", ""])
def test_helper_rejects_non_numeric(bad_input):
    with pytest.raises(ValueError):
        d2b.decimal_to_binary_recursive_helper(bad_input)


@pytest.mark.negative
def test_helper_negative_input_recurses_forever():
    # Documented limitation: the helper is for positive values only. For -1,
    # divmod(-1, 2) == (-1, 1), so the exit case is never reached.
    with pytest.raises(RecursionError):
        d2b.decimal_to_binary_recursive_helper(-1)


# ---------------------------------------------------------------------------
# decimal_to_binary_recursive  (8 tests)
# boundaries: "0", "1", "-1"; invalid: empty, blank, mixed text
# defects: "-0" and "--5" are accepted (see docs/ECP_BVA_notes.md)
# ---------------------------------------------------------------------------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "number, expected",
    [("0", "0b0"), ("1", "0b1"), ("-1", "-0b1")],
)
def test_recursive_boundaries(number, expected):
    assert d2b.decimal_to_binary_recursive(number) == expected


@pytest.mark.negative
@pytest.mark.parametrize("bad_input", ["", "   ", "12abc"])
def test_recursive_invalid_strings(bad_input):
    with pytest.raises(ValueError):
        d2b.decimal_to_binary_recursive(bad_input)


@pytest.mark.defect
@pytest.mark.xfail(reason="DEFECT: '-0' returns '-0b0' (bin(-0) is '0b0')", strict=True)
def test_recursive_negative_zero():
    assert d2b.decimal_to_binary_recursive("-0") == "0b0"


@pytest.mark.defect
@pytest.mark.xfail(reason="DEFECT: '--5' is accepted and returned as '-0b101'", strict=True)
def test_recursive_double_minus_should_be_rejected():
    with pytest.raises(ValueError):
        d2b.decimal_to_binary_recursive("--5")


# ---------------------------------------------------------------------------
# MODULE-LEVEL tests for decimal_to_binary.py  (8 tests)
# Round trip: converting back with int(result, 2) must return the original.
# ---------------------------------------------------------------------------
@pytest.mark.module
@pytest.mark.parametrize("n", [-8, -1, 0, 1, 2, 7, 8])
def test_module_iterative_round_trip(n):
    assert int(d2b.decimal_to_binary_iterative(n), 2) == n


@pytest.mark.module
def test_module_recursive_round_trip_large_value():
    n = 2**40 + 1
    assert int(d2b.decimal_to_binary_recursive(n), 2) == n
