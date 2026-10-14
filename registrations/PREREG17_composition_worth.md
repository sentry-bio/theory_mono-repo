# PREREG17 — what a composition reader is worth, in aligned sites (registered 2026-10-09, before any registered simulation ran)

## One claim, one verdict
PREREG16's composition rules (W4, W5) failed on *level* and were then derived exactly post hoc with nothing fitted.
This registration states the derived claim as predictions on NEW seeds and NEW cells, so it can pass or fail on its own:

**A composition reader's signal-to-noise on a deep quartet is a closed-form function of the substitution rate and the
tree alone — bounded, independent of genome length, and decaying toward the letter-count value with depth; and the
letter-count value exceeds "one aligned site" exactly where the medium sits above the Kesten–Stigum line.**

Nothing here is new mathematics: the predictions are second-moment (Isserlis) identities under Jukes–Cantor on the
PREREG15/16 quartet. The claim is that they hold at the registered tolerances on an independent run.

## Design (identical process and tree to PREREG15/16)
JC69, uniform iid root; deep quartet ((A,B),(C,D)) of complete binary clades of height h, every edge length t,
x = 2λ², λ = e^{−4t/3}. Readers on the same replicate trees:
- letter-count reader: clade census of per-leaf letter counts, margin M₁;
- 4-mer reader: PREREG3's R2 std4 (overlapping 4-mers, centred at (L−3)/256, scaled by √), clade census, margin M₄;
- aligned census (per-site margin), to express worth in sites: r = E[M]/sd_site, with E[M] from PREREG15's closed form.
Cells: x ∈ {0.8, 1.0, 1.25, 1.5}, h ∈ {1, 2, 3, 4, 6}, L ∈ {5,000, 40,000}. Replicates R = 4,000 in every rule cell,
1,500 in report-only cells. Seeds: 37000 + 100·h + round(100·x) + L/1000 (new; PREREG16 used 26000 + …).

## Predictions, computed before the run from the closed form (zero fitted parameters)
z = mean/sd of the margin across replicates under Gaussian pairing. z₁ is the large-L limit for letter counts; z₄ is
the 4-mer reader's value. "share" = fraction of the 4-mer mean carried by mode j = 1 (the letter-count mode).

| x | h | z₁ | z₄ | z₄/z₁ | share j = 1 | reps for z₄ ≥ 4/√R |
|---|---|---|---|---|---|---|
| 0.8 | 1 | 0.169 | 0.171 | 1.01 | 0.37 | 550 |
| 0.8 | 2 | 0.104 | 0.073 | 0.70 | 0.65 | 2,989 |
| 0.8 | 3 | 0.071 | 0.043 | 0.62 | 0.83 | 8,510 |
| 0.8 | 4 | 0.050 | 0.030 | 0.60 | 0.93 | 17,711 |
| 0.8 | 6 | 0.028 | 0.017 | 0.62 | 0.99 | 54,260 |
| 1.0 | 1 | 0.220 | 0.337 | 1.54 | 0.23 | 141 |
| 1.0 | 2 | 0.154 | 0.157 | 1.02 | 0.43 | 651 |
| 1.0 | 3 | 0.118 | 0.098 | 0.83 | 0.64 | 1,676 |
| 1.0 | 4 | 0.096 | 0.073 | 0.76 | 0.79 | 3,001 |
| 1.0 | 6 | 0.070 | 0.053 | 0.76 | 0.94 | 5,670 |
| 1.25 | 1 | 0.278 | 0.713 | 2.57 | 0.12 | 32 |
| 1.25 | 2 | 0.215 | 0.386 | 1.79 | 0.22 | 108 |
| 1.25 | 3 | 0.182 | 0.255 | 1.40 | 0.36 | 247 |
| 1.25 | 4 | 0.162 | 0.194 | 1.20 | 0.50 | 425 |
| 1.25 | 6 | 0.140 | 0.146 | 1.04 | 0.75 | 750 |
| 1.5 | 1 | 0.330 | 1.340 | 4.06 | 0.06 | 9 |
| 1.5 | 2 | 0.274 | 0.879 | 3.22 | 0.10 | 21 |
| 1.5 | 3 | 0.245 | 0.653 | 2.66 | 0.15 | 38 |
| 1.5 | 4 | 0.230 | 0.524 | 2.29 | 0.22 | 59 |
| 1.5 | 6 | 0.214 | 0.389 | 1.82 | 0.39 | 106 |

Rule cells (power: reps needed ≤ 4,000 and h ≥ 2): (0.8, 2); (1.0, 2), (1.0, 3), (1.0, 4); (1.25, 2–6); (1.5, 2–6) —
12 (x, h) pairs, 24 cells over L. Everything else is reported, not scored. The h = 1 cells are the shallow,
non-Gaussian corner (PREREG16's named miss) and are excluded from every rule by design, not after the fact.

Letter-count worth in sites, L_eff,1 = Var_site / P, is NOT closed-form (Var_site is a fourth moment); its registered
prediction is PREREG15's own measured Var_site/P at the same (x, h) (posthoc_gaussianity_P15.json, an independent
earlier run), copied here from that file: x = 0.8: 1.13 (h 2), 1.09 (3), 1.04 (4), 1.03 (6); x = 1.0: 1.24, 1.18,
1.13, 1.09; x = 1.25: 1.47, 1.38, 1.33, 1.25; x = 1.5: 1.95, 1.82, 1.74, 1.66. (A first draft of this paragraph,
written minutes earlier and before any run, had transcribed the post-hoc prose's deep-h plateau values instead; it
was replaced with the file's per-cell values on re-reading the file. No simulation had run.)

## Rules
- C1 (4-mer closed form): |z₄_meas − z₄_pred| ≤ 3/√R in ≥ 22 of 24 rule cells and ≤ 5/√R in all 24.
- C2 (length independence): z₄(40k)/z₄(5k) ∈ [0.8, 1.25] in ≥ 10 of 12 rule pairs; L_eff,1(40k)/L_eff,1(5k) ∈ [0.8, 1.25]
  in ≥ 10 of 12.
- C3 (decay toward the letter-count value): at L = 40k and x ∈ {1.25, 1.5}, measured z₄/z₁ is strictly decreasing in
  h over {2, 3, 4, 6}, allowing one inversion smaller than 2 SE; at x = 1.0 over {2, 3, 4}, likewise.
- C4 (the letter-count level is the horizon): L_eff,1 at L = 40k within ±20% of PREREG15's Var_site/P in ≥ 10 of 12
  rule pairs, including every x = 1.5 pair (where the prediction is 1.6, not 1).
- C5 (reported): fraction of replicates in which all leaves' 4-mer vectors are distinct (identity kept).
- Verdict: COMPOSITION WORTH PREDICTED if C1–C4 hold; otherwise NOT PREDICTED, naming the failing rule.

## What a pass licenses in EAG v4
The Atlas paragraph of §3 states what a composition reader is worth in sites, why it cannot carry deep genealogy, and
that its letter-count floor reflects the horizon. It licenses nothing about real genomes beyond the JC/quartet model.

## Caveats stated in advance
- The z₄ prediction is Gaussian at the window level (a CLT over ~L² window pairs); at L = 5k and h = 2 the CLT is
  weakest, which is where C1 is most likely to miss by 3–5 SE.
- A monotone-decay rule with four points has little power against a flat truth; C3's content is the ordering, not
  the slope. Its prediction at x = 0.8 (flat, j = 1 dominant) is reported, not scored, because only (0.8, 2) has power.
- The SE used is 1/√R; the exact SE of a z-statistic is slightly larger (≈ √(1 + z²/2)/√R), which makes C1 stricter,
  not looser.

## Frozen files (sha256 recorded in run.log at launch)
exp1_sim.py, closed_form.py (copied from PREREG16's posthoc_closed_form.py without change), exp1_score.py.

## Disclosed before registration
All numbers in the prediction table were computed from the closed form before any simulation of this registration ran.
No simulation under the new seeds has been run.
