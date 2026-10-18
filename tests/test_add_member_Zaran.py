

import pytest

from helpers import load_module

mod = load_module("addition_without_arithmetic")


# ---------------------------------------------------------------------------
# add  (7 tests)
# classes: both positive | zero operand | both negative |
#          mixed signs with a negative result
# (mixed signs with a zero/positive result are covered by Member B's defect
#  tests, because add() never returns for them)
# ---------------------------------------------------------------------------
@pytest.mark.ecp
@pytest.mark.parametrize(
    "first, second, expected",
    [
        (3, 5, 8),  # both positive
        (13, 5, 18),  # both positive, carries
        (100, 200, 300),  # both positive, larger
        (0, 7, 7),  # zero operand
        (-3, -4, -7),  # both negative
        (-7, 2, -5),  # mixed signs, negative result
        (-321, 1, -320),  # mixed signs, negative result
    ],
)
def test_add_classes(first, second, expected):
    assert mod.add(first, second) == expected


# ---------------------------------------------------------------------------
# MODULE-LEVEL tests for addition_without_arithmetic.py  (8 tests)
# add() must agree with the + operator, and addition must be commutative.
# ---------------------------------------------------------------------------
@pytest.mark.module
@pytest.mark.parametrize("a, b", [(2, 3), (10, 20), (99, 1), (1234, 4321), (0, 0)])
def test_module_matches_plus_operator(a, b):
    assert mod.add(a, b) == a + b


@pytest.mark.module
@pytest.mark.parametrize("a, b", [(4, 9), (15, 16), (-5, 2)])
def test_module_is_commutative(a, b):
    assert mod.add(a, b) == mod.add(b, a)
