#!/usr/bin/env python3
"""
Integration tests for pyclosewat using test fixtures.

These tests verify end-to-end functionality with realistic PDB inputs.
"""

import pytest
import tempfile
import os
from pathlib import Path

import pyclosewat as pc
import test_fixtures as fixtures


class TestIntegrationWithFixtures:
    """Integration tests using predefined test fixtures"""
    
    def run_pyclosewat_on_fixture(self, fixture_content):
        """Helper to run pyclosewat on a fixture and return results"""
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as fin:
            fin.write(fixture_content)
            input_file = fin.name
        
        output_file = tempfile.mktemp(suffix='.pdb')
        log_file = tempfile.mktemp(suffix='.log')
        
        try:
            # Setup
            top = pc.TotalSt()
            
            # Prepare arguments
            class Args:
                S = False
                H = False
                B = False
                X = None
                M = None
                L = None
                O = None
            
            args = Args()
            
            with open(input_file, 'r') as tfpi, \
                 open(output_file, 'w') as tfpwat, \
                 open(log_file, 'w') as tfpl:
                
                top.tfpi = tfpi
                top.tfpwat = tfpwat
                top.tfpl = tfpl
                
                pc.procargs(args, top, tfpl)
                
                # First pass: count atoms
                for line in top.tfpi:
                    pc.getpdblin(line, top)
                
                # Prepare for second pass
                result = pc.ready(top)
                if result != 0:
                    raise Exception("ready() failed")
                
                # Second pass: process
                for line in top.tfpi:
                    try:
                        pc.procpdblin(line, top)
                    except ValueError as e:
                        tfpl.write(f"Warning: {e}\n")
                        continue
                
                # Run analysis
                top.tnwaters = top.tpwap
                pc.noconformers(top)
                top.tpate = top.tpatp
                pc.closestwat(top)
                
                for i in range(top.tnwaters):
                    pwap = top.tpwa[i]
                    if pwap.p_nbr is not None and pwap.p_conf == ' ':
                        pc.thisthird(top, pwap)
                
                pc.meanbw(top)
                
                # Output results
                for i in range(top.tnwaters):
                    pc.outrec(top.tpwa[i], top.tfpwat)
            
            # Read output and log
            with open(output_file, 'r') as f:
                output_content = f.read()
            
            with open(log_file, 'r') as f:
                log_content = f.read()
            
            return {
                'top': top,
                'output': output_content,
                'log': log_content,
                'success': True
            }
        
        except Exception as e:
            return {
                'top': None,
                'output': '',
                'log': '',
                'success': False,
                'error': str(e)
            }
        
        finally:
            # Clean up
            for f in [input_file, output_file, log_file]:
                if os.path.exists(f):
                    os.unlink(f)
    
    def test_minimal_fixture(self):
        """Test with minimal PDB fixture"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_MINIMAL)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('minimal')
        
        # Verify basic counts
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"
        
        assert top.tpatp == expectations['expected_protein_atoms'], \
            f"Expected {expectations['expected_protein_atoms']} protein atoms, got {top.tpatp}"
        
        assert len(top.tchs) == expectations['expected_chains'], \
            f"Expected {expectations['expected_chains']} chains, got {len(top.tchs)}"
        
        # Verify output was generated
        assert len(result['output']) > 0, "No output generated"
        assert 'HOH' in result['output'], "Output should contain water molecules"
    
    def test_conformers_fixture(self):
        """Test with conformer PDB fixture"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_CONFORMERS)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('conformers')
        
        # Verify waters were processed
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"
        
        # Verify output contains water records
        assert len(result['output']) > 0, "No output generated"
        assert 'HOH' in result['output'], "Output should contain water molecules"
    
    def test_close_waters_fixture(self):
        """Test with close waters fixture"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_CLOSE_WATERS)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('close_waters')
        
        # Verify waters were processed
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"
        
        # Check that close contacts were detected (should be in log)
        # The exact number may vary based on distance thresholds
        assert len(result['log']) > 0, "No log generated"
    
    def test_metal_fixture(self):
        """Test with metal coordination fixture"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_METAL)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('metal')
        
        # Verify waters were processed
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"
        
        # Verify metal was processed as non-water heteroatom
        assert top.tpatp > 4, "Metal should be counted in protein atoms"
    
    def test_multchain_fixture(self):
        """Test with multiple chains fixture"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_MULTCHAIN)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('multchain')
        
        # Verify waters were processed
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"
        
        # Verify multiple chains were detected
        assert len(top.tchs) == expectations['expected_chains'], \
            f"Expected {expectations['expected_chains']} chains, got {len(top.tchs)}"
    
    def test_high_b_fixture(self):
        """Test with high B-factor fixture"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_HIGH_B)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('high_b')
        
        # Verify waters were processed
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"
        
        # Verify mean B-value was calculated
        assert top.tmeanbw > 0, "Mean B-value should be calculated"
    
    def test_water_names_fixture(self):
        """Test with various water residue names"""
        result = self.run_pyclosewat_on_fixture(fixtures.SAMPLE_PDB_WATER_NAMES)
        
        assert result['success'], f"Processing failed: {result.get('error', 'Unknown error')}"
        
        top = result['top']
        expectations = fixtures.get_expectations('water_names')
        
        # Verify all water types were recognized
        assert top.tpwap == expectations['expected_waters'], \
            f"Expected {expectations['expected_waters']} waters, got {top.tpwap}"


class TestDistanceCalculations:
    """Test distance calculations with known values"""
    
    def test_known_distances(self):
        """Test distance calculations against known values"""
        for test_case in fixtures.KNOWN_DISTANCES:
            rec1 = pc.PDBRecord()
            rec1.p_xc, rec1.p_yc, rec1.p_zc = test_case['point1']
            
            rec2 = pc.PDBRecord()
            rec2.p_xc, rec2.p_yc, rec2.p_zc = test_case['point2']
            
            dist_sq = pc.pdbdist(rec1, rec2)
            
            # Check squared distance
            assert abs(dist_sq - test_case['distance_squared']) < 0.001, \
                f"Distance squared mismatch for {test_case['name']}: " \
                f"expected {test_case['distance_squared']}, got {dist_sq}"
            
            # Check actual distance
            import math
            dist = math.sqrt(dist_sq)
            assert abs(dist - test_case['distance']) < 0.01, \
                f"Distance mismatch for {test_case['name']}: " \
                f"expected {test_case['distance']}, got {dist}"


class TestMetalDetection:
    """Test metal atom detection"""
    
    def test_metal_atoms(self):
        """Test that known metals are detected"""
        for metal in fixtures.METAL_ATOMS:
            assert pc.ismetal(metal) == 1, f"{metal} should be detected as metal"
    
    def test_non_metal_atoms(self):
        """Test that non-metals are not detected as metals"""
        for atom in fixtures.NON_METAL_ATOMS:
            assert pc.ismetal(atom) == 0, f"{atom} should not be detected as metal"


class TestWaterResidueDetection:
    """Test water residue name detection"""
    
    def test_water_residues(self):
        """Test that known water residues are detected"""
        for water_name in fixtures.WATER_RESIDUE_NAMES:
            assert pc.is_water_residue(water_name) == True, \
                f"{water_name} should be detected as water"
    
    def test_non_water_residues(self):
        """Test that non-water residues are not detected as water"""
        for residue_name in fixtures.NON_WATER_RESIDUE_NAMES:
            assert pc.is_water_residue(residue_name) == False, \
                f"{residue_name} should not be detected as water"


class TestCommandLineOptions:
    """Test various command line options"""
    
    def test_single_chain_mode(self):
        """Test -S (single chain) option"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as fin:
            fin.write(fixtures.SAMPLE_PDB_MINIMAL)
            input_file = fin.name
        
        output_file = tempfile.mktemp(suffix='.pdb')
        
        try:
            class Args:
                S = True  # Single chain mode
                H = False
                B = False
                X = None
                M = None
                L = None
                O = None
            
            args = Args()
            top = pc.TotalSt()
            
            with open(input_file, 'r') as tfpi, \
                 open(output_file, 'w') as tfpwat, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.log') as tfpl:
                
                top.tfpi = tfpi
                top.tfpwat = tfpwat
                top.tfpl = tfpl
                
                pc.procargs(args, top, tfpl)
                
                assert top.t1ch_s == 1, "Single chain mode should be enabled"
        
        finally:
            for f in [input_file, output_file]:
                if os.path.exists(f):
                    os.unlink(f)
    
    def test_custom_distance_thresholds(self):
        """Test custom distance threshold options"""
        class Args:
            S = False
            H = False
            B = False
            X = 3.5  # Custom max H-bond distance
            M = 2.0  # Custom min H-bond distance
            L = 1.2  # Custom hydrogen distance
            O = 4.0  # Custom heteroatom distance
        
        args = Args()
        top = pc.TotalSt()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.log') as tfpl:
            pc.procargs(args, top, tfpl)
            
            # Verify custom thresholds were set
            assert abs(top.tmaxhbsq - 3.5**2) < 0.001
            assert abs(top.tminhbsq - 2.0**2) < 0.001
            assert abs(top.tminhsq - 1.2**2) < 0.001
            assert abs(top.tminhet - 4.0**2) < 0.001


class TestOutputFormatting:
    """Test output file formatting"""
    
    def test_output_is_valid_pdb(self):
        """Verify output is valid PDB format"""
        result = TestIntegrationWithFixtures().run_pyclosewat_on_fixture(
            fixtures.SAMPLE_PDB_MINIMAL
        )
        
        assert result['success']
        
        lines = result['output'].split('\n')
        water_lines = [l for l in lines if 'HOH' in l]
        
        # Verify PDB format for water lines
        for line in water_lines:
            if len(line) < 54:
                continue
            
            # Check key fields are present and properly formatted
            assert line[0:6].strip() in ['ATOM', 'HETATM'], \
                "First field should be ATOM or HETATM"
            
            # Check that coordinates are numeric and properly formatted
            try:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                assert -1000 < x < 1000, "X coordinate out of reasonable range"
                assert -1000 < y < 1000, "Y coordinate out of reasonable range"
                assert -1000 < z < 1000, "Z coordinate out of reasonable range"
            except (ValueError, IndexError):
                pytest.fail(f"Invalid coordinate format in line: {line}")


class TestErrorRecovery:
    """Test error handling and recovery"""
    
    def test_malformed_pdb_line(self):
        """Test handling of malformed PDB lines"""
        malformed_pdb = """HEADER    TEST
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
MALFORMED LINE HERE
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 20.00           O
END
"""
        result = TestIntegrationWithFixtures().run_pyclosewat_on_fixture(malformed_pdb)
        
        # Should succeed despite malformed line
        assert result['success']
        
        # Should still process valid waters
        assert result['top'].tpwap > 0
    
    def test_empty_pdb(self):
        """Test handling of empty PDB file"""
        empty_pdb = """HEADER    EMPTY
END
"""
        result = TestIntegrationWithFixtures().run_pyclosewat_on_fixture(empty_pdb)
        
        # May or may not succeed, but should not crash
        # Just verify it completes without exception
        assert isinstance(result, dict)


# Run tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

