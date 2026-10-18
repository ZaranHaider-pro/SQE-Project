"""Shared helpers for the test files.

load_module("decimal_to_binary") finds decimal_to_binary.py anywhere inside the
repository and imports it, so the tests keep working no matter which folder the
module lives in.
"""

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_SKIP_DIRS = {"venv", ".venv", ".git", "tests", "site-packages", "__pycache__"}
_cache = {}


def find_module_file(name: str) -> Path:
    for path in sorted(ROOT.rglob(f"{name}.py")):
        if _SKIP_DIRS.isdisjoint(path.relative_to(ROOT).parts):
            return path
    raise FileNotFoundError(f"Could not find {name}.py inside {ROOT}")


def load_module(name: str):
    if name not in _cache:
        path = find_module_file(name)
        spec = importlib.util.spec_from_file_location(f"sqe_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _cache[name] = module
    return _cache[name]


def run_add_with_timeout(first: int, second: int, timeout: float = 3):
    """Run add(first, second) in a separate process.

    Returns the result, or None if the call did not finish within `timeout`
    seconds. A separate process is used because add() never returns for some
    inputs (see docs/ECP_BVA_notes.md), and a hung test must not freeze the
    whole test run (this also works on Windows).
    """
    path = find_module_file("addition_without_arithmetic")
    code = (
        "import importlib.util, sys;"
        "s = importlib.util.spec_from_file_location('m', sys.argv[1]);"
        "m = importlib.util.module_from_spec(s);"
        "s.loader.exec_module(m);"
        "print(m.add(int(sys.argv[2]), int(sys.argv[3])))"
    )
    try:
        done = subprocess.run(
            [sys.executable, "-c", code, str(path), str(first), str(second)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None
    return int(done.stdout.strip())
