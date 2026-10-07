# C/Python reference comparison

## Result and scope
I replaced machine-specific executable paths in saved Python log headings with `pyclosewat.py`; the recorded PDB outputs and comparison values are unchanged.


I compared complete default CLI outputs on the four bundled X-ray structures before and after fixing the port. A water matches only if every parsed PDB field agrees after alignment by original atom serial. I score output order and byte equality separately; neither can be inferred from matching counts.

| Input | Waters | Matching records before | Matching records after | Remaining number / occupancy / B differences |
|---|---:|---:|---:|---|
| 1IR0 | 129 | 0 | 121 | 8 / 0 / 0 |
| 1UBQ | 58 | 0 | 58 | 0 / 0 / 0 |
| 1CTF | 62 | 0 | 62 | 0 / 0 / 0 |
| 2CI2 | 64 | 0 | 64 | 0 / 0 / 0 |

The [summary](../results/parity/summary.json) records 0/313 → 305/313 (97.44%) matching waters and 0/4 → 3/4 ordered parsed outputs. There are no missing or extra serials. All 12 occupancy and 16 B-factor disagreements are removed. Byte equality is still 0/4: Python left-aligns the stripped atom name where C right-aligns it. Logs and diagnostic classifications are not equivalent by this test.

## Isolated causes

Before changing the algorithm, I extracted [four real pairs](../tests/data/reproducers/). Each contains two original water records, the nearest non-water atom to the predominant conformer, and an atom preserving the maximum residue number of that chain. [sources.json](../tests/data/reproducers/sources.json) identifies the input and serials. No coordinates, occupancies, or B-factors were edited.

The [before](../results/parity/reproducers/before/comparison.json) and [after](../results/parity/reproducers/after/comparison.json) comparisons show the same Q/B differences in these small inputs and their removal after the fix:

- 1IR0: serials 693/753 isolated the B-factor difference (C 9.54, Python 8.35).
- 1UBQ: serials 641/649 isolated occupancy 0.35/0.65 versus 0.34/0.66 and B 25.44 versus 20.90.
- 1CTF: serials 524/544 isolated occupancy 0.57/0.43 versus 0.58/0.42.
- 2CI2: serials 527/541 isolated occupancy 0.37/0.63 versus 0.32/0.68 and B 12.76 versus 10.61.

The numbering implementation started every chain at 1, numbered paired conformers independently, and did not apply C's multiple-conformer ordering or 10-residue gap. I now retain the largest non-water residue per chain, start at the next hundred plus one, assign a group using its predominant conformer, and reorder/renumber multiple conformers as C does.

The old `adjustmult()` only renumbered records and never called `adjustqb()`. Its unused adjustment routine averaged already-modified B-factors and forced equal occupancies. I replaced that with the C equations: use original occupancy and B-factor, floor original B at 2, weight occupancy by inverse B, scale the minimum original B according to occupancy and weighted spread, and correct two-decimal occupancy sums. [test_adjustment.py](../test_adjustment.py) directly invokes the unchanged C routine for pairs, triples, quads, zero occupancy, small B, large B, and rounding cases.

The eight remaining 1IR0 numbering differences form four tied pairs: 671/678 (B=6.72), 653/702 (11.29), 732/739 (14.44), and 690/733 (15.80), each with identical occupancy and no conformer. C's `occbsort()` returns +1 in both comparison directions for equal Q/B. That is not a consistent ordering relation; this run's C sort reverses each pair relative to Python. I did not invent a tie-breaker and call it portable C behavior. Non-equivalence remains explicit.

## Reproduce

`tools/compare_reference.py` compiles the bundled, unchanged C with `gcc -std=c99 -O0 closewat.c -lm`. Each complete CLI runs in its own temporary directory with default options and a subprocess timeout. Full PDB outputs, stdout, stderr, and logs are retained in [before](../results/parity/before/) and [after](../results/parity/after/). The earlier [reference results](../results/reference/) remain unchanged.

```bash
python tools/compare_reference.py --output /tmp/closewat-comparison
python tools/compare_reference.py --reproducers --output /tmp/closewat-pairs
python tools/report_parity.py
```

The summary command reads the committed before/after comparisons. `test_reference.py` runs both CLIs again, checks complete saved outputs and the difference report, and checks preservation of input water serials and positions. Missing GCC or a failed C process is a test failure. Passing these tests asserts the recorded scope, not parity on unseen inputs. No timing, scientific accuracy, nondefault-option, or native refinement claim follows.

## Inputs and attribution

`1IR0.pdb` was already bundled. The full additional inputs came from the free RCSB service: [1UBQ](https://files.rcsb.org/download/1UBQ.pdb), [1CTF](https://files.rcsb.org/download/1CTF.pdb), and [2CI2](https://files.rcsb.org/download/2CI2.pdb). Their headers specify X-ray diffraction and retain depositor/publication credits. Input SHA-256 values are pinned in the reports; tests are offline.

The C file has no author/license notice. Its earliest recorded repository commit is `095ded4` (2025-04-25, “All files done”), without upstream attribution. I assign no license or author to it. Identifying its original source and confirming redistribution terms remains open for the owner.

The existing 844-row metadata/water-count CSV is unchanged and is not the parity dataset. Batch fetching and plotting were not rerun. The next useful compatibility work is an explicit tie policy, then separate tests for nondefault flags and higher-order grouping; I make no claim that those already match.
