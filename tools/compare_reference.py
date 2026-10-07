"""Compile closewat.c and compare both CLIs on pinned, offline PDB inputs."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "1IR0": ROOT / "1IR0.pdb",
    "1UBQ": ROOT / "tests/data/1UBQ.pdb",
    "1CTF": ROOT / "tests/data/1CTF.pdb",
    "2CI2": ROOT / "tests/data/2CI2.pdb",
}
REPRODUCERS = {
    path.stem: path for path in sorted((ROOT / "tests/data/reproducers").glob("*.pdb"))
}


def compile_reference(destination):
    subprocess.run(
        ["gcc", "-std=c99", "-O0", str(ROOT / "closewat.c"), "-lm", "-o", str(destination)],
        check=True, capture_output=True, text=True, timeout=60,
    )


def run_cli(command, input_path, workdir):
    workdir.mkdir(parents=True)
    output_path = workdir / "waters.pdb"
    process = subprocess.run(
        [*command, str(input_path), str(output_path)], cwd=workdir,
        capture_output=True, text=True, timeout=60,
    )
    if process.returncode:
        raise RuntimeError(f"{command[0]} exited {process.returncode}: {process.stderr}")
    return {
        "output": output_path.read_text(),
        "log": (workdir / "closewat.log").read_text(),
        "stdout": process.stdout,
        "stderr": process.stderr,
    }


def records(text):
    """Parse every emitted PDB field; preserve ordering and atom identity."""
    parsed = []
    for line in text.splitlines():
        if not line.startswith(("ATOM  ", "HETATM")):
            raise ValueError(f"Unexpected output line: {line!r}")
        parsed.append({
            "record": line[:6].strip(), "serial": int(line[6:11]),
            "atom": line[12:16].strip(), "conformer": line[16],
            "residue": line[17:20].strip(), "chain": line[21],
            "resnum": int(line[22:26]), "x": float(line[30:38]),
            "y": float(line[38:46]), "z": float(line[46:54]),
            "occupancy": float(line[54:60]), "bfactor": float(line[60:66]),
            "element": line[76:78].strip(),
        })
    return parsed


def compare(c_text, python_text):
    c_records, python_records = records(c_text), records(python_text)
    c_by_id = {r["serial"]: r for r in c_records}
    py_by_id = {r["serial"]: r for r in python_records}
    if len(c_by_id) != len(c_records) or len(py_by_id) != len(python_records):
        raise ValueError("Duplicate output atom serials; cannot align waters")
    differences = []
    for serial in sorted(c_by_id.keys() & py_by_id.keys()):
        for field, value in c_by_id[serial].items():
            if value != py_by_id[serial][field]:
                differences.append({"serial": serial, "field": field,
                                    "c": value, "python": py_by_id[serial][field]})
    return {
        "c_waters": len(c_records), "python_waters": len(python_records),
        "byte_equal": c_text == python_text,
        "parsed_equal_in_order": c_records == python_records,
        "same_serial_order": [r["serial"] for r in c_records] == [r["serial"] for r in python_records],
        "only_c_serials": sorted(c_by_id.keys() - py_by_id.keys()),
        "only_python_serials": sorted(py_by_id.keys() - c_by_id.keys()),
        "different_waters": len({d["serial"] for d in differences}),
        "field_mismatches": dict(sorted(Counter(d["field"] for d in differences).items())),
        "differences": differences,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="Directory for generated outputs and comparison.json")
    parser.add_argument("--reproducers", action="store_true",
                        help="Compare the small extracted disagreement inputs instead")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    report = {"options": "default (no flags)", "cases": {}}
    with tempfile.TemporaryDirectory(prefix="closewat-reference-") as temporary:
        work = Path(temporary)
        executable = work / "closewat"
        compile_reference(executable)
        for name, input_path in (REPRODUCERS if args.reproducers else INPUTS).items():
            c = run_cli([str(executable)], input_path, work / name / "c")
            python = run_cli([sys.executable, str(ROOT / "pyclosewat.py")], input_path, work / name / "python")
            case_dir = output / name
            case_dir.mkdir(exist_ok=True)
            for label, result in (("c", c), ("python", python)):
                (case_dir / f"{label}.pdb").write_text(result["output"])
                # Normalize executable paths in log headings, not PDB outputs.
                log = result["log"].replace(str(executable), "closewat")
                log = log.replace(str(ROOT / "pyclosewat.py"), "pyclosewat.py")
                (case_dir / f"{label}.log").write_text(log)
                (case_dir / f"{label}.stderr").write_text(result["stderr"])
                (case_dir / f"{label}.stdout").write_text(result["stdout"])
            report["cases"][name] = {
                "input_sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                **compare(c["output"], python["output"]),
            }
            summary = report["cases"][name]
            print(f"{name}: C={summary['c_waters']}, Python={summary['python_waters']}; "
                  f"field mismatches={summary['field_mismatches']}; "
                  f"same order={summary['same_serial_order']}")
    (output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
