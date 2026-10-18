

import pytest

from helpers import load_module, run_add_with_timeout

mod = load_module("addition_without_arithmetic")


# ---------------------------------------------------------------------------
# add  (9 tests)
# boundaries: 0+0 | x+0 | 0+(-x) | -1+-1 | carry boundaries 1+1, 1+7, 1+255
# ---------------------------------------------------------------------------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "first, second, expected",
    [
        (0, 0, 0),  # smallest operands
        (1, 0, 1),  # identity
        (0, -7, -7),  # zero plus negative
        (-1, -1, -2),  # smallest negative pair
        (1, 1, 2),  # first carry
        (1, 7, 8),  # carry ripples through 3 bits
        (1, 255, 256),  # carry ripples through 8 bits
    ],
)
def test_add_boundaries(first, second, expected):
    assert mod.add(first, second) == expected


# DEFECT: when the operands have different signs and the true sum is zero or
# positive, the carry keeps shifting left forever (Python ints are unbounded),
# so add() never returns. The call is made in a separate process with a
# timeout so a hang cannot freeze the test run.
@pytest.mark.defect
@pytest.mark.xfail(reason="DEFECT: add() never returns for mixed signs with sum >= 0", strict=True)
@pytest.mark.parametrize("first, second, expected", [(-1, 1, 0), (5, -3, 2)])
def test_add_mixed_signs_non_negative_result(first, second, expected):
    assert run_add_with_timeout(first, second) == expected


# ---------------------------------------------------------------------------
# MODULE-LEVEL tests for addition_without_arithmetic.py  (8 tests)
# ---------------------------------------------------------------------------
@pytest.mark.module
@pytest.mark.parametrize("a", [0, 1, -1, 12345, -99999])
def test_module_zero_is_identity(a):
    assert mod.add(a, 0) == a


@pytest.mark.module
@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (10, 20, 30), (7, 0, 9)])
def test_module_is_associative_for_non_negative_values(a, b, c):
    assert mod.add(mod.add(a, b), c) == mod.add(a, mod.add(b, c))
