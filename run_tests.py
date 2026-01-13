#!/usr/bin/env python3
"""
Simple test runner script for py-closewat.

This script provides a convenient way to run tests without needing pytest installed.
It performs basic validation and import tests.
"""

import sys
import os

def test_import():
    """Test that pyclosewat can be imported"""
    print("Testing module import...")
    try:
        import pyclosewat as pc
        print("  [PASS] pyclosewat imported successfully")
        
        # Count public functions/classes
        public_items = [name for name in dir(pc) if not name.startswith('_')]
        print(f"  [PASS] Found {len(public_items)} public functions/classes")
        
        return True
    except ImportError as e:
        print(f"  [FAIL] Failed to import pyclosewat: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without pytest"""
    print("\nTesting basic functionality...")
    try:
        import pyclosewat as pc
        
        # Test PDBRecord creation
        rec = pc.PDBRecord()
        assert rec.p_xc == 0.0, "PDBRecord initialization failed"
        print("  [PASS] PDBRecord creation works")
        
        # Test distance calculation
        rec1 = pc.PDBRecord()
        rec1.p_xc, rec1.p_yc, rec1.p_zc = 0.0, 0.0, 0.0
        rec2 = pc.PDBRecord()
        rec2.p_xc, rec2.p_yc, rec2.p_zc = 3.0, 4.0, 0.0
        dist_sq = pc.pdbdist(rec1, rec2)
        assert abs(dist_sq - 25.0) < 0.001, "Distance calculation failed"
        print("  [PASS] Distance calculation works")
        
        # Test swap
        rec1.p_atnum = 100
        rec2.p_atnum = 200
        pc.swap01(rec1, rec2)
        assert rec1.p_atnum == 200, "Swap failed"
        assert rec2.p_atnum == 100, "Swap failed"
        print("  [PASS] Record swapping works")
        
        # Test water detection
        assert pc.is_water_residue("HOH") == True, "Water detection failed"
        assert pc.is_water_residue("WAT") == True, "Water detection failed"
        assert pc.is_water_residue("ALA") == False, "Water detection failed"
        print("  [PASS] Water residue detection works")
        
        # Test metal detection
        assert pc.ismetal("MG") == 1, "Metal detection failed"
        assert pc.ismetal("FE") == 1, "Metal detection failed"
        assert pc.ismetal("C") == 0, "Metal detection failed"
        print("  [PASS] Metal detection works")
        
        return True
    except Exception as e:
        print(f"  [FAIL] Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdb_parsing():
    """Test PDB line parsing"""
    print("\nTesting PDB parsing...")
    try:
        import pyclosewat as pc
        
        # Test valid ATOM line
        line = "ATOM      1  N   ALA A   1      10.000  20.000  30.000  1.00 10.00           N  "
        rec = pc.PDBRecord()
        pc.strtorec(line, rec)
        
        assert rec.p_rtype == "ATOM", "Record type parsing failed"
        assert rec.p_atnum == 1, "Atom number parsing failed"
        assert rec.p_attype == "N", "Atom type parsing failed"
        assert abs(rec.p_xc - 10.0) < 0.001, "X coordinate parsing failed"
        print("  [PASS] ATOM line parsing works")
        
        # Test water line
        line = "HETATM  100  O   HOH A 200      14.000  15.000  16.000  1.00 20.00           O  "
        rec = pc.PDBRecord()
        pc.strtorec(line, rec)
        
        assert rec.p_rtype == "HETATM", "HETATM parsing failed"
        assert rec.p_resname == "HOH", "Residue name parsing failed"
        print("  [PASS] HETATM line parsing works")
        
        return True
    except Exception as e:
        print(f"  [FAIL] PDB parsing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_test_files():
    """Check if test files exist"""
    print("\nChecking test files...")
    test_files = [
        'test_pyclosewat.py',
        'test_integration.py',
        'test_fixtures.py'
    ]
    
    all_exist = True
    for filename in test_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  [PASS] {filename} exists ({size} bytes)")
        else:
            print(f"  [FAIL] {filename} not found")
            all_exist = False
    
    return all_exist

def check_documentation():
    """Check if documentation files exist"""
    print("\nChecking documentation...")
    doc_files = [
        'README.md',
        'QUICKSTART.md',
        'CHANGELOG.md'
    ]
    
    all_exist = True
    for filename in doc_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  [PASS] {filename} exists ({size} bytes)")
        else:
            print(f"  [FAIL] {filename} not found")
            all_exist = False
    
    return all_exist

def run_pytest_if_available():
    """Try to run pytest if it's available"""
    print("\nChecking for pytest...")
    try:
        import pytest
        print("  [PASS] pytest is installed")
        print("\nRunning pytest...")
        print("=" * 60)
        
        # Run pytest
        exit_code = pytest.main(['-v', '--tb=short'])
        
        print("=" * 60)
        if exit_code == 0:
            print("  [PASS] All pytest tests passed!")
        else:
            print(f"  [WARN] pytest exited with code {exit_code}")
        
        return exit_code == 0
    except ImportError:
        print("  [WARN] pytest not installed (optional)")
        print("    Install with: pip install pytest pytest-cov")
        return None

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("py-closewat Validation Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Import Test", test_import()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("PDB Parsing", test_pdb_parsing()))
    results.append(("Test Files", check_test_files()))
    results.append(("Documentation", check_documentation()))
    
    # Try pytest
    pytest_result = run_pytest_if_available()
    if pytest_result is not None:
        results.append(("pytest", pytest_result))
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "[PASS]" if result else "[FAIL]"
        print(f"{name:.<40} {status}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\nAll validation tests passed!")
        print("py-closewat is ready to use.")
        return 0
    else:
        print(f"\n{total - passed} test(s) failed.")
        print("Please check the error messages above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
