
import ast
import csv

import pytest

from helpers import ROOT, load_module

CSV_FILE = ROOT / "data" / "test_cases.csv"


def read_cases():
    with open(CSV_FILE, newline="", encoding="utf-8") as handle:
        return [
            pytest.param(row, id=f"{row['test_id']}-{row['function']}")
            for row in csv.DictReader(handle)
        ]


@pytest.mark.csv
@pytest.mark.parametrize("row", read_cases())
def test_cases_from_csv(row):
    func = getattr(load_module(row["module"]), row["function"])
    args = ast.literal_eval(row["args"])
    expected = row["expected"]

    if expected.startswith("raises:"):
        error_type = {"TypeError": TypeError, "ValueError": ValueError}[expected.split(":")[1]]
        with pytest.raises(error_type):
            func(*args)
    else:
        assert func(*args) == ast.literal_eval(expected)
