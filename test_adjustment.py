"""Exercise the unchanged C adjustment routine directly, including rounding edges."""
import subprocess

import pytest

import pyclosewat as pc
from tools.compare_reference import ROOT


@pytest.fixture(scope="module")
def adjustment_oracle(tmp_path_factory):
    work = tmp_path_factory.mktemp("adjustment-oracle")
    source = work / "oracle.c"
    source.write_text('''#define main closewat_cli_main
#include "closewat.c"
#undef main
int main(int argc, char **argv) {
    TOTALST top = {0};
    PDBRECORD waters[4] = {0};
    int n = atoi(argv[1]);
    top.tpwa = waters; top.tpwap = waters + n;
    for (int i = 0; i < n; i++) {
        waters[i].p_nconfs = n;
        waters[i].p_conf = 'A' + i;
        waters[i].p_occo = waters[i].p_occ = atof(argv[2 + 2*i]);
        waters[i].p_bvo = waters[i].p_bval = atof(argv[3 + 2*i]);
    }
    adjustqb(&top, waters);
    for (int i = 0; i < n; i++)
        printf("%c %.12f %.12f\\n", waters[i].p_conf, waters[i].p_occ, waters[i].p_bval);
    return 0;
}
''')
    executable = work / "oracle"
    subprocess.run(["gcc", "-std=c99", "-O0", "-I", str(ROOT), str(source),
                    "-lm", "-o", str(executable)], check=True, timeout=60)
    return executable


@pytest.mark.parametrize("originals", [
    [(1.0, 10.0), (1.0, 10.0)],
    [(0.3, 10.0), (0.8, 40.0)],
    [(0.0, 0.0), (0.0, 0.0)],
    [(0.01, 0.0), (0.02, 1.0)],
    [(1.0, 150.0), (1.0, 180.0)],
    [(1.0, 10.0)] * 3,
    [(0.2, 8.0), (0.3, 20.0), (0.4, 40.0)],
    [(0.1, 4.0), (0.2, 8.0), (0.3, 12.0), (0.4, 16.0)],
])
def test_adjustqb_matches_c(originals, adjustment_oracle):
    command = [str(adjustment_oracle), str(len(originals))]
    command += [str(value) for pair in originals for value in pair]
    result = subprocess.run(command, check=True, capture_output=True, text=True, timeout=10)
    expected = [line.split() for line in result.stdout.splitlines()]
    top = pc.TotalSt()
    for i, (q, b) in enumerate(originals):
        water = pc.PDBRecord()
        water.p_conf = chr(ord('A') + i)
        water.p_nconfs = len(originals)
        water.p_occo = water.p_occ = q
        water.p_bvo = water.p_bval = b
        top.tpwa.append(water)
    top.tpwap = len(originals)
    pc.adjustqb(top, top.tpwa[0])
    for water, (conf, q, b) in zip(top.tpwa, expected):
        assert water.p_conf == conf
        # C stores Q/B in float32; Python uses float64. Check the equations
        # within storage precision AND require exact agreement at PDB precision.
        assert water.p_occ == pytest.approx(float(q), rel=1e-6, abs=1e-7)
        assert water.p_bval == pytest.approx(float(b), rel=1e-6, abs=1e-7)
        assert f"{water.p_occ:.2f}" == f"{float(q):.2f}"
        assert f"{water.p_bval:.2f}" == f"{float(b):.2f}"
