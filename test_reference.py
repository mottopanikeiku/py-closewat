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
@pytest.mark.parametrize("name", ("1UBQ", "1CTF"))
def test_single_chain_option_preserves_c_numbering(name, c_reference, tmp_path):
    c = run_cli([str(c_reference), "-S"], INPUTS[name], tmp_path / "c")["output"]
    python = run_cli([sys.executable, str(ROOT / "pyclosewat.py"), "-S"],
                     INPUTS[name], tmp_path / "python")["output"]
    assert compare(c, python)["parsed_equal_in_order"]
    assert records(python)[0]["resnum"] == 1
    assert {water["chain"] for water in records(python)} == {"S"}


SYNTHETIC_GROUP = """\
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N  
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C  
HETATM    3  O  AHOH A 101      13.000  13.000  13.000  0.25 20.00           O  
HETATM    4  O  BHOH A 101      13.600  13.000  13.000  0.25 20.00           O  
HETATM    5  O  CHOH A 101      13.000  13.600  13.000  0.25 20.00           O  
HETATM    6  O  DHOH A 101      13.000  13.000  13.600  0.25 20.00           O  
HETATM    7  O   HOH A 102      16.000  16.000  16.000  1.00 20.00           O  
"""


@pytest.mark.parametrize("positions", (3, 4))
def test_documented_higher_order_grouping_difference(positions, c_reference, tmp_path):
    """Synthetic 3- and 4-position water: C groups all positions; the port does not.

    Triple/quad grouping is not ported (README limitations). When it is, this
    test should fail and the documentation should change with it.
    """
    lines = SYNTHETIC_GROUP.splitlines(keepends=True)
    input_path = tmp_path / "group.pdb"
    input_path.write_text("".join(lines[:2 + positions] + lines[-1:]))
    c = run_cli([str(c_reference)], input_path, tmp_path / "c")["output"]
    python = run_cli([sys.executable, str(ROOT / "pyclosewat.py")], input_path, tmp_path / "python")["output"]
    assert sorted(r["conformer"] for r in records(c)) == [" ", *"ABCD"[:positions]]
    assert sorted(r["conformer"] for r in records(python)) == [" "] * (positions - 1) + ["A", "B"]


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
