
import pytest

from helpers import load_module

cv = load_module("count_vowels")


# ---------------------------------------------------------------------------
# count_vowels  (7 tests)
# classes: lowercase | uppercase | digits mixed in | no vowels | only vowels |
#          mixed case sentence | non-string input
# ---------------------------------------------------------------------------
@pytest.mark.ecp
@pytest.mark.parametrize(
    "text, expected",
    [
        ("hello world", 3),  # lowercase
        ("HELLO WORLD", 3),  # uppercase
        ("123 hello world", 3),  # digits ignored
        ("rhythm", 0),  # no vowels
        ("AEIOUaeiou", 10),  # only vowels, both cases
        ("the quick BROWN fox", 5),  # mixed case
    ],
)
def test_count_vowels_classes(text, expected):
    assert cv.count_vowels(text) == expected


@pytest.mark.ecp
@pytest.mark.negative
def test_count_vowels_non_string_class():
    with pytest.raises(TypeError):
        cv.count_vowels(12345)


# ---------------------------------------------------------------------------
# MODULE-LEVEL tests for count_vowels.py  (8 tests)
# ---------------------------------------------------------------------------
@pytest.mark.module
@pytest.mark.parametrize("text", ["", "xyz", "education", "A quick brown fox!"])
def test_module_count_is_between_zero_and_length(text):
    assert 0 <= cv.count_vowels(text) <= len(text)


@pytest.mark.module
@pytest.mark.parametrize(
    "left, right",
    [("hello", "world"), ("", "aeiou"), ("xyz", "xyz"), ("AEI", "ou")],
)
def test_module_count_is_additive_over_concatenation(left, right):
    assert cv.count_vowels(left + right) == cv.count_vowels(left) + cv.count_vowels(right)
