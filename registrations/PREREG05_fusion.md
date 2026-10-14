# Fusion test (recorders) — pre-registration

Written 2026-09-28 before any code for this test ran. Same data and split as PREREG4 (60 train / 47 test colonies).

Conjecture: the accounting law's independence term is the entropy the medium actually writes, not a count of
events. Registered models overcounted independent events (R1/R2 failed); an entropy-defined writer should not.

Atlas arm dropped at design time: packing/correlation dimension from a few hundred genomes in 135 dimensions
saturates near 2·log10(N) ≈ 5–7, so it cannot reach the ~14 effective channels; the test would fail by construction.

## Empirical writer (train only)
- Donor branches: internal nodes with >= 2 leaves (and the root edge / founder branches) of train trees. Leaf
  branches are not donors (misreads are indistinguishable from edits there).
- Event (s, a) placed on the branch into v if at least k − x of v's k leaves carry a at s (x = 0 for k <= 3, 1 for
  k <= 12, 2 above), the mismatching leaves are not exactly one daughter clade of v, and the same rule does not
  hold at v's parent.
- Target branch (start time a, duration d): donors from the same start bin ([0,60),[60,110),[110,160),[160,217])
  with duration within ±25% (widen to ±50%, then the whole bin, until >= 30 donors). A train colony's own
  branches are never its own donors.
- Simulation: every site starts unedited (founder edits come from root-edge donors); each branch applies one
  sampled donor configuration to still-unedited sites; leaves are misread at ε from the PREREG4 fit. 400 reps.
- W_v = Miller–Madow entropy (nats) of the donor-configuration distribution for daughter A plus that for B.

## Validation on train (before any test statistic)
The empirical writer run on train colonies (leave-own-colony-out) must reproduce the train dispersion of placed
events per branch within ±0.3 of the observed value. If not, fix the simulator and record the fix here.

## Rules (test colonies)
- F1 regime: in each generation with >= 30 divisions, recorded >= 1/2 iff mean W_v >= ln 2.
- F2 recorded fraction per generation within max(0.07, 2 SD) of prediction in every gated generation, and
  calibration over 5 predicted-probability bins (>= 20 each) with mean |error| <= 0.05.
- F3 collision fraction within max(0.07, 2 SD) in every generation with >= 50 lineages.
- F4 logistic recorded ~ log W vs recorded ~ log m, each fitted on train divisions; W wins if its test log-loss is
  lower.
- Fusion supported if F2, F3 and F4 pass. Partial if F4 passes and F2 or F3 improves on PREREG4 in every
  generation. Refuted if F4 fails.

## Result (2026-09-28)
Validation on train passed (dispersion 1.84 ± 0.12 vs observed 1.88). Test: F1 FAIL, F2 FAIL, F3 FAIL, F4 FAIL →
fusion REFUTED as registered. Recorded fraction gens 0–4: observed 0.82/0.76/0.61/0.49/0.30, entropy writer
0.88/0.82/0.69/0.64/0.62 (gens 0–1 in tolerance). Collisions gens 1–3 in tolerance, 4–5 not. W stays > ln 2 (2.7
nats at gen 4) while recording is 0.30; per-division log-loss W 0.629 vs count 0.594.
Reading: recording depends on whether anything distinguishing is written (count-like), not on write diversity
(entropy); the remaining late shortfall is persistence of writer activity across branches within sub-lineages,
which no per-branch quantity captures. Next conjecture (post hoc, unregistered): lineage-level writing entropy
with heritable activity.
