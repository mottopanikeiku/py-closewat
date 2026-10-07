# py-closewat

A Python port of the bundled [original `closewat.c`](closewat.c) for analyzing water molecules in X-ray PDB structures; the C source does not name its author or license.

Does the Python port reproduce the original C program's water assignments and occupancy/B-factor adjustments?

[`pyclosewat.py`](pyclosewat.py) reads PDB atom records, groups nearby waters, assigns chains and conformers, and writes water-only PDB records plus a contact log. [`test_reference.py`](test_reference.py) compiles the unchanged C source with GCC and runs both command-line programs on pinned structures. [`tools/compare_reference.py`](tools/compare_reference.py) saves their outputs and reports differences by original atom serial.

## Result

**I increased parsed water-record parity from 0/313 to 305/313 (97.44%) on the four bundled structures.** The port is still **not equivalent** to C. Three structures now match every parsed field in output order; eight waters in 1IR0 still have different residue numbers because their occupancy and B-factor sort keys tie.

| PDB | Waters | Matching complete records, before → after | Remaining Q/B differences |
|---|---:|---:|---:|
| 1IR0 | 129 | 0 → 121 | 0 |
| 1UBQ | 58 | 0 → 58 | 0 |
| 1CTF | 62 | 0 → 62 | 0 |
| 2CI2 | 64 | 0 → 64 | 0 |

I count a match only when **every parsed field** agrees after alignment by original atom serial; output order is scored separately. The [before/after summary](results/parity/summary.json) and [full comparisons](results/parity/) contain the counts, outputs, and logs. Byte equality remains 0/4 because atom-name spacing differs.

I extracted [four small real-data reproducers](tests/data/reproducers/), fixed chain numbering and conformer-group sorting, and ported C's original-occupancy/B-factor weighting. All four pairs now agree on parsed output. [Reference notes](docs/REFERENCE.md) explain the causes and the unresolved ties, rather than treating them as floating-point noise.

The existing [`pdb_water_analysis.csv`](pdb_water_analysis.csv) has 844 rows of structure metadata and water counts. It is not a C-versus-Python validation dataset, and its download workflow was not rerun here.

## Reproduce

From the repository root, with Python, [uv](https://docs.astral.sh/uv/), and GCC installed:

```bash
uv venv .venv && uv pip install --python .venv/bin/python pytest
nice -n 19 .venv/bin/python -m pytest -q test_reference.py test_adjustment.py test_pyclosewat.py test_integration.py
nice -n 19 .venv/bin/python tools/compare_reference.py --output /tmp/closewat-comparison
```

Local CPU only; no GPU or paid service. Test inputs are bundled, so tests need no network access. Only environment setup downloads packages. The analysis CLI uses the Python standard library; batch plotting scripts need the optional packages in [`requirements.txt`](requirements.txt). For single-file usage, see [QUICKSTART.md](QUICKSTART.md).

## Limitations

- Default options on these small X-ray structures are the reference scope; other structures and option combinations are not validated against C.
- Equal-key sorting in C does not define a consistent tie order; eight residue-number disagreements remain. Do not substitute Python for C without checking the output.
- Logs and diagnostic classifications are recorded, but diagnostic-code equivalence is not established.
- The C program is a comparison baseline, not experimental ground truth for water placement or hydrogen bonding.
- Original C authorship and redistribution terms need confirmation; there is no license file in this repository.

## Prior work and data

This project builds on the included [`closewat.c`](closewat.c), not a new water-analysis algorithm. The original author/source URL is not recorded in the file or its initial repository commit. Structures come from the [RCSB PDB](https://www.rcsb.org/): [1IR0](https://www.rcsb.org/structure/1IR0), [1UBQ](https://www.rcsb.org/structure/1UBQ), [1CTF](https://www.rcsb.org/structure/1CTF), and [2CI2](https://www.rcsb.org/structure/2CI2). PDB depositor credits remain in the input headers; the format is documented by [wwPDB](https://www.wwpdb.org/documentation/file-format).

[Reference notes](docs/REFERENCE.md) describe the comparison, input provenance, and remaining parity limits.

Written with AI coding assistance.
