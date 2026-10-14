# PREREG17 — composition's worth, results (run 2026-10-08 23:00–23:40 UTC on biosphereatlas; frozen hashes in
# results/run.log; 40 cells in results/exp1_comp_*.jsonl; scored by exp1_score.py as registered)

## Verdict (registered rules)
- C1 closed-form level: 24/24 rule cells within 3 SE (max 1.68 SE) → PASS.
- C2 length independence: z₄ ratios 40k/5k within [0.8, 1.25] in 9/12 rule cells (rule ≥ 10/12) → **FAIL**;
  L_eff,1 ratios 12/12.
- C3 decay toward the letter-count value with depth (x = 1.0, 1.25, 1.5) → PASS.
- C4 letter-count level = PREREG15's Var_site/P: 12/12 within 20%, all x = 1.5 cells included → PASS.
- C5 identity kept (reported): fraction of distinct tips 1.000 in every cell.
- **Verdict: NOT PREDICTED** (C2 failed; the registration required C1–C4).

## Checks that the analysis was done right
- The three C2 misses are the three rule cells with the smallest z₄: (1.0, 3) ratio 1.32, (1.0, 4) 0.73,
  (1.25, 6) 0.77, at z₄ = 0.05–0.16. At R = 4,000 the SE of z₄ is 0.016, so a ratio of two such cells has a sampling
  SD of 0.2–0.3 at these levels; the ±25% band was tighter than those cells can resolve. The nine cells with
  z₄ ≥ 0.18 all sit within 0.84–1.05. The mean log-ratio over the 12 rule cells is −0.01: no length dependence is
  detectable in either direction.
- C1 already covers both lengths at every cell (24 cells) and passed with margin, so length independence was shown
  at the level the data resolve; C2 as written was a second, weaker test of the same thing with a tolerance the
  registration mis-sized. The verdict stands as registered. A re-registration of C2 with the band scaled to each
  cell's SE is the honest next step; it is not run here.
- Seeds were new (37000 + 100h + round(100x) + L/1000); the closed form had no fitted parameter.

## Readings (separate from the verdict)
- PREREG16's closed form (reader modes j with lines x_j = 1, 1.41, 1.59, 1.68; the one-site worth of letter counts
  below the line) predicted the 4-mer worth z₄ at every (x, h, L) on new seeds with nothing fitted: 24/24 within
  3 SE. The composition reader's worth is bounded, decays with depth toward the letter-count value, and that value is
  PREREG15's Var_site/P within 20% in every cell.
- For EAG v4 §3 and the Atlas paragraph: a composition reader is worth 1.0–1.3 aligned sites below the line and
  about 2 sites at x = 1.5, falling toward one site with depth. This is the measured price of reading composition
  instead of sequence, with the line as its hinge.
