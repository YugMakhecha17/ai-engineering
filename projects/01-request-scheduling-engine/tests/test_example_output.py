"""The documented example must keep producing the output shown in the project README."""

import subprocess
import sys
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "basic_usage.py"

EXPECTED = """\
== FIFO ==
req-1: summarise report
req-2: translate memo
req-3: classify ticket
== Priority (lower number = more urgent) ==
queued after cancel: 4
req-2 (p=0): interactive A
req-3 (p=0): interactive B
req-1 (p=5): batch job
req-5 (p=9): background
"""


def test_example_runs_and_prints_the_documented_output() -> None:
    result = subprocess.run(
        [sys.executable, str(EXAMPLE)], capture_output=True, text=True, check=True
    )
    assert result.stdout.replace("\r\n", "\n") == EXPECTED
