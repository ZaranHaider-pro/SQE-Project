"""Smoke suite - one very quick sanity check per function.

Run only this suite with:  pytest -m smoke

These tests also demonstrate TEST-level execution order: each one has its own
@pytest.mark.order(n) (pytest-order plugin), so they always run 1, 2, 3, 4, 5
and always run before every other group (groups are ordered in conftest.py).
"""

import pytest

from helpers import load_module

d2b = load_module("decimal_to_binary")
cv = load_module("count_vowels")
add_mod = load_module("addition_without_arithmetic")


@pytest.mark.smoke
@pytest.mark.order(1)
def test_smoke_iterative():
    assert d2b.decimal_to_binary_iterative(5) == "0b101"


@pytest.mark.smoke
@pytest.mark.order(2)
def test_smoke_recursive_helper():
    assert d2b.decimal_to_binary_recursive_helper(5) == "101"


@pytest.mark.smoke
@pytest.mark.order(3)
def test_smoke_recursive():
    assert d2b.decimal_to_binary_recursive(5) == "0b101"


@pytest.mark.smoke
@pytest.mark.order(4)
def test_smoke_count_vowels():
    assert cv.count_vowels("hello") == 2


@pytest.mark.smoke
@pytest.mark.order(5)
def test_smoke_add():
    assert add_mod.add(2, 3) == 5
