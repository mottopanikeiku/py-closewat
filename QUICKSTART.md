# Quick Start Guide for py-closewat

Get started with py-closewat in 5 minutes.

## Installation

```bash
# Clone the repository
git clone https://github.com/mottopanikeiku/py-closewat.git
cd py-closewat

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Analyze a Single PDB File

```bash
# Download a sample PDB file (or use your own)
# Run analysis
python pyclosewat.py sample.pdb sample_output.pdb

# Check the log file
cat closewat.log
```

### View Results

The output PDB file (`sample_output.pdb`) contains:
- Renumbered waters organized by chain
- Conformer labels (A/B/C/D) for alternate positions
- Adjusted occupancies and B-factors

The log file (`closewat.log`) includes:
- Statistics on waters analyzed
- Close contact warnings
- Conformer assignments
- Diagnostic codes for problematic waters

### Use as a Python Library

```python
import pyclosewat as pc

# Create a water record
water = pc.PDBRecord()

# Parse a PDB line
line = "HETATM  100  O   HOH A 200      10.00  20.00  30.00  1.00 25.00           O"
pc.strtorec(line, water)

# Print coordinates
print(f"Water at ({water.p_xc}, {water.p_yc}, {water.p_zc})")
print(f"Occupancy: {water.p_occ}, B-factor: {water.p_bval}")

# Calculate distance between two waters
import math
dist_squared = pc.pdbdist(water, water2)
distance = math.sqrt(dist_squared)
print(f"Distance: {distance:.2f} Angstroms")
```

## Common Use Cases

### Detect Water Conformers

```bash
# Use -H flag to handle high B-factors
python pyclosewat.py -H input.pdb output.pdb
```

### Fix Close Contacts Automatically

```bash
# Use -B flag to automatically adjust water positions
python pyclosewat.py -B input.pdb output.pdb
```

### Adjust Distance Thresholds

```bash
# Set custom H-bond distance (default 3.2 A)
python pyclosewat.py -X 3.5 input.pdb output.pdb

# Set custom minimum distance (default 2.5 A)
python pyclosewat.py -M 2.0 input.pdb output.pdb
```

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with verbose output
pytest -v

# Generate coverage report
pytest --cov=pyclosewat --cov-report=html
```

## Understanding the Output

### PDB Output Format

```
HETATM  201  O  AHOH A 201      14.123  15.456  16.789  0.60 18.50           O
HETATM  201  O  BHOH A 201      14.234  15.567  16.890  0.40 18.50           O
```

- `AHOH`/`BHOH`: Alternate conformations (A has 60% occupancy, B has 40%)
- Occupancies sum to 1.00 for conformer groups
- B-factors adjusted based on group statistics

### Diagnostic Codes

| Code | Label | Description |
|------|-------|-------------|
| 0 | faraway | Water isolated from neighbors |
| 1 | ok now | Properly positioned |
| 2 | metal | Coordinating a metal ion |
| 4 | altconf | Conformer code adjusted |
| 6 | bump | Minor clash, auto-corrected |
| 7 | edit | Serious clash, needs manual fix |

## Troubleshooting

### Problem: No waters in output

Check that input has water molecules:
```bash
grep "HOH" input.pdb
grep "HETATM.*HOH" input.pdb
```

### Problem: All waters marked as problematic

Try using bump correction or adjusting thresholds:
```bash
python pyclosewat.py -B input.pdb output.pdb
python pyclosewat.py -X 3.5 -M 2.0 input.pdb output.pdb
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [test_fixtures.py](test_fixtures.py) for example PDB structures
- Check [test_integration.py](test_integration.py) for advanced usage patterns

## Resources

- PDB Format Specification: https://www.wwpdb.org/documentation/file-format
- RCSB PDB Database: https://www.rcsb.org/

---

Happy analyzing!
