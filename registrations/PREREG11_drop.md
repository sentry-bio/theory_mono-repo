# PREREG11 — the drop as the swing test (registered 2026-09-30, before any correction was computed)

## Claim under test
The one-sign over-prediction of distinguishable states is a *derivable* quantity: it equals the count the model loses
when heterogeneity it averaged over is put back, and that heterogeneity can be measured on TRAIN genera alone and then
predicts the residual on TEST genera. If it derives, the "drop" stops being a named residual and becomes a term.

## What is already known (stated so the test cannot be quietly aimed at it)
The A-curve run (PREREG9) recorded aggregate AC1 residuals log(Σobs/Σpred) for the family image: bacteria
−0.002/−0.016/−0.041/−0.060/−0.081/−0.100/−0.121 at ε = 0.4…2.0 over 262 test genera; archaea −0.175 at ε = 2 over
35 genera (AC1 FAIL). Per-family residuals exist in acurve_{bac,ar}_results.json and have NOT been examined. The
derivations below use no residual, no test-genus coordinate, and no test-genus statistic other than the τ matrix.

## The image (unchanged from PREREG9)
Per family: Σ = cov of train genomes; Γ_fam(τ) from the train within-genus + within-family variogram (EDGES
geomspace(0.003, 1.5, 19), ≥ 150 pairs per bin), interpolated in log τ; below the first populated centre cen[0] the
fallback Σ − scale·Γ_pool(τ). Prediction for a test genus: greedy ε-packing of joint Gaussian draws with
Cov(z_i, z_j) = S_fam(τ_ij), averaged over replicates. This run recomputes obs, the r = 1 family prediction, and the
corrected predictions on the SAME genome subsets (seeds fixed), so all comparisons are internal to this run.

## Derivations (train only)
- **H-mix (primary; the Jensen mechanism).** Genus clock heterogeneity. For each TRAIN genus g with ≥ mingen genomes,
  the rate r_g solves mean_ij ||x_i − x_j||² = mean_ij 2·tr Γ_fam(r·τ_ij) (bisection on log r ∈ [−3, 3]); Γ_fam(τ) =
  Σ − S_fam(τ) with the same fallback. A family's rate distribution is {log r_g} over its qualifying train genera; if
  fewer than 3 qualify, the domain-wide distribution is used. Corrected prediction for a test genus: the equal-weight
  mean over the 0.1/0.3/0.5/0.7/0.9 quantiles r_q of the packing count of draws with Cov = S_fam(r_q·τ) (a clock
  rescaling, PSD by construction). Predicted correction Δ = log(pred_mix / pred_fam).
- **H-shape (secondary).** Isotropy deficit of the shallow fallback: below cen[0], replace the pooled shape with the
  family's own shallowest shape, S_shape(τ) = Σ − (τ/cen[0])·(Σ − S_fam(cen[0])). Everything else unchanged.
- **H-both (tertiary).** H-shape image with the H-mix clock mixture.
- **H-mix0 (exploratory, labelled).** Spread-only variant with r_g divided by its family geometric mean; separates the
  Jensen spread from a mean-clock offset. Reported, not scored.

## Predictions and rules (bacteria primary; archaea replication)
- D0 reproduction: the fresh r = 1 family prediction's aggregate residual at ε ≥ 1.0 lies within ±0.03 of the recorded
  values above. If not, the subsets differ; the run proceeds on its internal comparison and says so.
- D1 sign: for ≥ 90% of test genera at each ε ≥ 1.0, Δ_mix ≤ +0.02 (the correction can only lower the count, up to
  Monte Carlo noise).
- D2 aggregate: with H-mix alone, bacteria |log(Σobs/Σpred_mix)| ≤ 0.05 at every ε ≥ 1.0 (no over-correction either
  way); archaea ≤ 0.15 at every ε (the AC1 rule it failed) and ≤ 0.10 at ε ≤ 1.6.
- D3 per-family transfer: over families with ≥ 3 test genera, Spearman(Δ_fam, residual_fam) ≥ 0.5 at ε = 2.0 and the
  OLS slope of residual_fam on Δ_fam in [0.5, 1.5], where residual_fam = log(Σ_g obs / Σ_g pred_fam) and
  Δ_fam = log(Σ_g pred_mix / Σ_g pred_fam) over the family's test genera. (Rank right and magnitude right.)
- Verdict: **DERIVED** if D1–D3 hold for H-mix in bacteria and D2 holds in archaea. **PARTIAL** if D2 holds but D3
  fails (aggregate right, no per-family transfer), or if the rules hold only for H-shape/H-both. **NOT DERIVED**
  otherwise. Archaea failing D2 while bacteria pass everything is reported as DERIVED (bacteria) / NOT REPLICATED.
- Expected residual shape if H-mix is the mechanism but not all of it: the corrected residual is smaller with the same
  sign at every ε (finer-scale heterogeneity remains); a sign flip beyond −0.05 → +0.05 counts against the mechanism.

## Recorder arm (registered now, run after the Atlas arm)
Same law, finer scale. R-mix already mixed over colony activity classes and still over-predicted at ε = 2 on the swap
split (+0.14/+0.28/+0.21/+0.10/+0.16 by generation). Derivation: within-branch clumping, measured on TRAIN as the
dispersion of per-branch event counts, put into the writer as negative-binomial counts with that dispersion.
Prediction R-D1: the ε = 2 over-prediction falls to within ±0.10 in ≥ 4 of 5 generations on the swap split, with
ε = 0 and ε = 1 cells unchanged within ±0.05. Verdict independent of the Atlas arm.

## Caveats stated in advance
The five-quantile mixture approximates the rate distribution; families with few train genera inherit the domain
distribution, which weakens D3 for them (they are still scored). Clock rescaling assumes a genus differs from its
family by rate, not by direction; a direction-specific residual would be the next term, not this one. Monte Carlo
noise with 100 replicates is ~0.01 in log count per genus.

## Pre-run clarifications — 2026-09-30 03:34, before any correction was computed
- Cost: one 100-replicate draw for a 30-genome genus takes 5.3 s (4,050-dimensional eigendecomposition). H-both is run
  at three quantiles (0.2/0.5/0.8) instead of five; H-mix (primary) keeps five. H-mix0 is not run in this pass; each
  family's train rates {r_g} are saved so it can be computed later.
- D0 replay: the original per-family generator (seed 9001) is replayed by consuming the same standard-normal blocks the
  original draws consumed, so the test-genome subsets are identical; this run's own draws use a per-family seed
  derived from md5(family). Recorded aggregates are recomputed from acurve_{dom}_results.json, not typed in.
- Rate estimation on train genera: up to 30 genomes per genus (seed 9004); bisection on log r with 20 iterations;
  the shallow fallback is applied vectorised (same arithmetic as the original loop).
- Execution: bacteria split round-robin over sorted families into 3 local processes, archaea 1 process, 2 BLAS threads
  each, all under nice; the scorer runs once all parts finish and applies D0–D3 as written.

## Train-side observations — 2026-09-30 03:39, rates pass complete, main pass running, no test number seen
- Bacteria: 36 families (3 on the domain fallback), 288 train genera with rates; r quantiles 10/30/50/70/90 =
  0.41/0.70/0.93/1.21/1.83, geometric mean 0.94, SD(log r) 0.78; within-family SD(log r) median 0.65 (0.14–1.57);
  2% of genera at the upper cap, none at the lower. Archaea: 9 families (3 fallback), 31 genera; quantiles
  0.37/0.79/0.92/1.09/1.77, geometric mean 0.93, SD 0.79; 3% capped.
- The family kernel therefore sits near the mean clock (geometric mean ≈ 0.94), so H-mix is almost purely the spread
  term (Jensen), not a mean shift. A 4.5× spread between the 10th and 90th percentile genus is the heterogeneity the
  family-average image left out.
- Median cen0 is 0.016 (bac) / 0.028 (ar) and the median train-pair fraction below cen0 is 0.00: the shallow fallback
  rarely fires, so H-shape is expected to be close to a no-op. If it is, that settles the secondary candidate cheaply.

## Archaea result as registered — 2026-09-30 05:29 (bacteria still running)
35 test genera, 9 families (3 on the domain fallback). D0 PASS (fresh r=1 residuals reproduce the recorded ones to
±0.003). D1 PASS (Δ_mix ≤ +0.02 for 91–100% of genera at ε ≥ 1). D2 PASS: H-mix residuals at ε = 1.0/1.25/1.6/2.0 =
−0.057/−0.078/−0.090/−0.094 (from −0.071/−0.110/−0.150/−0.175), i.e. the ε = 2 residual is halved and archaea now sits
inside the AC1 rule it failed. Residual after correction is smaller with the same sign at every ε (the registered
"mechanism but not all of it" shape); no sign flip. H-shape is a no-op at coarse ε (−0.173 vs −0.175), as predicted
from the fallback rarely firing; secondary candidate settled. D3 FAIL: over 8 families with ≥ 3 test genera,
Spearman(Δ_mix, residual) = +0.29 (rule ≥ 0.5), OLS slope 0.85 (in range). Three of the eight are on the domain
fallback and carry no family-specific rank information; among the five informative families, Methanobacteriaceae
(−0.192 vs Δ −0.192), Haloarculaceae (−0.084 vs −0.082) and Poseidoniaceae (+0.047 vs −0.004) match, Thermoplasmataceae
half-matches (−0.285 vs −0.150), and Thalassarchaeaceae misses (−0.315 vs −0.012: small train heterogeneity, large
test residual). Verdict (archaea, H-mix): PARTIAL. Bacteria (36 families, 33 informative) is the D3 test with power.

## Bacteria result as registered — 2026-09-30 13:25
262 test genera, 36 families (3 on the domain fallback). D0 PASS (recorded residuals reproduced to ±0.001).
D1 FAIL, marginally: Δ_mix ≤ +0.02 for 100/100/100/97/92/90% of genera at ε = 0.4…2.0; at ε = 2.0 the fraction is
just under the 0.90 rule (three families have net positive Δ_mix: Rhizobiaceae +0.071, Micrococcaceae +0.042,
Beijerinckiaceae +0.022). D2 FAIL: H-mix moves the aggregate residual from −0.061/−0.081/−0.100/−0.120 to
−0.057/−0.074/−0.087/−0.102 at ε = 1.0/1.25/1.6/2.0, a 15% reduction against the 50% seen in archaea, nowhere near
±0.05. D3 FAIL: over 29 families with ≥ 3 test genera, Spearman(Δ_mix, residual) = +0.11, OLS slope 0.11; the
per-family residual spans −0.53 (Beijerinckiaceae) to +0.07 (Chitinophagaceae) while Δ_mix sits mostly within ±0.03.
H-shape is a no-op (−0.116 vs −0.120), as predicted. Verdict (bacteria, H-mix): NOT DERIVED.

Reading (verdict first, reading second): genus-level clock heterogeneity is a real term (sign law holds in ≥ 90% of
genera in both domains; half the archaeal drop) but it is a small part of the bacterial drop and it does not predict
which families over-predict. The registration's own caveat applies: "clock rescaling assumes a genus differs from its
family by rate, not by direction; a direction-specific residual would be the next term, not this one." The families
with the largest residuals (Beijerinckiaceae, Rhizobiaceae, Flavobacteriaceae, Microbacteriaceae, Enterobacteriaceae,
Burkholderiaceae) are well-sampled families with many closely related species; the smallest residuals are MAG-heavy
gut families with uniformly defined genera. Overall PREREG11 verdict: NOT DERIVED (bacteria primary), PARTIAL
(archaea). Any further derivation attempt is a new registration with a stopping rule, not an amendment of this one.

## Scope of the verdict, and the diagnostic — 2026-09-30 13:35
Audit of the run (execution): D0 reproduced Sunday's residuals to ±0.001 on replayed subsets; the vectorised fallback
matches the original loop to 3e-17; train rates are sane (geometric mean 0.94, 2% capped); the sign law held in
≥ 90% of genera. Audit of the design: the H-mix term is the Jensen gap ½·f″·Var(r), which is only large where a genus's
pair distances straddle ε; at ε = 2 bacteria is 76% distinct, so the term is structurally small there regardless of
the rate spread (archaea, 58% distinct, halved). The NOT DERIVED verdict therefore applies to the GENUS-RATE RUNG ONLY;
it does not settle whether the drop is derivable from heterogeneity measured on train genera.
Diagnostic (exploratory, labelled; uses test coordinates; same subsets as the run), bacteria at ε = 2: shortfall 522 of
4,094 distinct genomes; top 10% of genera carry 44% of it, top 25% carry 76%, 30% of genera have obs ≥ pred; pairs
closer than ε: observed 3,968 vs Gaussian-expected 2,501 (1.59×); the pair ratio d²/(2·tr Γ(τ)) has quantiles
1/5/25/50/75/95 = 0.12/0.25/0.52/0.80/1.20/2.19 where a 135-dof Gaussian gives ≈ 0.7 at the 1st percentile; 23% of
pairs below 0.5, 5% below 0.25; collisions sit at τ 0.015–0.16 (all pairs 0.08–0.46). Worst genera: MED-G14 (26
genomes, 4 distinct), MED-G13, UBA8316 (Flavobacteriaceae MAG genera), Polynucleobacter, Acidovorax, Cryobacterium,
Microvirga, MED-G52. Reading: the residual is a heavy near-duplicate tail concentrated in specific clades, i.e. rate
heterogeneity BELOW the genus (subclades compositionally frozen relative to their marker clock), which a genus-wide
clock cannot represent. That rung is registered separately as PREREG12, written after this diagnostic was seen.
