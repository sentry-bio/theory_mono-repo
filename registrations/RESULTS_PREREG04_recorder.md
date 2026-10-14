# Lineage recorders (intMEMOIR) — results, 2026-09-26

Registered (PREREG4.md; 60 train / 47 test colonies; write model fitted on train only):

| Test | Verdict | Numbers (test colonies, generations 0–4) |
|---|---|---|
| R1 recorded fraction per generation | FAIL | observed 0.82/0.76/0.61/0.49/0.30 vs predicted 0.96/0.92/0.83/0.72/0.60; calibration error 0.23 |
| R2 collisions (indistinguishable lineages), generations 1–5 | FAIL | observed 0.11/0.16/0.26/0.39/0.52 vs predicted 0.03/0.04/0.10/0.18/0.27 |
| R3 regime: recorded >= 1/2 iff expected distinguishing events m >= ln 2 | PASS | m = 3.87/3.06/1.52/0.69/0.25; knife-edge at generation 3 (m 0.690 vs 0.693, recorded 0.486) |

Train fit: the writer is nearly off before frame 60 (0.0006/frame), ~0.009/frame after, 0.005 late; site
efficiencies differ ~15-fold; misread rate 3.5%.

Exploratory (post hoc, after the failure; run inline, numbers recorded here):
1. Colony-level overdispersion of editing: standardised deviations SD 2.09 (model 1.0), 11/60 train colonies
   beyond |z| > 3. A colony-activity random effect (log SD 0.71, drawn from train) barely moves predictions
   (generation 0: 0.955 → 0.934).
2. Edits are clumped on branches (parsimony placement on true trees, all colonies): variance/mean 1.98 vs model
   1.18 (95% 1.11–1.25); branches with no event 52.5% vs 39.4%; 51.8% of events on branches with >= 3 events vs 32.5%.
3. Branch-level bursts (gamma multiplier shared by all sites on a branch, shape 0.25 tuned on train dispersion)
   predict test generations 0–1 well (0.75/0.77 vs 0.82/0.76) but not the late decline (generation 4: 0.61 vs 0.30).
   Hypothesis, untested: writer activity is heritable within sub-lineages (quiet sub-lineages stay quiet).

Reading: the independent-site write model overcounts independent writing events. The Atlas's round-1 failure had
the same shape (the pooled kernel overcounted independent channels). Memory is set by the number of independent
write events or channels, which correlation and heterogeneity reduce.
