# PREREG12 — the drop as heritable rate heterogeneity below the genus (registered 2026-09-30, after the PREREG11
# diagnostic was seen and before any clock parameter was fitted)

## Why this registration exists
PREREG11 tested a single clock per genus and found it a small term (15% of the bacterial drop; half in archaea). Its
diagnostic showed the residual is a near-duplicate tail concentrated in specific clades: 23% of within-genus pairs sit
below half the kernel's expected squared distance and 5% below a quarter, where a 135-dimensional Gaussian puts
essentially none; collisions occur at τ 0.015–0.16; 10% of genera carry 44% of the shortfall. Train genera show the
same tail at the subclade level (single linkage at τ ≤ 0.05: 14% of subclades below 0.25, 37% below 0.5, SD of log
ratio 0.91) and between-subclade pairs are equally spread (5/50/95 = 0.26/0.81/2.31). Heterogeneity is therefore
present at every level of the genus tree, which is what a heritable (autocorrelated) clock produces. This is the
trait layer's own claim, that composition rates are heritable settings, turned into a mechanism with one parameter.

## The mechanism (autocorrelated lognormal relaxed clock on the composition process)
For a test genus with sampled genomes g (same subsets as PREREG11, replayed), take the induced subtree on the GTDB
r220 tree (nodes = sampled leaves and their pairwise LCAs; edge lengths from root distances). Log-rate performs a
Brownian motion along the tree: at the subtree root, log m ~ N(0, s_g²); along an edge of length ℓ, log m(child) =
log m(parent) + N(−ν·ℓ/2, ν·ℓ) (the drift keeps E[m] = 1); the rate on an edge is exp of the mean of its endpoint
log-rates (Kishino et al. 2001). The effective divergence of a pair is τ_eff(i, j) = Σ_path m_e·ℓ_e, and the image is
the PREREG9 family Gaussian evaluated at τ_eff: Cov(z_i, z_j) = S_fam(τ_eff(i, j)), exactly as H-mix used S_fam(r·τ).
Under this model the median pair ratio is below 1 and the left tail is heavy, both by construction of a mean-1
lognormal, so the model is falsifiable already on train: one ν must reproduce five ratio quantiles.

## Parameters, from TRAIN genera only
- s_g (root rate spread): the SD of log r_g over the family's train genera from PREREG11's rates pass (domain-wide if
  fewer than 3 genera; values already on disk in drop_rates_{dom}.json).
- ν (clock variance per unit τ): per family, grid {0.25, 0.5, 1, 2, 4, 8, 16, 32}; for each ν, simulate 50 clock
  realisations per train genus (≤ 30 genomes, seed 9004 as before), compute the implied pair ratio
  tr Γ(τ_eff)/tr Γ(τ) (tr Γ tabulated on a log-τ grid), pool over the family's train genera, and take the quantiles
  5/25/50/75/95 of its log; choose ν minimising the sum of squared differences from the observed train log-ratio
  quantiles. Families with fewer than 5 train genera use the domain-wide fit.
- Train fit adequacy (registered gate): if the best ν leaves any of the five quantiles more than 0.20 (log) from the
  observed one for the domain-wide pool, the mechanism is declared inadequate on train and the test is not run.

## Prediction for a test genus
K = 8 clock realisations, each with 12 Gaussian replicates (96 draws; the r = 1 baseline uses the same 100-replicate
draw and seed as PREREG11, so its counts are identical). Corrected prediction = mean count over realisations and
replicates at each ε. Δ = log(pred_clock / pred_fam).

## Rules (bacteria primary; archaea replication)
- D0 reproduction: the baseline reproduces PREREG11's fam counts (identical seeds; tolerance ±0.005 in aggregate log).
- D1 sign: Δ ≤ +0.02 for ≥ 85% of test genera at each ε ≥ 1.0 (a relaxed clock can raise a fast subclade's count;
  net lowering is the prediction).
- D2 aggregate and ε-shape: bacteria |log(Σobs/Σpred_clock)| ≤ 0.05 at every ε ≥ 0.79; archaea ≤ 0.10 at every ε.
- D3 per-family transfer at ε = 2.0: over families with ≥ 3 test genera, Spearman(Δ_fam, residual_fam) ≥ 0.5 and OLS
  slope in [0.5, 1.5].
- D4 per-genus concentration at ε = 2.0: over all test genera, Spearman(Δ_g, residual_g) ≥ 0.4, where
  residual_g = log(obs_g / pred_fam_g) and Δ_g = log(pred_clock_g / pred_fam_g).
- Verdict: DERIVED if D1–D4 hold in bacteria and D2 holds in archaea. PARTIAL if D2 holds with exactly one of D3/D4.
  NOT DERIVED otherwise.
- Stopping rule: if NOT DERIVED, the drop at the Atlas is declared a measured quantity (usable as a calibration, not a
  term) and no further derivation attempts are made on the Atlas arm; the recorder arm (PREREG11 §recorder) proceeds
  independently. If DERIVED, the next registered step is the same clock applied to the recorder (clumped writing as a
  relaxed write-rate) and to the hippocampal population covariance.

## Caveats stated in advance
S_fam(τ_eff) treats the family kernel as a function of effective divergence, an approximation for a saturating kernel
(exact for a Brownian one). The induced subtree uses GTDB branch lengths, so the clock's ν is per unit marker-protein
divergence. Eight clock realisations per genus give Monte Carlo noise of order 0.02 in log count per genus; the
aggregate and Spearman statistics average over 262 genera. This registration was written after the PREREG11
diagnostic (which used test coordinates) was seen; the parameters themselves are fitted on train genera only.

## Pre-run clarifications — 2026-09-30 13:39, before any clock parameter was fitted
- The train fit compares quantiles of log pair ratio. The simulated ratio includes the Gaussian's own scatter (the
  observed squared distance is a 135-degree chi-square around its expectation under the model): simulated ratio =
  trΓ(τ_eff)/trΓ(τ) × χ²₁₃₅/135. trΓ is tabulated on 600 log-spaced τ points and interpolated, for observed and
  simulated alike.
- Train subsets and order replicate the PREREG11 rates pass exactly (seed 9004, families and genera sorted), so s_g and
  ν are estimated on the same genomes.
- The r = 1 baseline in the test pass is the first draw from the same per-family generator as PREREG11 with the same
  replicate count, so its counts are bit-identical; the clock realisations use a separate generator (seed
  md5("clock:"+family)).
- Execution: 3 bacterial parts + 1 archaeal, 2 BLAS threads each, under nice and caffeinate; the scorer applies D0–D4.

## Train fit — 2026-09-30 13:41, main pass running, no test number seen
- Bacteria: domain ν = 2.0 (per unit marker divergence). Observed log pair-ratio quantiles 5/25/50/75/95 =
  −1.40/−0.64/−0.22/+0.20/+0.84; best-fit errors (simulated − observed) = −0.03/+0.20/+0.17/+0.03/−0.03. GATE PASS at
  the boundary (max error 0.20). Archaea: ν = 1.0; observed −1.20/−0.56/−0.15/+0.24/+0.85; errors
  −0.08/+0.14/+0.11/+0.05/+0.12; GATE PASS.
- Reading before the test: one ν reproduces both tails of the ratio distribution, but the simulated middle sits
  0.17–0.20 (log) ABOVE the observed in bacteria: typical within-genus pairs are ~20% closer than the family kernel
  says even after the clock. A mean-1 clock cannot produce that; it is a bias in the kernel's typical level, most
  plausibly from pair-weighted variogram estimation (large genera and deep pairs dominate). Prediction stated now: the
  clock will remove the tail-driven part of the drop and leave a residual of order −0.05 to −0.08 at coarse ε with
  the sign law intact. If that is what the test shows, the remainder is an estimator matter (re-estimate Γ with equal
  genus weights), not a theory term, and the verdict must say so rather than call it heterogeneity.

## Result as registered — 2026-09-30 15:51 (files in prereg12_v1/)
BACTERIA: PARTIAL. D0 PASS (baseline identical to PREREG11, 0.0004). D1 PASS (92–100%). D2 PASS with the ε-shape
reproduced: clock residuals −0.036/−0.040/−0.041/−0.040/−0.044 at ε = 0.79/1.0/1.25/1.6/2.0 (from
−0.041/−0.061/−0.082/−0.100/−0.120); the growth with ε is gone and a flat −0.04 remains, inside the pre-stated
−0.05…−0.08 band for the kernel-level bias. D3 PASS: Spearman(Δ_clock, residual) = +0.62, slope 0.77 over 29 families
(Flavobacteriaceae −0.326 vs −0.282; Rhizobiaceae −0.370 vs −0.226; Enterobacteriaceae −0.231 vs −0.158;
Burkholderiaceae −0.187 vs −0.113; Lachnospiraceae −0.098 vs −0.058; misses: Beijerinckiaceae −0.536 vs −0.003,
Microbacteriaceae −0.304 vs −0.068). D4 FAIL: per-genus Spearman +0.17.
ARCHAEA: NOT DERIVED. Clock residual −0.160 at ε = 2 (from −0.175); D1 FAIL at ε = 2 (63%: the clock RAISES counts
for many genera); D3 +0.33/0.26; D4 +0.16. 20 of 35 genera on the domain ν.
Two things noticed on reading, recorded before any change: (i) the registered root draw log m ~ N(0, s_g²) has mean
rate exp(s_g²/2) > 1, contrary to the stated intent "E[m] = 1"; with s_g ≈ 0.7 that is a 1.3× upward bias in the root
rate, which raises counts and is the likely cause of the archaeal D1 failure (bacteria's ν = 2 drift dominated it).
(ii) D4 was ill-posed for a stochastic clock: the model assigns genera with similar trees the same expected
correction, while the realised residual of one genus is a single draw, so per-genus rank agreement cannot be high
even when the model is right; the well-posed per-genus test is coverage (calibration), as in R-mix's RM2.
Both are handled by amendment PREREG12a below; the results above stand as the registered PREREG12 outcome.

## Amendment PREREG12a — 2026-09-30 15:51, registered before running
- Root draw corrected to mean rate 1: log m(root) ~ N(−s_g²/2, s_g²). Everything else in the mechanism unchanged.
  ν is refitted on train with the corrected root (same procedure, same gate).
- Realisations per genus raised from 8 to 12 (10 Gaussian replicates each) so that per-genus spread is estimable.
- D4 is retained and reported as registered. A well-posed per-genus rule D4′ (coverage) is added: with
  z_g = (obs_g − mean_clock_g) / SD_g at ε = 2, where SD_g is the SD of the 12 realisation means (floored at 0.5
  genome), PASS if |z_g| ≤ 2 for ≥ 85% of test genera and |mean z| ≤ 0.5 (no systematic bias).
- Verdict for PREREG12a: DERIVED if D1–D3 and D4′ hold in bacteria and D2 holds in archaea; DERIVED (bacteria) /
  NOT REPLICATED (archaea) if archaea fails D2; PARTIAL if D2 holds with one of D3/D4′; NOT DERIVED otherwise. The
  stopping rule of PREREG12 applies to PREREG12a's outcome.
- Prediction stated now: bacteria's D2/D3 results move little (its correction was drift-dominated); the flat −0.04
  remainder persists (kernel-level bias, an estimator matter to be tested separately by re-estimating Γ with equal
  genus weights); archaea's D1 failure is expected to resolve, and its D2 outcome is genuinely open.

## PREREG12a outcome — 2026-09-30 15:56: GATE FAILED on train (registered stop; test not run)
With the root at mean rate 1, no ν on the grid fits the train quantiles: bacteria best ν = 0.25 with errors
−0.23/+0.11/+0.09/−0.08/−0.27 (left tail too heavy, right tail too light); archaea ν = 0.5, errors
−0.31/+0.07/+0.04/−0.11/−0.15. Diagnosis: the cumulative drift −νℓ/2 that keeps E[m] = 1 in a Brownian log-rate
pushes long paths down and cannot widen the right tail; in v1 the root's upward bias (mean 1.38) supplied the right
tail and ν = 2 the left, which is why v1 fitted at the boundary and 12a cannot. The observed marginal is in fact a
single mean-1 lognormal: from the median −0.22, σ² = 0.44 (σ = 0.66) predicts quantiles −1.31/−0.67/−0.22/+0.23/+0.87
against observed −1.40/−0.64/−0.22/+0.20/+0.84, one parameter read off the median. A genus-wide factor with that σ
(ν = 0, which is PREREG11's H-mix in lognormal form) fits the marginal but produces almost no correction, because
the marginal does not carry the DEPENDENCE that makes collisions: frozen subclades. The Brownian clock added
dependence only by breaking the marginal. The correctly specified model is a STATIONARY heritable rate process (an
Ornstein–Uhlenbeck log-rate on the tree): stationary variance σ² fixed by the marginal, mean-reversion θ setting how
much of the variance is shared by a clade. θ is identifiable on train from how the log-ratio spread varies with τ
and from the variance of subclade means. That check is run next, before any registration.
RETRACTION: the "kernel-level bias from pair-weighted estimation" I put on record earlier today as the explanation of
v1's flat −0.04 remainder was wrong reasoning. The kernel estimates the MEAN of d² correctly; under a lognormal spread
the median sits below the mean by σ²/2 ≈ 0.22, which is the observed −0.22. There is no kernel bias to fix. v1's
remainder is more plausibly its own root-level mis-specification.
STATUS of PREREG12 v1: recorded as PARTIAL (D2, D3 passed; D4 ill-posed) under a mis-specified marginal; supportive of
the mechanism (heritable subclade heterogeneity), not a derivation. The derivation claim rests on the stationary
model, to be registered as PREREG13 with a final-attempt clause.
