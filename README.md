# SQE Project Phase 2: Unit Test Automation

**Project:** [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) (fork)

**Members:** Zaran (Member A), Nadeem (Member B)

## Modules tested

| Module | Functions |
|---|---|
| `conversions/decimal_to_binary.py` | `decimal_to_binary_iterative`, `decimal_to_binary_recursive_helper`, `decimal_to_binary_recursive` |
| `strings/count_vowels.py` | `count_vowels` |
| `bit_manipulation/addition_without_arithmetic.py` | `add` |

## Where our work is

- `tests/`: our tests are the files named `*member*`, `test_smoke.py` and `test_data_driven_csv.py` (the other files in `tests/` belong to the original project)
- `docs/ECP_BVA_notes.docx`: ECP/BVA notes
- `docs/test_cases.xlsx` and `data/test_cases.csv`: Excel test cases and the CSV data the tests read
- `pytest.ini` and `conftest.py`: groups and execution order
- `video/`: setup video

## Setup

```
python -m venv venv
source venv/Scripts/activate
pip install -r requirements-test.txt
```

## Run the tests

| Goal | Command |
|---|---|
| All tests | `pytest` |
| In parallel | `pytest -n auto` |
| In the defined order | `pytest -n 0 -v` |
| One group | `pytest -m smoke` (groups: `smoke`, `ecp`, `boundary`, `negative`, `module`, `csv`, `defect`) |
| Only our tests | `pytest tests/test_smoke.py tests/test_data_driven_csv.py tests/*member*.py` |

Group order: smoke, ecp, boundary, negative, module, csv, defect.

## Known bugs found

`add(-1, 1)` never returns, and `decimal_to_binary_recursive("-0")` and `("--5")` give wrong results. These tests are marked `xfail`, so they show as `xfailed` in the report.

## Who did what

- **Zaran:** ECP tests for all 3 modules, smoke tests, CSV data-driven tests, Excel test cases, ECP/BVA notes, pytest configuration, setup video
- **Nadeem:** BVA and invalid-input tests for all 3 modules
