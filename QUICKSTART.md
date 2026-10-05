# Single-file usage

This Python port builds on the included [`closewat.c`](closewat.c). Its outputs differ from C; read the [measured comparison](README.md#result) before using adjusted occupancies or B-factors.

The CLI needs Python's standard library only. Run from a temporary directory so the new `closewat.log` does not overwrite the example log in the repository:

```bash
mkdir -p /tmp/closewat-example
(cd /tmp/closewat-example && nice -n 19 python /path/to/py-closewat/pyclosewat.py /path/to/py-closewat/1IR0.pdb waters.pdb)
```

Replace `/path/to/py-closewat` with your checkout path. `waters.pdb` contains only the output water records, not the whole input structure. `closewat.log` contains contact diagnostics and summary counts. The residue numbers, occupancies and B-factors can change; these are algorithm outputs, not new experimental measurements.

To view the available flags:

```bash
python pyclosewat.py --help
```

`-S` requests a single water chain, `-H` requests high-B occupancy adjustment, and `-B` enables bump handling. `-X`, `-M`, `-L`, and `-O` set distance thresholds. The reference comparison currently covers default options only, not these flags. Do not treat automatic adjustments as validated structural refinement.

The [README](README.md#reproduce) gives the offline test and reference-comparison commands. The original integration tests exercise portions of the Python pipeline; `test_reference.py` runs the complete C and Python CLIs and checks their saved outputs, including documented disagreements.
