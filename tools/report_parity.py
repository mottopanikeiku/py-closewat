"""Summarize saved complete-output comparisons without measuring runtime."""
import argparse
import json
from pathlib import Path


def summarize(report):
    cases = report["cases"]
    total = sum(case["c_waters"] for case in cases.values())
    matched = sum(case["c_waters"] - case["different_waters"]
                  - len(case["only_c_serials"]) for case in cases.values())
    return {
        "structures": len(cases),
        "ordered_parsed_equal": sum(case["parsed_equal_in_order"] for case in cases.values()),
        "byte_equal": sum(case["byte_equal"] for case in cases.values()),
        "c_waters": total,
        "matched_waters_by_serial": matched,
        "water_parity_percent": 100 * matched / total,
        "only_python_serials": sum(len(case["only_python_serials"]) for case in cases.values()),
        "only_c_serials": sum(len(case["only_c_serials"]) for case in cases.values()),
        "field_mismatches": {
            field: sum(case["field_mismatches"].get(field, 0) for case in cases.values())
            for field in ("resnum", "occupancy", "bfactor")
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before", type=Path, default=Path("results/parity/before/comparison.json"))
    parser.add_argument("--after", type=Path, default=Path("results/parity/after/comparison.json"))
    parser.add_argument("--output", type=Path, default=Path("results/parity/summary.json"))
    args = parser.parse_args()
    before, after = (json.loads(path.read_text()) for path in (args.before, args.after))
    if {name: case["input_sha256"] for name, case in before["cases"].items()} != {
        name: case["input_sha256"] for name, case in after["cases"].items()
    }:
        raise ValueError("Before and after must use identical inputs")
    result = {"definition": "All parsed fields of a water agree after alignment by original serial; order scored separately.",
              "options": "default (no flags)",
              "before": summarize(before), "after": summarize(after)}
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
