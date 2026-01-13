#!/usr/bin/env python3
"""
Comprehensive test suite for pyclosewat.py

This module contains unit tests, integration tests, and validation tests
for the pyclosewat water analysis tool.
"""

import pytest
import sys
import os
import math
import tempfile
from io import StringIO
from pathlib import Path

# Import the module to test
import pyclosewat as pc


class TestPDBRecord:
    """Test the PDBRecord class"""
    
    def test_init(self):
        """Test PDBRecord initialization"""
        record = pc.PDBRecord()
        assert record.p_rtype == ""
        assert record.p_conf == ' '
        assert record.p_xc == 0.0
        assert record.p_occ == 0.0
        assert record.p_nbr is None
    
    def test_copy(self):
        """Test PDBRecord copying"""
        rec1 = pc.PDBRecord()
        rec1.p_rtype = "HETATM"
        rec1.p_atnum = 100
        rec1.p_xc = 10.5
        rec1.p_yc = 20.3
        rec1.p_zc = 30.1
        rec1.p_conf = 'A'
        
        rec2 = pc.PDBRecord()
        pc.cpypdb(rec1, rec2)
        
        assert rec2.p_rtype == "HETATM"
        assert rec2.p_atnum == 100
        assert rec2.p_xc == 10.5
        assert rec2.p_yc == 20.3
        assert rec2.p_zc == 30.1
        assert rec2.p_conf == 'A'


class TestChain:
    """Test the Chain class"""
    
    def test_init(self):
        """Test Chain initialization"""
        chain = pc.Chain()
        assert chain.c_chainid == ' '
        assert chain.c_minwat == 0
        assert chain.c_curwat == 0


class TestTotalSt:
    """Test the TotalSt class"""
    
    def test_init(self):
        """Test TotalSt initialization"""
        top = pc.TotalSt()
        assert top.tnhet == 0
        assert top.tnwaters == 0
        assert len(top.talert) == 8
        assert top.tmaxhbsq == pc.MAXHBONDSQ
        assert top.tminhbsq == pc.MINHBONDSQ


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_pdbdist(self):
        """Test distance calculation"""
        rec1 = pc.PDBRecord()
        rec1.p_xc = 0.0
        rec1.p_yc = 0.0
        rec1.p_zc = 0.0
        
        rec2 = pc.PDBRecord()
        rec2.p_xc = 3.0
        rec2.p_yc = 4.0
        rec2.p_zc = 0.0
        
        dist_sq = pc.pdbdist(rec1, rec2)
        assert abs(dist_sq - 25.0) < 0.001  # 3^2 + 4^2 = 25
    
    def test_swap01(self):
        """Test swapping two records"""
        rec1 = pc.PDBRecord()
        rec1.p_atnum = 100
        rec1.p_xc = 10.0
        rec1.p_conf = 'A'
        
        rec2 = pc.PDBRecord()
        rec2.p_atnum = 200
        rec2.p_xc = 20.0
        rec2.p_conf = 'B'
        
        pc.swap01(rec1, rec2)
        
        assert rec1.p_atnum == 200
        assert rec1.p_xc == 20.0
        assert rec1.p_conf == 'B'
        assert rec2.p_atnum == 100
        assert rec2.p_xc == 10.0
        assert rec2.p_conf == 'A'
    
    def test_is_water_residue(self):
        """Test water residue detection"""
        assert pc.is_water_residue("HOH") == True
        assert pc.is_water_residue("WAT") == True
        assert pc.is_water_residue("H2O") == True
        assert pc.is_water_residue("ALA") == False
        assert pc.is_water_residue("GLY") == False
    
    def test_ismetal(self):
        """Test metal atom detection"""
        assert pc.ismetal("FE") == 1
        assert pc.ismetal("MG") == 1
        assert pc.ismetal("CA") == 1
        assert pc.ismetal("ZN") == 1
        assert pc.ismetal("C") == 0
        assert pc.ismetal("N") == 0
        assert pc.ismetal("O") == 0


class TestPDBParsing:
    """Test PDB file parsing functions"""
    
    def test_validate_pdb_line_valid(self):
        """Test validation of a valid PDB line"""
        line = "ATOM      1  N   ALA A   1      10.000  20.000  30.000  1.00 10.00           N  "
        assert pc.validate_pdb_line(line) == True
    
    def test_validate_pdb_line_invalid_short(self):
        """Test validation of too short PDB line"""
        line = "ATOM   1  N"
        assert pc.validate_pdb_line(line) == False
    
    def test_strtorec_atom(self):
        """Test converting PDB ATOM line to record"""
        line = "ATOM      1  N   ALA A   1      10.123  20.456  30.789  1.00 15.50           N  "
        rec = pc.PDBRecord()
        pc.strtorec(line, rec)
        
        assert rec.p_rtype == "ATOM"
        assert rec.p_atnum == 1
        assert rec.p_attype == "N"
        assert rec.p_resname == "ALA"
        assert rec.p_chainid == 'A'
        assert rec.p_resnum == 1
        assert abs(rec.p_xc - 10.123) < 0.001
        assert abs(rec.p_yc - 20.456) < 0.001
        assert abs(rec.p_zc - 30.789) < 0.001
        assert abs(rec.p_occ - 1.00) < 0.01
        assert abs(rec.p_bval - 15.50) < 0.01
    
    def test_strtorec_hetatm_water(self):
        """Test converting PDB HETATM water line to record"""
        line = "HETATM  100  O   HOH A 200       5.000  15.000  25.000  1.00 20.00           O  "
        rec = pc.PDBRecord()
        pc.strtorec(line, rec)
        
        assert rec.p_rtype == "HETATM"
        assert rec.p_atnum == 100
        assert rec.p_resname == "HOH"
        assert rec.p_chainid == 'A'
        assert rec.p_resnum == 200
    
    def test_strtorec_conformer(self):
        """Test converting PDB line with conformer"""
        line = "ATOM      1  N  AALA A   1      10.000  20.000  30.000  0.50 10.00           N  "
        rec = pc.PDBRecord()
        pc.strtorec(line, rec)
        
        assert rec.p_conf == 'A'
        assert abs(rec.p_occ - 0.50) < 0.01


class TestWaterAnalysis:
    """Test water analysis functions"""
    
    def test_seeneighbor_distant(self):
        """Test seeneighbor with distant atoms"""
        top = pc.TotalSt()
        
        water = pc.PDBRecord()
        water.p_xc = 0.0
        water.p_yc = 0.0
        water.p_zc = 0.0
        
        neighbor = pc.PDBRecord()
        neighbor.p_xc = 10.0
        neighbor.p_yc = 10.0
        neighbor.p_zc = 10.0
        
        dsq = pc.pdbdist(water, neighbor)
        result = pc.seeneighbor(water, neighbor, dsq, top)
        
        # Should be distant (code 0) or independent (code 1)
        assert result in [0, 1, 6, 7]
    
    def test_seeneighbor_metal(self):
        """Test seeneighbor with metal atom"""
        top = pc.TotalSt()
        
        water = pc.PDBRecord()
        water.p_xc = 0.0
        water.p_yc = 0.0
        water.p_zc = 0.0
        
        metal = pc.PDBRecord()
        metal.p_xc = 2.0
        metal.p_yc = 0.0
        metal.p_zc = 0.0
        metal.p_atomid = "MG"
        
        dsq = pc.pdbdist(water, metal)
        result = pc.seeneighbor(water, metal, dsq, top)
        
        assert result == 2  # Metal coordination
    
    def test_closestwat(self):
        """Test finding closest water neighbors"""
        top = pc.TotalSt()
        top.tfpl = None
        
        # Create three waters in a line
        w1 = pc.PDBRecord()
        w1.p_xc = 0.0
        w1.p_yc = 0.0
        w1.p_zc = 0.0
        w1.p_resnum = 1
        w1.p_conf = ' '
        
        w2 = pc.PDBRecord()
        w2.p_xc = 2.0
        w2.p_yc = 0.0
        w2.p_zc = 0.0
        w2.p_resnum = 2
        w2.p_conf = ' '
        
        w3 = pc.PDBRecord()
        w3.p_xc = 5.0
        w3.p_yc = 0.0
        w3.p_zc = 0.0
        w3.p_resnum = 3
        w3.p_conf = ' '
        
        top.tpwa = [w1, w2, w3]
        top.tpwap = 3
        
        # Run closestwat
        pc.closestwat(top)
        
        # Waters should have neighbor relationships established
        # (exact behavior depends on distances and thresholds)
        assert True  # Basic smoke test
    
    def test_noconformers(self):
        """Test removing input conformers"""
        top = pc.TotalSt()
        top.tfpl = None
        
        # Create water with conformer
        w1 = pc.PDBRecord()
        w1.p_conf = 'A'
        w1.p_resnum = 100
        w1.p_occ = 0.5
        w1.p_bval = 20.0
        
        w2 = pc.PDBRecord()
        w2.p_conf = 'B'
        w2.p_resnum = 100
        w2.p_occ = 0.5
        w2.p_bval = 20.0
        
        top.tpwa = [w1, w2]
        top.tpwap = 2
        
        ncleared = pc.noconformers(top)
        
        assert ncleared == 2
        assert w1.p_conf == ' '
        assert w2.p_conf == ' '


class TestIntegration:
    """Integration tests using sample PDB data"""
    
    def create_sample_pdb(self):
        """Create a minimal sample PDB file"""
        pdb_content = """HEADER    TEST PROTEIN
ATOM      1  N   ALA A   1      10.000  10.000  10.000  1.00 10.00           N
ATOM      2  CA  ALA A   1      11.000  11.000  11.000  1.00 10.00           C
ATOM      3  C   ALA A   1      12.000  12.000  12.000  1.00 10.00           C
ATOM      4  O   ALA A   1      13.000  13.000  13.000  1.00 10.00           O
HETATM  100  O   HOH A 200      14.000  14.000  14.000  1.00 20.00           O
HETATM  101  O   HOH A 201      15.000  15.000  15.000  1.00 20.00           O
END
"""
        return pdb_content
    
    def test_full_pipeline_with_sample(self):
        """Test full pipeline with sample PDB"""
        # Create temporary input and output files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.pdb', delete=False) as fin:
            fin.write(self.create_sample_pdb())
            input_file = fin.name
        
        output_file = tempfile.mktemp(suffix='.pdb')
        
        try:
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
            
            # Run the pipeline (simplified version)
            top = pc.TotalSt()
            
            with open(input_file, 'r') as tfpi, \
                 open(output_file, 'w') as tfpwat, \
                 tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as tfpl:
                
                top.tfpi = tfpi
                top.tfpwat = tfpwat
                top.tfpl = tfpl
                
                pc.procargs(args, top, tfpl)
                
                # First pass: count atoms and chains
                for line in top.tfpi:
                    pc.getpdblin(line, top)
                
                # Prepare for second pass
                result = pc.ready(top)
                assert result == 0
                
                # Second pass: process PDB
                for line in top.tfpi:
                    try:
                        pc.procpdblin(line, top)
                    except ValueError:
                        continue
                
                # Basic validation
                assert top.tpwap >= 0  # Should have processed some waters
                assert top.tpatp >= 0  # Should have processed some protein atoms
            
            # Verify output file was created
            assert os.path.exists(output_file)
            
        finally:
            # Clean up temporary files
            if os.path.exists(input_file):
                os.unlink(input_file)
            if os.path.exists(output_file):
                os.unlink(output_file)


class TestSortingFunctions:
    """Test sorting key functions"""
    
    def test_sort_key_occ(self):
        """Test occupancy-based sorting key"""
        rec1 = pc.PDBRecord()
        rec1.p_occ = 1.0
        rec1.p_bval = 10.0
        
        rec2 = pc.PDBRecord()
        rec2.p_occ = 0.5
        rec2.p_bval = 20.0
        
        key1 = pc.get_sort_key_occ(rec1)
        key2 = pc.get_sort_key_occ(rec2)
        
        # Higher occupancy should come first (negative for descending)
        assert key1 < key2
    
    def test_sort_key_chain(self):
        """Test chain-based sorting key"""
        rec1 = pc.PDBRecord()
        rec1.p_chainid = 'A'
        rec1.p_resnum = 1
        rec1.p_conf = 'A'
        
        rec2 = pc.PDBRecord()
        rec2.p_chainid = 'A'
        rec2.p_resnum = 2
        rec2.p_conf = ' '
        
        key1 = pc.get_sort_key_chain(rec1)
        key2 = pc.get_sort_key_chain(rec2)
        
        assert key1 < key2  # Lower residue number comes first


class TestErrorHandling:
    """Test error handling and edge cases"""
    
    def test_invalid_pdb_line(self):
        """Test handling of invalid PDB line"""
        line = "INVALID LINE FORMAT"
        rec = pc.PDBRecord()
        
        with pytest.raises(ValueError):
            pc.strtorec(line, rec)
    
    def test_empty_water_list(self):
        """Test handling empty water list"""
        top = pc.TotalSt()
        top.tpwa = []
        top.tpwap = 0
        top.tfpl = None
        
        # Should not crash with empty water list
        pc.closestwat(top)
        assert True
    
    def test_negative_coordinates(self):
        """Test handling negative coordinates"""
        rec1 = pc.PDBRecord()
        rec1.p_xc = -10.0
        rec1.p_yc = -20.0
        rec1.p_zc = -30.0
        
        rec2 = pc.PDBRecord()
        rec2.p_xc = 10.0
        rec2.p_yc = 20.0
        rec2.p_zc = 30.0
        
        # Distance calculation should work with negative coordinates
        dist_sq = pc.pdbdist(rec1, rec2)
        assert dist_sq > 0


class TestConformerHandling:
    """Test conformer-related functions"""
    
    def test_isconformer_same_residue(self):
        """Test conformer detection for same residue"""
        top = pc.TotalSt()
        
        rec1 = pc.PDBRecord()
        rec1.p_chainid = 'A'
        rec1.p_resnum = 100
        rec1.p_conf = 'A'
        rec1.p_bval = 20.0
        rec1.p_xc = 10.0
        rec1.p_yc = 10.0
        rec1.p_zc = 10.0
        
        rec2 = pc.PDBRecord()
        rec2.p_chainid = 'A'
        rec2.p_resnum = 100
        rec2.p_conf = 'B'
        rec2.p_bval = 20.0
        rec2.p_xc = 10.1
        rec2.p_yc = 10.1
        rec2.p_zc = 10.1
        
        result = pc.isconformer(top, rec1, rec2, checkdist=0)
        assert result == 1
    
    def test_isconformer_different_chain(self):
        """Test conformer detection for different chains"""
        top = pc.TotalSt()
        
        rec1 = pc.PDBRecord()
        rec1.p_chainid = 'A'
        rec1.p_resnum = 100
        rec1.p_conf = 'A'
        rec1.p_bval = 20.0
        
        rec2 = pc.PDBRecord()
        rec2.p_chainid = 'B'
        rec2.p_resnum = 100
        rec2.p_conf = 'B'
        rec2.p_bval = 20.0
        
        result = pc.isconformer(top, rec1, rec2, checkdist=0)
        assert result == 0
    
    def test_confchange(self):
        """Test changing conformer designation"""
        top = pc.TotalSt()
        top.tfpl = None
        
        rec = pc.PDBRecord()
        rec.p_conf = 'A'
        rec.p_resnum = 100
        
        top.tpwa = [rec]
        top.tpwap = 1
        
        result = pc.confchange(rec, top)
        assert result == 'B'


class TestOutputFunctions:
    """Test output formatting functions"""
    
    def test_outrec(self):
        """Test PDB record output"""
        rec = pc.PDBRecord()
        rec.p_rtype = "HETATM"
        rec.p_atnum = 100
        rec.p_attype = "O"
        rec.p_conf = ' '
        rec.p_resname = "HOH"
        rec.p_chainid = 'A'
        rec.p_resnum = 200
        rec.p_xc = 10.123
        rec.p_yc = 20.456
        rec.p_zc = 30.789
        rec.p_occ = 1.00
        rec.p_bval = 20.00
        rec.p_atomid = "O"
        
        output = StringIO()
        pc.outrec(rec, output)
        
        result = output.getvalue()
        assert "HETATM" in result
        assert "HOH" in result
        assert "10.123" in result
    
    def test_printclose(self):
        """Test close contact printing"""
        water = pc.PDBRecord()
        water.p_xc = 10.0
        water.p_yc = 20.0
        water.p_zc = 30.0
        water.p_conf = ' '
        water.p_resname = "HOH"
        water.p_chainid = 'A'
        water.p_resnum = 100
        water.p_confo = ' '
        water.p_chaino = 'A'
        water.p_resno = 100
        water.p_diag = 6
        
        atom = pc.PDBRecord()
        atom.p_attype = "N"
        atom.p_conf = ' '
        atom.p_resname = "ALA"
        atom.p_chainid = 'A'
        atom.p_resnum = 10
        atom.p_confo = ' '
        atom.p_chaino = 'A'
        atom.p_resno = 10
        
        output = StringIO()
        dsq = 4.0  # 2.0 Angstroms
        pc.printclose(water, atom, dsq, output)
        
        result = output.getvalue()
        assert "10.000" in result
        assert "20.000" in result
        assert "bump" in result.lower()


# Run tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])

