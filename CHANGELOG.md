# Changelog

All notable changes to py-closewat are documented here.

## [2.1.0] - 2026-01-13 - Bug Fixes and Documentation Cleanup

### Fixed
- Fixed IndexError when p_attype is empty in seeneighbor() and diagclose()
- Fixed ZeroDivisionError in relateem() when both B-factors are zero
- Fixed test scoping bug in test_pyclosewat.py Args class
- Removed all emojis from documentation files

### Changed
- Cleaned up documentation to follow GitHub best practices
- Updated README.md with complete documentation
- All 45 tests now pass

---

## [2.0.0] - 2024-11-13 - Complete Rewrite and Enhancement

### Major Milestone: Production Ready

This release represents a complete overhaul of the pyclosewat implementation, fixing all critical bugs, implementing all missing functionality, and adding comprehensive testing.

### Fixed Critical Bugs

#### Neighbor Chain Logic
- **Issue**: Infinite loops and circular references in neighbor pointer logic
- **Fix**: Proper index tracking and cycle detection in `thisthird()`, `split4()`, and `reorg4()`
- **Impact**: Eliminates crashes and hangs when processing complex water networks

#### List Iteration Issues
- **Issue**: Modifying lists while iterating in `noconformers()`
- **Fix**: Proper indexing and safe list modifications
- **Impact**: Prevents skipped elements and incorrect processing

#### Sorting Functions
- **Issue**: Incomplete replication of C sorting behavior
- **Fix**: Proper multi-key sorting with `get_sort_key_occb()`, `get_sort_key_chain()`, etc.
- **Impact**: Waters now sorted correctly by occupancy, B-factor, and chain

#### File I/O Handling
- **Issue**: Complex and error-prone stdin/file handling
- **Fix**: Simplified approach with proper error handling
- **Impact**: Reliable processing of both files and stdin

### Implemented Missing Functions

1. **`swap01(pw0, pw1)`** - Swap two PDBRecord objects
2. **`seeneighbor(pwap, pwaq, dsq, top)`** - Diagnose water-neighbor relationships
3. **`diagclose(pwap, pwaq, dsq, top)`** - Diagnose close contacts
4. **`confchange(pwp, top)`** - Change conformer designation
5. **`printclose(pwap, pwaq, dsq, fp)`** - Print close contact information
6. **`closetitle(top)`** - Print header for close contacts section

### Completed Incomplete Functions

- **`proximity(top)`**: Complete rewrite with split4 detection, water-water and water-protein contact analysis
- **`thisthird(top, p0)`**: Enhanced with proper neighbor chain traversal and quartet detection  
- **`split4(pwap, top)`**: Splits quartets into pairs based on distances
- **`reorg4(top, p0, p1, p2, p3)`**: Reorganizes waters into optimal pairing

### Comprehensive Testing Suite

- 45+ unit and integration tests
- Tests for all classes and functions
- Edge case and error handling coverage
- Distance calculation validation
- Output format verification

### Documentation

- Complete README.md with usage examples
- Quick start guide (QUICKSTART.md)
- Algorithm details and diagnostic codes
- Troubleshooting section

### Code Quality

- Type hints for function signatures
- Descriptive error messages with context
- Input validation for PDB lines
- Coordinate range checking

### Validation Against C Version

- Distance calculations match exactly
- Water detection identical
- Conformer handling produces same results  
- Output format compatible
- Diagnostic codes match
- Sorting produces equivalent ordering

---

## [1.0.0] - Initial Release

### Initial Features
- Basic Python port of closewat.c
- Water counting functionality
- Statistical analysis tools

### Known Issues (Fixed in 2.0.0)
- Incomplete implementation of core functions
- Missing error handling
- No test suite
- Bugs in neighbor chain logic

---

For full details, see the [README.md](README.md) and test files.
