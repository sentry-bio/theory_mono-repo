# Confirmation suite — pre-registration (2026-09-28, written before any of this code ran)

Law under test: distinguishable lineages at depth τ = ε-packing number of the process's retained image on the actual
tree; the reader enters only as metric + ε; real images are mixtures. Standard for a definitive pass: disjoint data,
no parameter touching the outcome, a live baseline that fails, many cells and many statistics from ONE image, and
replication.

## R-mix (recorders, intMEMOIR; 60 train / 47 test as before)

The empirical writer (PREREG5) with two process-structure corrections, both estimated on train only:
1. Branch-type-matched donors. Internal branches draw from internal donors (root edge included); leaf branches draw
   from LEAF donors (events placed on leaf branches by the same tolerant rule, which include misreads), and no
   separate misread step is applied. Rationale: leaf branches were excluded as donors before, so late daughters
   inherited internal-branch activity and misreads were added on top of donor configurations that already contain
   them.
2. Colony activity classes. Per train colony, activity = placed events per branch-frame over all branches; terciles
   define three classes with class-specific donor pools. Each simulated colony draws a class: with train class
   frequencies conditional on the colony's depth class (max generation ≤ 3, 4, ≥ 5) if Spearman(activity, max
   generation) on train has |ρ| ≥ 0.3, else unconditional. 400 replicates.
   Branch-level quiet mass is already present (empty donor configurations); no extra quiet parameter.
- Validation on train (leave-own-colony-out donors) before any test statistic: dispersion of placed events per
  internal branch within ±0.3 of observed, and per-colony edited-leaf fraction standardised deviation SD ≤ 1.5
  (was 2.09 under the homogeneous model). If either fails, the writer is fixed and the fix recorded here.
- Registered directions: ε = 0 errors at g4–5 move toward 0 (currently −0.15, −0.32); ε = 2 error at g5 moves toward
  0 (currently +0.41); ε = 1 stays within ±0.15 in every generation; recorded fraction at g3–4 moves toward the
  observed 0.49/0.30 (currently predicted 0.64/0.62 by the empirical writer).
- Rules (test colonies): RM1 D_g at ε ∈ {0, 1, 2}, every generation with ≥ 50 lineages, |log error| ≤ 0.15.
  RM2 recorded fraction per generation with ≥ 30 divisions within max(0.07, 2 predictive SD), calibration over
  predicted-probability bins mean |error| ≤ 0.07. RM3 reader cell: strict and tolerant clade signatures (tolerance
  x = 0/1/2 for clade size ≤ 3/≤ 12/> 12) at ε = 1, both predicted from the same simulated leaf states, both within
  ±0.15 in every gated generation. Baseline: the PREREG5 writer (homogeneous across colonies, internal donors only,
  misreads added) must fail RM1 at ε = 0 or ε = 2 where R-mix passes.
- Verdict: CONFIRMED if RM1, RM2, RM3 all pass and the baseline fails at least one RM1 cell; PARTIAL if RM1 and RM3
  pass; REFUTED if RM1 fails at ε = 1 anywhere or at more than one cell overall.

## R-swap (replication within dataset)

Train₂ = the 47 former test colonies; test₂ = the 60 former train colonies, whose collision and recording
statistics have never been computed. Writer (donor pools, activity classes) re-estimated on train₂ only. Same rules
RM1–RM3, same verdict definitions. Both splits CONFIRMED = the operating law and mixture clause confirmed within
intMEMOIR.

## A-curve (Atlas trait layer; base map v1.0; bac120 r220; E-D family split; families ≥ 300 genomes)

- Process per family: the E-D full-matrix process from train genera (Γ_f(τ) bins with ≥ 150 pairs, Σ_f; below the
  first bin, pooled within-genus shape scaled to the first bin's trace). One image per family for all statistics.
- AC1 packing curves: test genera with ≥ 10 genomes (cap 30, seed 9001); joint Gaussian draw on the genus subtree,
  200 reps; greedy ε-packing in the recipe metric at ε ∈ {0.4, 0.6, 0.79, 1.0, 1.25, 1.6, 2.0} (0.79 = K2's ε).
  Rule: at every ε, |log Σ_obs − log Σ_pred| ≤ 0.15 over all such genera, AND the median per-genus |log error| ≤
  0.25 at ε ≥ 1.0 (the non-saturated range). Baselines: pooled process; "all distinct" (Σ N); both must fail at some
  ε ≥ 1.0 where the family image passes.
- AC2 quartets: new F4 quartets from test genera (seed 9002, ≤ 300 per family), predicted by the same family image
  (full-matrix CLT, as E-D). Rule: pooled t-bins with ≥ 150 quartets, |obs − pred| ≤ 0.05 each, mean ≤ 0.03.
- AC3 retrieval: per family, 60 random test genomes (seed 9003; all if fewer), simulated jointly (50 reps);
  fraction whose nearest neighbour among the 60 is same-genus, predicted vs observed. Rule: pooled over families
  within ±0.05; per-family mean |error| ≤ 0.10.
- Verdict: CONFIRMED if AC1–AC3 pass with baselines failing in AC1; PARTIAL if AC1 passes; REFUTED if AC1 fails at
  two or more ε ≥ 1.0.

## A-arch (replication in a second domain of life)

ar53 r220 tree; catalogue archaea. Families with ≥ 100 genomes, split by md5("E-D:" + genus) parity, train ≥ 50,
≥ 3 test genera. AC1 only, same ε grid and rule, genera with ≥ 6 genomes. Reported: number of families and genera.

## Deferred (not run)

Atlas reader cell (recipe vs unwhitened log-ratio metric): needs halves distances in the second metric, which were
not retained. Hippocampal filling fraction: a translation, not a test, until a cross-condition prediction is
registered. Algorithm-independence tests: tautological given known topology.

## Overall

The law is CONFIRMED at the level claimed (operating law + mixture clause + reader-relativity, two media, replicated)
if R-mix and R-swap are CONFIRMED and A-curve is at least PARTIAL with A-arch passing AC1. Anything less is reported
as scored, with the reading kept separate from the verdict.

## R-mix result (2026-09-28)
Validation (main) PASS: dispersion 1.86 vs 1.88; colony z SD 1.16. Spearman(activity, depth) −0.06 → classes drawn
unconditionally. Test (47 colonies): RM1 FAIL at ε=1 g3–5 (+0.23/+0.18/+0.18) and ε=2 g5 (+0.45); RM2 FAIL (g2:
0.61 obs vs 0.49; calibration 0.078); RM3 FAIL. Baseline PREREG5 writer fails at ε=0 g4–5 and ε=2 g5. Verdict as
registered: REFUTED.
Registered directions: ε=0 late closed as predicted (−0.15/−0.32 → +0.07/−0.02); recording at g3–4 moved toward
observed as predicted (0.64/0.62 → 0.40/0.33 vs 0.49/0.30); ε=2 g5 did NOT move (+0.45); ε=1 did NOT stay within
±0.15 (worsened from ≤0.11 to ≤0.23); early recording now under-predicted (g1–2: 0.67/0.49 vs 0.76/0.61).
Reading (post hoc): leaf-branch donors cannot represent misreads (transitions to state 0, or at already-edited
sites) under the exhaustion rule, so the corrected writer under-produces multi-site variation; the PREREG5 writer
modelled misreads correctly but over-produced late single-site differences. Neither passes the full table.
R-swap validation (train₂ = 47): dispersion 1.77 vs 1.86 (ok), colony z SD 1.55 (> 1.5) → FAIL; per registration the
writer is to be fixed on train-only diagnostics and recorded here before any swap test statistic.

## Amendment — 2026-09-28 13:35, after R-mix main and A-arch, before any swap test statistic
- Train-only diagnostic: leaf branches carry 0.829 placed events each vs 0.457 expected from internal donors plus
  0.352 expected misreads → true-edit activity of leaves relative to internal donors r = 1.05 (by start bin
  1.68/1.43/2.11/0.86; the late bin holds 774 of 838 leaves). The leaf-donor construction is therefore withdrawn:
  leaf branches revert to internal donors plus misreads at ε from the PREREG4 fit (the PREREG5 treatment).
  Colony activity classes are kept. The main test set has now been seen at all three ε, so the revised writer's
  verdict comes from R-swap ONLY; its main-split table is reported as seen data, not as a verdict.
- A-arch (35 test genera, 517 leaves): AC1 FAIL as registered. Family-image log-error by ε: 0.000/−0.006/−0.048/
  −0.072/−0.111/−0.147/−0.175 (ε 0.4…2.0); pooled −0.23 and all-distinct −0.54 at ε = 2. The family image is the
  best process but over-predicts distinctness increasingly with ε (reality more compact).
- A-curve bacteria: AC2 crashed on a code shape bug in the shallow-kernel fallback (no design change); rerun.
- 2026-09-28 13:35: revised writer failed swap validation on colony z SD only (1.58 vs 1.5; dispersion 1.69 vs
  1.86 ok). Cause: with 47 train colonies, tercile pools (~16 colonies) fall back to all classes under the 30-donor
  minimum. Fix: class-specific pools accept >= 15 donors (all-class fallback below that). Re-validated below.
- 2026-09-28 13:39: with the 15-donor pools the swap writer still fails validation (dispersion 1.64 vs 1.86;
  colony z SD 1.62). Two failed fixes; further changes would be fitting. R-swap is NOT RUN under the registered gate.
  Revised writer on the SEEN main split (reported, not a verdict): ε=1 within ±0.12 in every generation and the
  tolerant-reader cell passes (RM3), but ε=0 g5 and ε=2 g5 fail and per-division recording is over-predicted late
  (g2–4: 0.69/0.63/0.61 vs 0.61/0.49/0.30), i.e. the PREREG5 pattern returns. Colony activity classes did not
  repair the late cells. Recorder arm of the suite: R-mix REFUTED, R-swap not run.

## Amendment — 2026-09-28 13:43, readout mixture (registered before the swap test statistic)
Train-only diagnostics: (1) duration matching of internal donors is accurate in every late bin (e.g. bin 3, 30–45
frames: 0.402 observed vs 0.385 expected events); (2) in-sample recording is right for internal-daughter divisions
(≤ 0.06 off at every generation) and wrong only for leaf-daughter divisions (g2–4: 0.64/0.62/0.61 predicted vs
0.52/0.48/0.36); (3) in 240 short train cherries (< 25 frames), per-site discordance is nearly uniform across
sites (3× spread), yet P(any discordant site) is 0.404 against 0.637 for independent sites: 143 cherries differ at
no site, and the count of discordant sites is overdispersed (var/mean 2.62). The residual structure is a per-cell
readout mixture, not site-specific error and not the writer.
Model: each leaf is read cleanly (rate ε_c) or noisily (rate ε_n) with probability π, fitted by maximum likelihood on
train short cherries to the distribution of discordant-site counts (with a fixed edit offset 0.024 per site from
the duration regression). Internal donors and colony classes unchanged. Registered directions: leaf-daughter
recording falls toward observed while internal-daughter recording is unchanged; ε=0 g5 and ε=2 g5 errors move
toward 0; ε=1 stays within ±0.15. Verdict from R-swap only (RM1–RM3 as registered); main split reported as seen.
- 2026-09-28 13:47 readout-mixture results. Fitted on train: main π=0.136, ε_clean=0.0005, ε_noisy=0.268 (240
  cherries); swap-train π=0.096, ε_clean≈0, ε_noisy=0.236 (164 cherries). Main split (SEEN): RM1 PASS (all 15 ε×gen
  cells within ±0.15; ε=0: −0.03/0.00/+0.04/+0.02/−0.10; ε=1: +0.02/+0.05/+0.10/+0.02/−0.07; ε=2: +0.06/+0.06/−0.01/
  −0.09/+0.14), RM3 PASS, RM2 FAIL by calibration 0.072 vs 0.07 (every generation within tolerance; g4 0.41 vs 0.30
  inside 2 SD). Registered directions all realised (leaf-daughter recording fell, ε=0 g5 −0.32 → −0.10, ε=2 g5
  +0.40 → +0.14, ε=1 within ±0.10). Scored on seen data: PARTIAL, not a verdict.
  Swap validation: dispersion 1.71 vs 1.86 (ok), colony z SD 1.57 (> 1.5) → gate FAIL a third time; this criterion
  has not moved with any writer change (1.55/1.62/1.57) and reflects the 47-colony train. The swap test is run below
  FOR INFORMATION ONLY, labelled as run after a gate miss; it is not a registered verdict.
- 2026-09-28 13:51 R-swap (information only; gate missed). Writer from 47 colonies (π=0.096, ε_noisy=0.236),
  predictions on the 60 never-scored colonies. Distinct lineages: ε=0 −0.002/+0.09/+0.05/+0.003/−0.05 (all within
  ±0.10); ε=1 +0.07/+0.16/+0.11/+0.11/+0.08 (one cell over 0.15); ε=2 +0.14/+0.28/+0.21/+0.10/+0.16 (three cells
  over). Recording: 0.81/0.75/0.60/0.51/0.47 vs 0.83/0.86/0.65/0.52/0.36 (g1 under, g4 over); calibration 0.059.
  Tolerant reader +0.12/+0.18/+0.16/+0.11/+0.08. Baseline writer fails worse (ε=0 g4–5 −0.16/−0.27; ε=2 +0.13…+0.29).
  Scored by RM1–RM3 it would be REFUTED (RM1 fails at ε=1 g2 and ε=2 g2/g3/g5). Reading: every ε=2 error is positive
  (reality more distinct at coarse resolution), consistent with the noisy-cell rate being underestimated from 164
  cherries (π 0.096 vs 0.136 on the larger train); fine resolution is predicted almost exactly.
  Recorder arm final status: R-mix REFUTED as registered; R-swap not run under the gate; the readout-mixture image
  is PARTIAL on seen data and, on the unseen swap, exact at ε=0 and short at ε=2.

## A-curve (bacteria) result — 2026-09-28 14:57
One family image (E-D full-matrix process from train genera) → three held-out statistics, 36 families:
- AC1 packing curves, 262 test genera, 5,384 leaves: family-image log-error by ε (0.4…2.0) = −0.002/−0.016/−0.041/
  −0.060/−0.081/−0.100/−0.121; median per-genus |error| at ε ≥ 1.0 = 0.009/0.039/0.070/0.085 → PASS. Baselines fail at
  ε ≥ 1.6: pooled −0.166/−0.153, all-distinct −0.189/−0.274.
- AC2 quartets (new F4, seed 9002): t-bins 0.10–0.60, observed vs predicted 0.546/0.566, 0.533/0.531, 0.447/0.450,
  0.389/0.401; worst 0.020, mean 0.009 → PASS. (No t-bin below 0.097 had ≥ 150 quartets, so the shallow-extrapolation
  region is not exercised.)
- AC3 retrieval (60 test genomes per family): same-genus nearest neighbour observed 0.688 vs predicted 0.736
  (|diff| 0.048 ≤ 0.05, marginal); per-family mean |error| 0.056 → PASS.
A-bac verdict: CONFIRMED as registered. Residual, same sign as archaea: the family image over-predicts
distinctness increasingly with ε (bacteria −0.04 → −0.12, within tolerance; archaea −0.05 → −0.18, over) and
over-predicts genus separability (0.736 vs 0.688). Overall PREREG9 rule not met (R-mix REFUTED, R-swap not run,
A-arch FAIL); the Atlas arm stands at A-curve CONFIRMED, A-arch FAIL.
