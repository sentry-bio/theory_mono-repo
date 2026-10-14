# PREREG19 — Test B results (run 2026-10-08 23:30–23:34 UTC on biosphereatlas; hashes in results/run.log; scored
# by the registered rules; 96 cells in results/testB_cells.jsonl)

## Verdicts
B1 (mean decided accuracy over 3 seeds; Δ = acc(800k) − acc(50k)):

| gen | D | 50k | 100k | 200k | 400k | 800k | Δ | B1 |
|---|---|---|---|---|---|---|---|---|
| G gamma rates | 1.0 | 0.9974 | 0.9994 | 0.9999 | 0.9998 | 1.0000 | +0.003 | RECOVERS |
| G | 2.0 | 0.9918 | 0.9974 | 0.9998 | 0.9998 | 1.0000 | +0.008 | RECOVERS |
| H skewed composition | 1.0 | 0.9962 | 0.9991 | 0.9996 | 0.9997 | 1.0000 | +0.004 | RECOVERS |
| H | 2.0 | 0.9720 | 0.9859 | 0.9950 | 0.9992 | 0.9994 | +0.027 | RECOVERS |
| T heterotachy | 1.0 | 0.9113 | 0.9191 | 0.9244 | 0.9263 | 0.9272 | +0.016 | INDETERMINATE |
| T | 2.0 | 0.8917 | 0.8962 | 0.9067 | 0.9205 | 0.9372 | +0.046 | RECOVERS |

- **B2: INCONCLUSIVE.** Five pairs recover; heterotachy at D = 1.0 is neither a floor (Δ ≥ 0.005) nor a recovery
  (Δ < 0.02 and acc < 0.98).
- **B3: DISCRIMINATOR WORKS by the registered letter.** C* mean p_major = 0.61 (3 seeds × 200 wrong quartets; the
  rule asked ≤ 0.85). The misspecified half is vacuous: nothing floored.
- B4 (reported): undecidable fraction 0 for G, H and C*; for T 0–0.007 at D = 1.0 and 0.34–0.39 → 0.19 (50k → 800k)
  at D = 2.0. Block witness 247 / 254 (D = 1.0 / 2.0) for G and H, 249 / 255 for T, 250–253 for C*: Test C's upward
  drift reproduced in sign.
- Reference C*: decided accuracy 0.857–0.865 at 200k and 0.857–0.864 at 800k (79–81 transfer events) — Test C's
  floor, reproduced on the frozen instrument.

## Checks that the run was right
- The disclosed smoke test (32-tip tree) passed before any registered cell; the heterotachy clades are nodes 506
  and 496 in every seed, chosen from the tree alone as registered.
- Seeds agree where it matters: T at D = 1.0, L = 800k: 0.9267 / 0.9280 / 0.9270.
- 0.8–23 s per cell; 96 cells = 90 registered + 6 reference.

## Readings (separate from the verdicts)
1. Specificity is not established. Gamma rates and skewed composition do not floor. Heterotachy at the shallower
   depth gives a near-floor that rises 0.911 → 0.927 over 16× in sites: faster than Test C's floors (< 0.005),
   slower than Test A's recoveries (≥ 0.04). The L-recovery curve alone does not separate a second history from
   long-branch attraction at this depth; v3.5 §3's reading of the Atlas floor as mixing cannot rest on the floor
   alone.
2. The window-vote discriminator passes by its letter and fails in substance. Its registered prediction for the
   misspecified side (uniform bias ⇒ p_major ≥ 0.95) is contradicted by the reported values: heterotachy's wrong
   quartets split their windows 0.57 / 0.51 (D = 1.0 / 2.0), the same as mixing's 0.61. Had T at D = 1.0 been scored
   FLOOR, B3 would have failed. p_major measures the decision margin of a wrong quartet, not whether the error is
   carried by blocks of sites; a near-tied quartet splits its windows whatever the cause.
3. What separates the cases in Test C is donor-topology agreement (98.7% of wrong quartets voted the donor topology
   against 52.3% under vertical noise), which needs a donor hypothesis. The honest two-part diagnostic for real
   data is: a floor plus agreement with a named second history, or a block-structure statistic scored against a
   site-permutation null (PREREG19b, registered below, not yet run).
4. For EAG v4 §3: "a floor is the signature of mixing" becomes "a floor is consistent with mixing and with
   heterotachy; mixing is identified by donor-topology agreement (Test C) and, if PREREG19b passes, by block
   structure against a permutation null".

## PREREG19b — registered 2026-10-09 before any permutation statistic was computed (design; run pending)
Cells: C* and T at D ∈ {1.0, 2.0}, L = 800,000, seeds 0–2 (the registered seeds; sequences regenerated
deterministically). For each quartet decided wrongly at full length (≤ 200 per cell): the dispersion of the
per-window four-point margin across 20 windows of 40,000 sites, compared with the same statistic after permuting
site columns across windows (200 permutations; the null of exchangeable sites). A quartet is BLOCKED if its observed
dispersion exceeds the permutation 95th percentile.
- Prediction: under C*, ≥ 70% of wrong quartets are BLOCKED (transferred sites arrive in segments); under T, ≤ 30%
  (heterotachy's site classes are drawn per site and are exchangeable across windows).
- Verdict: BLOCK DISCRIMINATOR WORKS if both hold at both depths; FAILS if either bound is violated at either depth.
- This replaces B3's p_major as the proposed second part of the diagnostic. It is registered here, in the results
  file of the run that motivated it, so that the dependence is on record.

Amendment, 2026-10-09 ≈01:58 CEST (before the 02:01:02 CEST launch recorded in perm_run.log; the clock time first
written here, 02:40, was mis-stated and is corrected to the launch log), before any PREREG19b statistic was computed. The per-window margin is made
additive over sites so that the exchangeable-sites null is exact: for a quartet decided wrongly at full length by the
registered reader (JC four-point), the wrong topology W it chose and the true topology T define a per-site
contribution m_s = δ_T(s) − δ_W(s), where δ_X(s) is the mismatch indicator of the pair-sum of split X at site s
(raw mismatches, not JC-corrected; the reader's decision is still the registered one). The window margin is
Σ_{s ∈ window} m_s over 20 contiguous windows of 40,000 sites. Under exchangeable sites the across-window variance
has the hypergeometric value Var_null = w·σ²(m)·(1 − w/L)·L/(L − 1); the statistic is φ = Var_obs/Var_null and a quartet
is BLOCKED if φ > 1.586 (the 95th percentile of χ²₁₉/19), which is the permutation test's 95th percentile computed
exactly instead of by 200 permutations. Predictions and verdict unchanged: C* ≥ 70% BLOCKED, T ≤ 30%, both depths.
Correction, ≈02:00 CEST (testB_perm.py written 02:00:31, launch 02:01:02; the time first written here, 02:55, was
mis-stated), still before any statistic: Var_null carries the partition factor K/(K − 1) = 20/19 (the
20 windows partition the sites, so the across-window sample variance has expectation K/(K − 1) times the single-window
hypergeometric variance); with it, φ ~ χ²₁₉/19 under the null and the 1.586 threshold is right. testB_perm.py
implements this; its hash is in perm_run.log at launch.

### PREREG19b result (run 2026-10-09 02:01–02:03 CEST, local; hashes in perm_run.log; cells in testB_perm.jsonl)
| cell | wrong quartets scored | BLOCKED fraction | median φ |
|---|---|---|---|
| C* D = 1.0 | 600 (3 × 200) | 1.000 | 880 |
| C* D = 2.0 | 600 | 0.942 | 208 |
| T D = 1.0 | 600 | 0.045 | 0.94 |
| T D = 2.0 | 489 | 0.064 | 0.97 |
**Verdict: BLOCK DISCRIMINATOR WORKS** (C* ≥ 0.70 and T ≤ 0.30 at both depths, as registered). Readings: under
mixing the wrong quartets' window margins are hundreds of null variances apart (the transferred 240,000-site
segments sit in whole windows); under heterotachy they are exactly on the exchangeable-sites null (φ ≈ 0.95, and
4–6% exceed the 95th percentile, the nominal rate). The two-part diagnostic for real data is therefore: a floor in
the L-recovery curve, plus block structure of the wrong quartets against the site-permutation null; p_major is
withdrawn. Caveat stated now: the transferred segments here are long (30% of the genome); shorter transfers
(below the 40,000-site window) would lower φ, and the window length is a parameter the real-data registration must
set from the expected segment length.
