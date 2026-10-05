# py-closewat

A Python port of the bundled [original `closewat.c`](closewat.c) for analyzing water molecules in X-ray PDB structures; the C source does not name its author or license.

Does the Python port reproduce the original C program's water assignments and occupancy/B-factor adjustments?

[`pyclosewat.py`](pyclosewat.py) reads PDB atom records, groups nearby waters, assigns chains and conformers, and writes water-only PDB records plus a contact log. [`test_reference.py`](test_reference.py) compiles the unchanged C source with GCC and runs both command-line programs on pinned structures. [`tools/compare_reference.py`](tools/compare_reference.py) saves their outputs and reports differences by original atom serial.

## Result

**The port is not equivalent to the C program on these small examples.** With default options, both preserve the same water coordinates and atom serials, but every output residue number differs. Ordering, some occupancies, and some B-factors also differ.

| PDB | Waters, each program | Different residue numbers | Different occupancies | Different B-factors |
|---|---:|---:|---:|---:|
| 1IR0 | 129 | 129 | 0 | 2 |
| 1UBQ | 58 | 58 | 2 | 4 |
| 1CTF | 62 | 62 | 4 | 2 |
| 2CI2 | 64 | 64 | 6 | 8 |

Counts are per water record, from [`results/reference/comparison.json`](results/reference/comparison.json). Full C/Python PDB outputs and logs are in [`results/reference/`](results/reference/). The tests check complete saved outputs and the explicit disagreements; passing them does **not** mean the two algorithms agree.

The existing [`pdb_water_analysis.csv`](pdb_water_analysis.csv) has 844 rows of structure metadata and water counts. It is not a C-versus-Python validation dataset, and its download workflow was not rerun here.

## Reproduce

From the repository root, with Python, [uv](https://docs.astral.sh/uv/), and GCC installed:

```bash
uv venv .venv && uv pip install --python .venv/bin/python pytest
nice -n 19 .venv/bin/python -m pytest -q test_reference.py test_pyclosewat.py test_integration.py
nice -n 19 .venv/bin/python tools/compare_reference.py --output /tmp/closewat-comparison
```

Local CPU only; no GPU or paid service. Test inputs are bundled, so tests need no network access. Only environment setup downloads packages. The analysis CLI uses the Python standard library; batch plotting scripts need the optional packages in [`requirements.txt`](requirements.txt). For single-file usage, see [QUICKSTART.md](QUICKSTART.md).

## Limitations

- Default options on these small X-ray structures are the reference scope; other structures and option combinations are not validated against C.
- Numbering and occupancy/B-factor disagreements remain unresolved. Do not substitute this port for the C program without checking the output.
- Logs and diagnostic classifications are recorded, but diagnostic-code equivalence is not established.
- The C program is a comparison baseline, not experimental ground truth for water placement or hydrogen bonding.
- Original C authorship and redistribution terms need confirmation; there is no license file in this repository.

## Prior work and data

This project builds on the included [`closewat.c`](closewat.c), not a new water-analysis algorithm. The original author/source URL is not recorded in the file or its initial repository commit. Structures come from the [RCSB PDB](https://www.rcsb.org/): [1IR0](https://www.rcsb.org/structure/1IR0), [1UBQ](https://www.rcsb.org/structure/1UBQ), [1CTF](https://www.rcsb.org/structure/1CTF), and [2CI2](https://www.rcsb.org/structure/2CI2). PDB depositor credits remain in the input headers; the format is documented by [wwPDB](https://www.wwpdb.org/documentation/file-format).

[Reference notes](docs/REFERENCE.md) describe the comparison, input provenance, and the next parity work.
