# PREREG13 — stationary heritable rate (OU log-rate) as the drop mechanism: FINAL derivation attempt on the Atlas arm
# (registered 2026-09-30 after the train-side structure check; no test statistic has been computed for this model)

## Why this model, from train data only
On 68,131 bacterial train pairs the log pair-ratio (observed d² over the family kernel's expectation) has median
−0.22, mean −0.24 and SD 0.69: a mean-1 lognormal (−σ²/2 = −0.24). Its SD falls with τ: 0.81/0.75/0.68/0.61/0.58 across
τ quintiles (medians 0.065/0.147/0.223/0.310/0.427). 42% of the pair variance is shared genus-wide (SD of genus means
0.45); within-subclade means at cutoff 0.02 have SD 0.74, larger than pairs at depth. Archaea: SD 0.63,
0.76 → 0.57 with τ, 47% genus-shared. A Brownian log-rate (PREREG12) has spread growing with τ and is excluded; a
genus-wide factor (PREREG11) is flat in τ and produces no within-genus dependence; a stationary mean-reverting rate
has spread decaying with τ and clade-shared components at every scale. The data leave that one.

## Mechanism
On the induced GTDB subtree of a test genus (same subsets as PREREG11/12, replayed), the node log-rate follows an
Ornstein–Uhlenbeck process with stationary law N(μ, σ²), μ = −σ²/2 (mean rate 1 at every node), and reversion rate θ
per unit τ: root lm ~ N(μ, σ²); child lm_c = μ + (lm_p − μ)·e^{−θℓ} + N(0, σ²(1 − e^{−2θℓ})). Edge rate m_e =
exp((lm_p + lm_c)/2); τ_eff(i,j) = Σ_path m_e ℓ_e; image Cov(z_i, z_j) = S_fam(τ_eff) exactly as before.

## Parameters, from TRAIN genera only
Grid σ ∈ {0.6, 0.7, 0.8, 0.9, 1.0, 1.1}, θ ∈ {0.5, 1, 2, 4, 8, 16}. For each (σ, θ): 30 realisations per train genus
(≤ 30 genomes, seed 9004, same order as before); simulated pair log-ratio = log[trΓ(τ_eff)/trΓ(τ)] + log(χ²₁₃₅/135).
Loss = Σ over the five quantiles (5/25/50/75/95) of (sim − obs)² + Σ over the five τ-quintile SDs of (sim − obs)² +
(genus-share_sim − genus-share_obs)², quintile edges fixed from the observed τ. Domain-wide fit for all families;
families with ≥ 8 train genera get their own (σ, θ) by the same loss on their own pairs, others use the domain pair.
Adequacy gate (domain fit): max quantile error ≤ 0.15, max quintile-SD error ≤ 0.10, genus-share error ≤ 0.10;
if the gate fails the test is not run and the outcome is NOT DERIVED.

## Test and rules (identical to PREREG12a)
12 realisations × 10 Gaussian replicates per genus; baseline = PREREG11's fam draw (bit-identical). D0 baseline
identity (±0.005). D1 sign: Δ ≤ +0.02 for ≥ 85% of genera at ε ≥ 1.0. D2 aggregate and ε-shape: bacteria |residual| ≤
0.05 at every ε ≥ 0.79, archaea ≤ 0.10 at every ε. D3 per-family transfer at ε = 2 (families with ≥ 3 test genera):
Spearman ≥ 0.5 and slope in [0.5, 1.5]. D4 per-genus rank (reported only). D4′ coverage: |z_g| ≤ 2 for ≥ 85% of genera
and |mean z| ≤ 0.5, z from the 12 realisation means (SD floor 0.5 genome).
Verdict: DERIVED if D1, D2, D3, D4′ hold in bacteria and D2 holds in archaea; DERIVED (bacteria) / NOT REPLICATED
(archaea) if archaea fails D2 only; PARTIAL if D2 holds with exactly one of D3/D4′; NOT DERIVED otherwise.

## Final-attempt clause
This is the last derivation attempt on the Atlas arm. Whatever the outcome, no further model is fitted to this
residual: NOT DERIVED or PARTIAL closes the Atlas derivation with the drop recorded as a measured quantity (usable as
a calibration) and the mechanism recorded as supported at the level the passed rules justify; DERIVED closes it as a
term. The recorder arm (clumped writing as a stationary write-rate) and the hippocampal bridge proceed on their own
registrations. PREREG12 v1 remains on record as PARTIAL under a mis-specified marginal.

## Predictions stated now
Bacteria: D2 passes with the ε-shape flat as in v1, and the flat remainder shrinks below −0.04 because the marginal is
now right (my earlier "kernel bias" explanation is retracted; a correctly specified spread should leave less). D3
passes at a level near v1's (+0.62/0.77). Archaea: D1 resolves (mean rate 1 at every node); D2 is open, and with 20 of
35 genera on a domain fit and 3 of 9 families on the fallback kernel it is the weaker replication.

## Pre-run clarification — 2026-09-30 15:59
Numerical check: τ_eff = τ at σ = 0 (exact); node rates are stationary with mean 1 at every depth. Edge rates, taken as
the geometric mean of endpoint node rates, have mean exp(−σ²(1 − e^{−θℓ})/4) < 1 (0.87 at σ = 0.8, θ = 2, ℓ = 1; a few
percent for the short edges in these subtrees). The (σ, θ) fit to the observed marginal absorbs this; it is stated so
that σ is read as a fitted, not a directly measured, spread. Execution as PREREG12a: 3 bacterial parts + archaea,
2 BLAS threads each, nice, caffeinate.

## Outcome — 2026-09-30 16:03: bacterial GATE FAILED on train (registered stop) ⇒ NOT DERIVED; Atlas derivation closed
Bacteria domain fit σ = 0.9, θ = 8: quantile errors −0.16/+0.01/+0.04/−0.09/−0.18 (gate 0.15), τ-quintile SD errors
+0.04/+0.02/0.00/−0.06/−0.19 (gate 0.10), genus-share error +0.24 (simulated 0.66 vs observed 0.42; gate 0.10). No
(σ, θ) on the grid satisfies all three. The failure pattern is informative: to reproduce the DEEP pairs' spread (SD
0.58 at τ ≈ 0.43) a rate process must keep lineages correlated over long paths (small θ), but that raises the
genus-shared fraction far above the observed 0.42; with θ large enough to match the share, deep pairs average over
many edges and their spread collapses (−0.19). Observed deep pairs are heterogeneous WITHOUT being genus-shared. A
scalar rate cannot do that: at depth the heterogeneity is directional (lineages differ in where they move in
composition space, and convergence brings unrelated lineages closer than their divergence implies), which is the
"convergence balloon" named in the 9/25 mapping, not a clock. Archaea domain fit σ = 0.7, θ = 16 passed its gate
(quantile errors ≤ 0.11, SD errors ≤ 0.10, share +0.02); the runner stopped on the primary, and the archaeal test is
run below as registered, for the record (the verdict is NOT DERIVED regardless, since bacteria was not run).
Closure under the final-attempt clause: the drop at the Atlas is a MEASURED quantity (a calibration); the mechanism
"heritable heterogeneity below the genus" is supported at the level PREREG12 v1's passed rules justify (ε-shape
reproduced, per-family transfer +0.62/0.77) under a mis-specified marginal; no scalar-rate model fits the train
statistics; the remaining structure is directional and is a target for the harness (a directional trait process) or
for a measurement of convergence, not for another Atlas derivation.

## Archaea, run for the record — 2026-09-30 16:20: NOT DERIVED
Stationary clock (σ = 0.7, θ = 16, domain fit; all 35 genera on the domain pair). D0 PASS. D1 PASS (89–97%: the v1
sign failure resolved, as predicted, once the root was mean 1). D2 FAIL: residual at ε = 1.0/1.25/1.6/2.0 =
−0.044/−0.068/−0.101/−0.126 (from −0.072/−0.112/−0.149/−0.175), a 28% reduction against the ≤ 0.10 rule. D3 FAIL
(Spearman −0.19 over 8 families, 3 on the fallback kernel). D4′ FAIL: coverage 0.80, mean z = −0.52, a systematic
under-correction (observed counts sit below the model's realisations). Same reading as bacteria: a scalar rate
removes part of the drop and leaves a systematic, direction-shaped remainder. PREREG13 overall: NOT DERIVED; the
final-attempt clause stands as applied above.
