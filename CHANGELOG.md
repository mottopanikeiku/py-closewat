# Changelog

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
