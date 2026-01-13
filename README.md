# py-closewat

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#testing)

A Python toolkit to analyze water molecules in X-ray diffraction PDB structures. This is a complete and improved reimplementation of the original C `closewat` algorithm with enhanced features, comprehensive testing, and better error handling.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Algorithm Details](#algorithm-details)
- [Repository Structure](#repository-structure)
- [Development](#development)
- [License](#license)

## Features

### Core Water Analysis
- Identify and classify water molecules in protein structures
- Detect water conformers (alternate positions for the same water site)
- Analyze close contacts between waters and protein atoms
- Detect metal coordination (water molecules coordinating metal ions)
- Calculate hydrogen bonding networks between waters
- Renumber and reorganize waters by chain and occupancy

### Complete Implementation
- All core functions from C version implemented
- Missing functions added: `seeneighbor`, `diagclose`, `confchange`, `swap01`, `printclose`, `closetitle`
- Complete proximity analysis with diagnostic codes
- Proper conformer handling (A/B/C/D alternate positions)
- Metal coordination detection
- Comprehensive error handling and validation

### Testing and Quality
- 45+ unit and integration tests covering all functions
- Edge case and error handling tests
- Distance calculation validation
- Output format verification

## Installation

### Prerequisites

- Python 3.7+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Analyze a Single PDB File

```bash
python pyclosewat.py input.pdb output.pdb
```

This will:
1. Read the input PDB file
2. Identify all water molecules
3. Analyze water-water and water-protein contacts
4. Detect alternate conformations
5. Write annotated waters to output PDB
6. Generate a detailed log file (`closewat.log`)

### Command Line Options

```bash
python pyclosewat.py [options] <input.pdb> <output.pdb>
```

**Options:**
- `-S` : Single chain mode - assign all waters to chain 'S'
- `-H` : High B-factor quality mode - adjust occupancies for high B-value waters
- `-B` : Automatic bump correction - move waters to resolve close contacts
- `-X <dist>` : Maximum H-bond distance (default: 3.2 A)
- `-M <dist>` : Minimum H-bond distance (default: 2.5 A)
- `-L <dist>` : Minimum hydrogen distance (default: 1.5 A)
- `-O <dist>` : Minimum heteroatom distance (default: 3.9 A)

**Examples:**

```bash
# Basic analysis
python pyclosewat.py 1abc.pdb 1abc_waters.pdb

# Single chain mode with tighter distance threshold
python pyclosewat.py -S -M 2.3 input.pdb output.pdb

# Automatic bump correction with high B quality mode
python pyclosewat.py -B -H input.pdb output.pdb
```

### Python API

```python
import pyclosewat as pc

# Create structures
top = pc.TotalSt()
water = pc.PDBRecord()

# Parse PDB line
line = "HETATM  100  O   HOH A 200      10.00  20.00  30.00  1.00 25.00           O"
pc.strtorec(line, water)

# Calculate distance between two atoms
dist_squared = pc.pdbdist(water1, water2)

# Check if atom is metal
is_metal = pc.ismetal("MG")  # Returns 1

# Detect water residues
is_water = pc.is_water_residue("HOH")  # Returns True
```

## Testing

Run the comprehensive test suite:

```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=pyclosewat --cov-report=html
```

### Test Coverage

- **Unit Tests** (`test_pyclosewat.py`): Tests for all classes and functions
- **Integration Tests** (`test_integration.py`): End-to-end workflow tests
- **Test Fixtures** (`test_fixtures.py`): Sample PDB structures for testing

## Algorithm Details

### Water Analysis Pipeline

1. **First Pass - Counting**: Count ATOM/HETATM records, identify waters and chains
2. **Second Pass - Processing**: Parse all atom and water records
3. **Conformer Cleanup**: Remove input conformer designations, adjust occupancies
4. **Water Network Analysis**: Find nearest-neighbor waters, identify H-bonding networks
5. **Conformer Assignment**: Assign A/B/C/D conformer labels with proper occupancies
6. **Chain Assignment**: Assign waters to nearest protein chains
7. **Proximity Analysis**: Check all water-protein contacts, detect issues
8. **Sorting and Output**: Sort waters, write annotated PDB and log

### Diagnostic Codes

Waters are assigned codes based on their environment:

| Code | Label | Description |
|------|-------|-------------|
| 0 | faraway | Too far from all neighbors (> 3.9 A) |
| 1 | ok now | Properly positioned |
| 2 | metal | Coordinating a metal ion (acceptable) |
| 3 | leave | Independent from original input |
| 4 | altconf | Conformer code altered |
| 5 | replace | Needs conformer assignment |
| 6 | bump | Too close, can be auto-corrected |
| 7 | edit | Too close, needs manual editing |

## Repository Structure

```
py-closewat/
├── closewat.c                 # Original C implementation (reference)
├── pyclosewat.py              # Complete Python implementation
├── test_pyclosewat.py         # Unit tests
├── test_integration.py        # Integration tests
├── test_fixtures.py           # Test data and fixtures
├── run_tests.py               # Simple test runner
├── analyze_pdb_files.py       # Batch PDB analysis
├── analyze_water_distribution.py  # Statistical analysis
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── CHANGELOG.md               # Version history
└── QUICKSTART.md              # Quick start guide
```

## Development

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with proper tests
4. Run the test suite: `pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Coding Standards

- Follow PEP 8 style guidelines
- Add type hints to new functions
- Write docstrings for all public functions
- Include tests for new functionality

## Improvements Over C Version

### Accessibility
- Clean Python syntax vs C pointer arithmetic
- Comprehensive documentation with examples
- Type hints for better IDE support
- Interactive Python API for scripting

### Robustness
- 45+ unit tests covering all functions
- Input validation at all entry points
- Comprehensive error messages with context
- Edge case handling (empty files, malformed lines, etc.)

### Features
- Extended water residue detection (HOH, WAT, H2O, TIP3, etc.)
- Improved metal detection with comprehensive list
- Statistical analysis tools for batch processing
- Log file with detailed diagnostic information

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'pyclosewat'`
```bash
# Ensure you're in the correct directory
cd py-closewat
python pyclosewat.py input.pdb output.pdb
```

**Problem**: No waters in output
```bash
# Check input file has water molecules
grep "HETATM" input.pdb | grep "HOH"
```

## License

This project is licensed under the MIT License.

## Citation

If you use py-closewat in your research, please cite:

```bibtex
@software{pyclosewat2024,
  title = {py-closewat: A Python toolkit for analyzing water molecules in PDB structures},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/mottopanikeiku/py-closewat}
}
```

## References

- PDB file format: https://www.wwpdb.org/documentation/file-format
- Original closewat algorithm

---

**Status**: Production Ready
