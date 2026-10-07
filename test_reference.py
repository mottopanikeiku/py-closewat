"""C comparisons, including explicit regressions for documented disagreements.

These tests do not assert algorithmic equivalence: see docs/REFERENCE.md.
GCC is required; an unavailable or broken C reference is a test failure.
"""

import hashlib
import json
import sys

import pytest

from tools.compare_reference import INPUTS, ROOT, compare, compile_reference, records, run_cli
from tools.compare_reference import REPRODUCERS

RESULTS = ROOT / "results/parity/after"
EXPECTED = json.loads((RESULTS / "comparison.json").read_text())["cases"]


@pytest.fixture(scope="session")
def c_reference(tmp_path_factory):
    executable = tmp_path_factory.mktemp("c-reference") / "closewat"
    compile_reference(executable)
    return executable


@pytest.mark.parametrize("name", INPUTS)
def test_real_pdb_reference_and_documented_differences(name, c_reference, tmp_path):
    input_path = INPUTS[name]
    assert hashlib.sha256(input_path.read_bytes()).hexdigest() == EXPECTED[name]["input_sha256"]
    assert "EXPDTA    X-RAY DIFFRACTION" in input_path.read_text()
    c = run_cli([str(c_reference)], input_path, tmp_path / "c")["output"]
    python = run_cli([sys.executable, str(ROOT / "pyclosewat.py")], input_path, tmp_path / "python")["output"]

    # Assert complete outputs, not merely nonempty files or aggregate counts.
    assert c == (RESULTS / name / "c.pdb").read_text()
    assert python == (RESULTS / name / "python.pdb").read_text()
    assert compare(c, python) == {key: value for key, value in EXPECTED[name].items()
                                  if key != "input_sha256"}

    # A useful positive comparison despite differences in numbering and Q/B.
    input_waters = records("\n".join(line for line in input_path.read_text().splitlines()
                                    if line.startswith(("ATOM  ", "HETATM"))
                                    and line[17:20] == "HOH"))
    def positions(text_records):
        return sorted((r["serial"], r["x"], r["y"], r["z"]) for r in text_records)
    assert positions(records(c)) == positions(records(python)) == positions(input_waters)

@pytest.mark.parametrize("name", REPRODUCERS)
def test_extracted_pair_parity(name, c_reference, tmp_path):
    """Each four-record real-data reproducer now agrees on every parsed field."""
    c = run_cli([str(c_reference)], REPRODUCERS[name], tmp_path / "c")["output"]
    python = run_cli([sys.executable, str(ROOT / "pyclosewat.py")],
                     REPRODUCERS[name], tmp_path / "python")["output"]
    comparison = compare(c, python)
    assert comparison["parsed_equal_in_order"]
    assert comparison["field_mismatches"] == {}
    assert comparison["c_waters"] == comparison["python_waters"] == 2



def test_comparison_detects_changed_fields_and_order():
    text = (RESULTS / "1UBQ/c.pdb").read_text()
    lines = text.splitlines(keepends=True)
    mutated = lines.copy()
    first = mutated[0]
    mutated[0] = first[:54] + "  0.12" + first[60:]
    mismatch = compare(text, "".join(mutated))
    assert mismatch["field_mismatches"] == {"occupancy": 1}
    assert mismatch["different_waters"] == 1
    assert not mismatch["parsed_equal_in_order"]
    assert mismatch["same_serial_order"]
    reordered = compare(text, "".join(reversed(lines)))
    assert reordered["field_mismatches"] == {}
    assert not reordered["same_serial_order"]
    assert not reordered["parsed_equal_in_order"]
