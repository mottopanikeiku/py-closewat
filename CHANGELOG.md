# Changelog

## Atom-name parity fix

- The port stripped PDB atom names, so Tyr `OH` and Arg `NH1`/`NH2` were classified as hydrogens and skipped as nearest polar neighbours. It now keeps columns 13-16 raw, as `closewat.c` does. The too-far-water counts in the 1CTF and 2CI2 logs drop by one each and now match C.
- Byte-identical water outputs rose from 0/4 to 3/4; 1IR0 differs only in its eight tied residue numbers. Parsed-field parity (305/313) is unchanged.

## Default-output parity fixes

- I isolated saved numbering and occupancy/B-factor disagreements in four small real PDB pairs before changing the port.
- I restored chain numbering above the largest non-water residue, grouped conformer numbering, the multiple-conformer numbering gap, and C's adjustment based on original occupancy and B-factor.
- Parsed water-record parity rose from 0/313 to 305/313 across the bundled structures; three of four outputs match as ordered parsed records. Eight equal-key numbering differences in 1IR0 remain. Byte formatting and diagnostic equivalence are not claimed.
- I kept the old comparison files, added before/after outputs and direct C adjustment tests, and added CI for the offline tests. C authorship and license remain open.
- I fixed two issues found in independent review: chain-local reinsertion ranges cannot span another chain, and `-S` retains its numbering base after reinsertion. Regression tests cover mixed single/multiple chain ranges and two `-S` inputs; this is not general flag parity.

## C reference comparison and documentation correction

- Added `test_reference.py`, which compiles the unchanged `closewat.c` with GCC and runs both CLIs on 1IR0 and three additional small X-ray structures: 1UBQ, 1CTF, and 2CI2.
- Saved complete outputs, logs, and field-level disagreements in `results/reference/`; pinned public inputs in `tests/data/`.
- Found matching water counts and coordinates, but different residue numbering and order on every input, plus occupancy/B-factor disagreements. See [reference notes](docs/REFERENCE.md). No algorithm parity fix is claimed.
- Replaced README status/badges and unsupported completeness, superiority, and C-equivalence claims with the measured comparison.
- Removed the MIT badge: the linked LICENSE file did not exist. The C source's original author and redistribution terms remain unidentified.

## Earlier history (as previously recorded)

### 2026-01-13

The earlier changelog recorded fixes for empty atom-type handling in `seeneighbor()` and `diagclose()`, zero B-factor handling in `relateem()`, and an Args scoping issue in the unit tests, plus documentation edits.

Its statement that “all 45 tests now pass” did not identify a command or saved run. The existing tests do not compile or execute C, so that statement was not evidence of C compatibility.

### 2024-11-13

The earlier changelog described work on neighbor traversal, conformer cleanup, sorting, file I/O, contact diagnostics, and additional unit/integration tests. Those are descriptions of implementation work, not validation that every function matches C.

The previous claims of readiness, identical conformer handling, matching diagnostic codes, and equivalent sorting were unsupported by a C execution test and have been withdrawn. The new comparison contradicts output equivalence on the checked real structures.

### Initial port

The repository contains a Python port of `closewat.c`, water-counting scripts, and batch-analysis scripts. Historical release labels have been removed here rather than imply a maturity level not established by tests.
