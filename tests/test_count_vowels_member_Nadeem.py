

import pytest

from helpers import load_module

cv = load_module("count_vowels")


# ---------------------------------------------------------------------------
# count_vowels  (9 tests)
# boundaries: length 0 | length 1 (vowel / consonant) | length 2 |
#             characters just outside the vowel set ("y", accented "e")
# ---------------------------------------------------------------------------
@pytest.mark.boundary
@pytest.mark.parametrize(
    "text, expected",
    [
        ("", 0),  # shortest possible input
        ("a", 1),  # single vowel
        ("b", 0),  # single consonant
        ("ab", 1),  # shortest mixed input
        ("y", 0),  # 'y' is not counted as a vowel
        ("é", 0),  # accented e is not in "aeiouAEIOU"
        (" ", 0),  # whitespace only
    ],
)
def test_count_vowels_boundaries(text, expected):
    assert cv.count_vowels(text) == expected


@pytest.mark.negative
@pytest.mark.parametrize("bad_input", [None, ["a", "e"]])
def test_count_vowels_rejects_non_strings(bad_input):
    with pytest.raises(TypeError):
        cv.count_vowels(bad_input)


# ---------------------------------------------------------------------------
# MODULE-LEVEL tests for count_vowels.py  (7 tests)
# ---------------------------------------------------------------------------
@pytest.mark.module
@pytest.mark.parametrize("text", ["Education", "PYTHON", "Software Quality", "xyz"])
def test_module_result_does_not_depend_on_case(text):
    assert cv.count_vowels(text.lower()) == cv.count_vowels(text.upper())


@pytest.mark.module
@pytest.mark.parametrize(
    "text, expected",
    [
        ("a" * 1000, 1000),  # very long input, all vowels
        ("b" * 1000, 0),  # very long input, no vowels
        ("ab" * 500, 500),  # very long input, alternating
    ],
)
def test_module_long_inputs(text, expected):
    assert cv.count_vowels(text) == expected
