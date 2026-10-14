# PREREG19 — Test B: can the L-recovery diagnostic tell a second history from a wrong model? (registered 2026-10-09,
# before any cell ran)

## Why this gate exists
v3.5 §3 reads a non-recovering floor in decided-quartet accuracy as the signature of mixing (a second history on the
same tape, Test C), and a recovering curve as poverty (Test A). The reading is trusted on real data only if a wrong
substitution model with NO transfer does not also floor. v3.5 §6 names this as Test B, unrun. Known theory makes
the outcome genuinely uncertain: distance methods under a misspecified model are inconsistent in parts of parameter
space (the Felsenstein zone; heterotachy, Kolaczkowski–Thornton 2004), so floors from a wrong model are possible.
Either outcome is informative: a pass licenses the diagnostic as it stands; a fail says the floor alone does not
identify mixing and names the discriminator that would.

## Instrument (identical to Tests A and C; frozen copies in this folder)
Yule tree, 256 tips, seed 42, rescaled to mean root-to-tip depth D (sim_core.py); 3,000 quartets, seed 7
(measures.sample_quartets); reader = JC-corrected Hamming distances and the four-point method, saturated pairs
(p ≥ 0.749999) excluded as undecidable (measures.jc_correct, quartet_accuracy); block witness at ε = 0.01
(measures.block_capacity). Outcomes per cell: accuracy of decided quartets, fraction undecidable, block witness.

## Generators (no transfer in any of them; the reader always assumes JC69)
- G (gamma rates): JC69 with per-site rate r_s ~ Gamma(shape 0.5, mean 1).
- H (base composition): HKY85 with equilibrium frequencies (A, C, G, T) = (0.15, 0.35, 0.35, 0.15) and
  transition/transversion ratio κ = 4; branch lengths scaled to mean one substitution per site per unit length.
- T (heterotachy): JC69 with two site classes of equal size; class-1 sites evolve 4× faster on the branches inside
  clade A, class-2 sites 4× faster inside clade B, where A and B are the two largest disjoint clades with ≤ 64 tips
  each in the seed-42 tree (chosen by the generator from the tree alone; identities recorded).
- C* (reference): Test C's mixing cell, transfer rate f = 0.30, transfer fraction 0.30 (hgt_core.apply_hgt), at D = 1.0
  only, for the discriminator's calibration. Not scored under B1.

Cells: generator ∈ {G, H, T} × D ∈ {1.0, 2.0} × L ∈ {50,000, 100,000, 200,000, 400,000, 800,000} × seeds {0, 1, 2}
(90 cells), plus C* × L ∈ {200,000, 800,000} × 3 seeds.

## Rules
- B1 (floor per generator and depth): with acc(L) = mean decided accuracy over seeds, Δ = acc(800k) − acc(50k).
  RECOVERS if Δ ≥ 0.02 or acc(800k) ≥ 0.98; FLOOR if Δ < 0.005 and acc(800k) < 0.98; otherwise INDETERMINATE.
  (Test C's floors moved < 0.005 over the same 16× range; Test A's recoveries moved ≥ 0.04.)
- B2 (primary verdict): DIAGNOSTIC SPECIFIC if all six (generator, D) pairs RECOVER; NOT SPECIFIC if any FLOORS;
  INCONCLUSIVE otherwise. This is v3.5's kill line, stated as a pass/fail.
- B3 (the discriminator the frame predicts, registered now, scored separately): mixing writes a second history in
  *blocks*; a wrong model biases every site the same way. For every quartet decided wrongly at L = 800,000, split
  the alignment into 20 windows of 40,000 sites, resolve the quartet in each window, and record the fraction of
  windows voting the quartet's majority topology (p_major). Prediction: under C*, mean p_major ≤ 0.85 (the
  transferred 30% votes the donor); under any floored misspecified generator, mean p_major ≥ 0.95 (uniform bias).
  DISCRIMINATOR WORKS if both hold (vacuously true on the misspecified side if nothing floors, in which case only the
  C* half is informative and is reported as such).
- B4 (reported): fraction undecidable and block witness per cell; Test C's signature was undecidable = 0 and
  witness drifting up (247 → 254). A floored misspecified generator with the same signature would show that these
  two statistics do not separate the cases either.

## Predictions stated before the run
G at D = 1.0 recovers; G at D = 2.0 is uncertain (rate heterogeneity biases JC distances nonlinearly). H at both
depths floors mildly, if at all (skewed composition lowers the saturation plateau). T floors at both depths: this is
the long-branch-attraction generator and the reason the test exists. If T floors and B3 separates it from C*, the
diagnostic for real data becomes two-part (recovery and block structure), which is what EAG v4 will state.

## Seeds and reproducibility
Sequence seeds: generator G 100 + seed, H 200 + seed, T 300 + seed, C* vertical 0 + seed with transfer seed 1000 +
seed (Test C's). Trees and quartets are deterministic from their seeds. Every per-cell result is written as a JSON
line as it finishes.

## Frozen files (sha256 recorded in run.log at launch)
sim_core.py, measures.py, hgt_core.py (unchanged from Zenodo_v2), misspec_core.py, testB_run.py, testB_score.py.

## Caveats stated in advance
One Yule tree and one quartet sample, as in Tests A and C; the floors found there are specific to that tree, and so
would be any found here. The Δ thresholds inherit Test A/C's empirical scale; a generator whose Δ falls between
0.005 and 0.02 is INDETERMINATE, not a pass. HKY's reader bias depends on π; the chosen skew is moderate, not extreme.

## Amendment before any registered cell — 2026-10-08 23:20 UTC
The disclosed smoke test (32-tip tree) failed in the heterotachy generator: its clade picker used an absolute 64-tip
cap, which on a 32-tip tree admits the root and leaves no disjoint second clade. The cap is now n_tips/4, which is 64
on the registered 256-tip tree, so generator T's registered definition ("two largest disjoint clades with ≤ 64 tips")
is unchanged. No registered cell had run (the runner stops on a smoke failure). misspec_core.py's hash changes; the
new hash is in run.log at relaunch.
