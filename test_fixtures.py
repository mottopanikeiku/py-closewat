#!/usr/bin/env python3
"""
Test fixtures and sample PDB data for pyclosewat testing.

This module provides reusable test data including:
- Sample PDB structures
- Known water configurations
- Expected output for validation
"""

# Sample minimal PDB file with protein and waters
SAMPLE_PDB_MINIMAL = """HEADER    TEST PROTEIN                            01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 20.00           O
HETATM  101  O   HOH A 201      15.000  15.000  15.000  1.00 20.00           O
END
"""

# Sample PDB with water conformers
SAMPLE_PDB_CONFORMERS = """HEADER    TEST CONFORMERS                         01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
HETATM  100  O  AHOH A 200      14.000  14.000  14.000  0.50 20.00           O
HETATM  101  O  BHOH A 200      14.100  14.100  14.100  0.50 20.00           O
HETATM  102  O   HOH A 201      15.000  15.000  15.000  1.00 20.00           O
END
"""

# Sample PDB with close water contacts
SAMPLE_PDB_CLOSE_WATERS = """HEADER    TEST CLOSE WATERS                       01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 20.00           O
HETATM  101  O   HOH A 201      14.500  14.500  14.500  1.00 20.00           O
HETATM  102  O   HOH A 202      20.000  20.000  20.000  1.00 20.00           O
END
"""

# Sample PDB with metal coordination
SAMPLE_PDB_METAL = """HEADER    TEST METAL COORDINATION                 01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
HETATM   10 MG   MG  A 100      15.000  15.000  15.000  1.00 20.00          MG
HETATM  100  O   HOH A 200      16.500  15.000  15.000  1.00 20.00           O
HETATM  101  O   HOH A 201      20.000  20.000  20.000  1.00 20.00           O
END
"""

# Sample PDB with multiple chains
SAMPLE_PDB_MULTCHAIN = """HEADER    TEST MULTIPLE CHAINS                    01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
ATOM      5  N   GLY B   1      20.000  20.000  20.000  1.00 10.00           N
ATOM      6  CA  GLY B   1      21.000  21.000  21.000  1.00 10.00           C
ATOM      7  C   GLY B   1      22.000  22.000  22.000  1.00 10.00           C
ATOM      8  O   GLY B   1      23.000  23.000  23.000  1.00 10.00           O
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 20.00           O
HETATM  101  O   HOH B 201      24.000  24.000  24.000  1.00 20.00           O
END
"""

# Sample PDB with high B-factors
SAMPLE_PDB_HIGH_B = """HEADER    TEST HIGH B-FACTORS                     01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 10.00           O
HETATM  101  O   HOH A 201      15.000  15.000  15.000  1.00 50.00           O
HETATM  102  O   HOH A 202      16.000  16.000  16.000  1.00 80.00           O
END
"""

# Sample PDB with various water residue names
SAMPLE_PDB_WATER_NAMES = """HEADER    TEST WATER NAMES                        01-JAN-00   TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 20.00           O
HETATM  101  O   WAT A 201      15.000  15.000  15.000  1.00 20.00           O
HETATM  102  O   H2O A 202      16.000  16.000  16.000  1.00 20.00           O
HETATM  103  O   TIP A 203      17.000  17.000  17.000  1.00 20.00           O
END
"""

# Expected behavior descriptions for each fixture
FIXTURE_EXPECTATIONS = {
    'minimal': {
        'description': 'Basic protein with 2 waters, no special features',
        'expected_waters': 2,
        'expected_protein_atoms': 4,
        'expected_chains': 1,
    },
    'conformers': {
        'description': 'Waters with alternate conformations',
        'expected_waters': 3,
        'expected_conformers': 2,
        'expected_chains': 1,
    },
    'close_waters': {
        'description': 'Waters at varying distances',
        'expected_waters': 3,
        'expected_close_pairs': 1,  # Waters 200 and 201 are close
        'expected_chains': 1,
    },
    'metal': {
        'description': 'Metal ion with coordinating water',
        'expected_waters': 2,
        'expected_metal_coords': 1,
        'expected_chains': 1,
    },
    'multchain': {
        'description': 'Multiple protein chains with waters',
        'expected_waters': 2,
        'expected_chains': 2,
    },
    'high_b': {
        'description': 'Waters with varying B-factors',
        'expected_waters': 3,
        'expected_high_b_waters': 2,  # B > 40
        'expected_chains': 1,
    },
    'water_names': {
        'description': 'Various water residue names',
        'expected_waters': 4,
        'expected_chains': 1,
    },
}

# Known coordinate test cases
KNOWN_DISTANCES = [
    {
        'name': 'orthogonal_3_4_5',
        'point1': (0.0, 0.0, 0.0),
        'point2': (3.0, 4.0, 0.0),
        'distance_squared': 25.0,
        'distance': 5.0,
    },
    {
        'name': 'unit_cube_diagonal',
        'point1': (0.0, 0.0, 0.0),
        'point2': (1.0, 1.0, 1.0),
        'distance_squared': 3.0,
        'distance': 1.732,
    },
    {
        'name': 'typical_hbond',
        'point1': (0.0, 0.0, 0.0),
        'point2': (2.8, 0.0, 0.0),
        'distance_squared': 7.84,
        'distance': 2.8,
    },
    {
        'name': 'close_contact',
        'point1': (0.0, 0.0, 0.0),
        'point2': (2.0, 0.0, 0.0),
        'distance_squared': 4.0,
        'distance': 2.0,
    },
]

# Metal atoms for testing
METAL_ATOMS = ['FE', 'MG', 'CA', 'ZN', 'MN', 'CU', 'NI', 'CO']
NON_METAL_ATOMS = ['C', 'N', 'O', 'S', 'P', 'H']

# Water residue names that should be recognized
WATER_RESIDUE_NAMES = ['HOH', 'WAT', 'H2O', 'D2O', 'TIP', 'TIP3', 'TIP4', 'TIP5', 'SPC', 'OPC', 'OPC3']
NON_WATER_RESIDUE_NAMES = ['ALA', 'GLY', 'SER', 'THR', 'VAL', 'LEU', 'ILE', 'MET', 'PRO']

def get_fixture(name):
    """Get a test fixture by name"""
    fixtures = {
        'minimal': SAMPLE_PDB_MINIMAL,
        'conformers': SAMPLE_PDB_CONFORMERS,
        'close_waters': SAMPLE_PDB_CLOSE_WATERS,
        'metal': SAMPLE_PDB_METAL,
        'multchain': SAMPLE_PDB_MULTCHAIN,
        'high_b': SAMPLE_PDB_HIGH_B,
        'water_names': SAMPLE_PDB_WATER_NAMES,
    }
    return fixtures.get(name, '')

def get_expectations(name):
    """Get expected behavior for a fixture"""
    return FIXTURE_EXPECTATIONS.get(name, {})

