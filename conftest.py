"""Project-wide pytest configuration: execution order of test groups.

Order of groups (Task 4 - "set the execution order of groups and test cases"):

    smoke -> ecp -> boundary -> negative -> module -> csv -> defect

How it works
------------
* Every test already carries a group marker (e.g. @pytest.mark.boundary).
* This hook gives each test a numeric position with the pytest-order plugin,
  based on its group (100, 101, 102, ...).
* Tests that set their own @pytest.mark.order(n) (see tests/test_smoke.py) keep
  their explicit position, which is how individual TEST ordering is shown.

Note: ordering is guaranteed in a normal run (`pytest`). With the parallel
option (`pytest -n auto`) tests are split across worker processes, so the
global order is not guaranteed - use `pytest -n 0` when order matters.
"""

import pytest

GROUP_ORDER = ["smoke", "ecp", "boundary", "negative", "module", "csv", "defect"]
GROUP_BASE = 100


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.get_closest_marker("order"):
            continue  # an explicit @pytest.mark.order(n) wins
        ranks = [
            GROUP_BASE + GROUP_ORDER.index(mark.name)
            for mark in item.iter_markers()
            if mark.name in GROUP_ORDER
        ]
        if ranks:
            item.add_marker(pytest.mark.order(min(ranks)))
