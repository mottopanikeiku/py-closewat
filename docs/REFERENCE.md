# C/Python reference comparison

## Method

`tools/compare_reference.py` compiles the bundled, unchanged `closewat.c` using `gcc -std=c99 -O0 closewat.c -lm`. Each CLI runs with default options in its own temporary directory, with a 60-second subprocess timeout. No PDB conversion, coordinate trimming, or filtering is applied to the inputs.

The comparison aligns output waters by original atom serial, checks parsed PDB fields, records output ordering separately, and checks byte equality. `results/reference/comparison.json` includes every differing field, the input SHA-256 digests, missing/extra serials, and counts. Full PDB outputs, stdout, stderr, and logs are kept alongside it. The temporary executable path is replaced with `closewat` in the saved C log heading; output PDB files are unmodified.

`test_reference.py` compiles and executes C again, checks both full output files against the saved outputs, and checks the observed comparison against the explicit difference report. It also asserts that the original water atom serials and coordinates survive in both implementations. A small mutation test checks that changing occupancy or reversing record order is detected. Missing GCC or a failed C process is a test failure, not a skip.

These are disagreement regression tests, **not an assertion of algorithm parity**. Changes that improve parity should update the affected expected output and report only after reviewing the new C comparison; do not blindly regenerate expected files to make a failure disappear.

## Observations

The recorded run used CPython 3.13.15, GCC 16.2.1, and pytest 9.1.1 on Linux x86_64. `nice -n 19 .venv/bin/python -m pytest -q test_reference.py test_pyclosewat.py test_integration.py` passed all 50 tests (the 5 new reference tests and 45 existing tests). Commands and observed results are saved in [`validation.txt`](../results/reference/validation.txt). Batch analysis, coverage, nondefault options, and other compiler/platform builds were not run.

| Input | C waters | Python waters | Residue-number mismatches | Occupancy mismatches | B-factor mismatches |
|---|---:|---:|---:|---:|---:|
| 1IR0 | 129 | 129 | 129 | 0 | 2 |
| 1UBQ | 58 | 58 | 58 | 2 | 4 |
| 1CTF | 62 | 62 | 62 | 4 | 2 |
| 2CI2 | 64 | 64 | 64 | 6 | 8 |

Source: `results/reference/comparison.json`. Every case has a different serial ordering. None is byte-equal or equal as an ordered list of parsed records. There are no missing/extra serials. Chain, conformer labels, atom identity, and coordinates match after alignment on these inputs; this does not establish behavior on other inputs. Logs have different layouts, and diagnostic-code equivalence was not tested.

Examples of substantive disagreements:

- 1IR0 serials 693 and 753: C emits B=9.54, Python emits B=8.35.
- 1UBQ serial 641: C emits occupancy=0.35 and B=25.44; Python emits 0.34 and 20.90.
- 2CI2 serial 527: C emits occupancy=0.37 and B=12.76; Python emits 0.32 and 10.61.

The cause of each disagreement has not been isolated. They are not explained away as floating-point tolerance. Existing Python unit tests and partial-pipeline integration tests do not justify substituting Python for C.

## Inputs and attribution

`1IR0.pdb` was already bundled. The other full PDB files were downloaded from the free RCSB service for this comparison:

- `tests/data/1UBQ.pdb`: https://files.rcsb.org/download/1UBQ.pdb
- `tests/data/1CTF.pdb`: https://files.rcsb.org/download/1CTF.pdb
- `tests/data/2CI2.pdb`: https://files.rcsb.org/download/2CI2.pdb

All four headers specify X-ray diffraction. The original headers, depositor names, and publication references remain intact. Input hashes are pinned in the report; tests use these files offline and do not fetch current revisions.

The C file has no author/license notice. Its earliest recorded repository commit is `095ded4` (2025-04-25, “All files done”), with no upstream attribution supplied by the file. No new license is assigned to it here. The owner should identify the original source and confirm redistribution terms.

The existing 844-row CSV is retained unchanged. It has columns `pdb_id`, `resolution`, `rfree`, and `water_count`; it is metadata/count data, not these CLI comparisons. The existing batch download and plotting scripts were not rerun.

## Next step

Use the saved real disagreements to isolate numbering in `makechains()`/`sortmults()` and occupancy/B-factor adjustment in `relateem()`/`adjustqb()` against the corresponding C routines. The next change should add a small isolated reproducer for a real discrepancy before altering the algorithm, then rerun this comparison. Local CPU and no paid compute should be sufficient; no runtime or completion estimate has been measured. Default parity should precede claims about nondefault flags or diagnostic-code parity.
