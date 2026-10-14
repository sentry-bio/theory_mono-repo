# RESULTS — PREREG24, the audit in mutual information (intMEMOIR, both splits)

Registration frozen 2026-10-14 05:15:35 CEST; amendments (i) analytic readout 05:18:22 and (ii) model-critic
observed estimator 05:19:51, each after a disclosed smoke test and before any verdict run; verdict runs (main 47
test colonies, swap 60) launched 05:20 CEST, 400 replicates, 200 permutations (per `run.log` and
`mi_closure_{main,swap}.json`). Scored by the registered rules; verdicts first, readings after.

## Verdict: NOT AS REGISTERED on both splits — the chain is ordered, the symptom resolves, closure fails

| Verdict | Rule | main | swap |
|---|---|---|---|
| MI1 chain ordered | every MI factor ≤ 1.02 at gated g | PASS (0.65–0.87) | PASS (0.65–0.87) |
| MI2 symptom resolves | reading_MI < 1 wherever the count-based reading factor exceeded 1 | PASS (reading_MI 0.80–0.82 against count 0.99–1.11; reading6_MI 0.81–0.82 against 1.03–1.16) | PASS (0.86–0.87 against 1.00–1.05; 0.86–0.87 against 1.03–1.07) |
| MI3 closure | \|ln(η_pred6 / η_obs)\| ≤ 0.15 at gated g | FAIL: η_obs is negative at every g (−0.04 to −0.07) | FAIL (−0.04 to −0.07) |
| MI4 consistency | η_MI,obs ≤ η_count,obs | PASS (trivially, η_MI,obs < 0) | PASS |

Gated generations 1–5 on both splits.

## The information chain (main split; swap in parentheses), bits

| g | log₂ M | I(ℓ;X_∞) | I(ℓ;X_dist) | I(ℓ;X_read) | I(ℓ;X_corr) | I(ℓ;X_read6) | fill | collisions | reading | correlation | reading6 | η_pred6 | I_obs,model6 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 9.6 | 1.14 (1.09) | 0.80 (0.71) | 0.64 (0.61) | 0.58 (0.49) | 0.47 (0.42) | 0.12 | 0.70 (0.65) | 0.80 (0.86) | 0.72 (0.68) | 0.81 (0.86) | 0.049 (0.043) | −0.38 (−0.35) |
| 2 | 12.1 | 1.92 (1.90) | 1.42 (1.33) | 1.15 (1.15) | 0.99 (0.88) | 0.81 (0.77) | 0.16 | 0.74 (0.70) | 0.81 (0.86) | 0.70 (0.67) | 0.81 (0.87) | 0.067 (0.062) | −0.72 (−0.66) |
| 3 | 12.9 | 2.56 (2.58) | 1.95 (1.87) | 1.58 (1.62) | 1.32 (1.25) | 1.08 (1.09) | 0.20 | 0.76 (0.72) | 0.81 (0.87) | 0.68 (0.67) | 0.82 (0.87) | 0.083 (0.081) | −0.96 (−0.98) |
| 4 | 12.8 | 2.36 (2.53) | 1.83 (1.88) | 1.50 (1.63) | 1.27 (1.32) | 1.04 (1.15) | 0.18 | 0.78 (0.74) | 0.82 (0.87) | 0.69 (0.70) | 0.82 (0.87) | 0.081 (0.085) | −0.90 (−0.87) |
| 5 | 12.3 | 1.88 (2.34) | 1.50 (1.75) | 1.23 (1.52) | 1.16 (1.38) | 0.96 (1.20) | 0.15 | 0.80 (0.75) | 0.82 (0.87) | 0.77 (0.79) | 0.82 (0.87) | 0.078 (0.088) | −0.89 (−0.93) |

## Readings (not scored)

1. **The audit closes in states and fails in information.** PREREG20 located closure for the *number* of distinct
   records (six-factor chain within 0.035–0.107 in log). The same model, asked which record belongs to which
   lineage, is anti-informative on the real colonies: the average log-likelihood ratio of a real leaf record under
   its own lineage's model distribution against the leaf-weighted mixture is −0.35 to −0.98 bits at every
   generation on both splits (standard errors of order 0.1 bits). The independent writer is worse than the correlated
   one (−0.49 to −1.57 bits). A model whose lineage-conditional distributions were right would give a non-negative
   value in expectation. So the real colonies carry lineage-specific structure the writer does not place: which
   sites a given lineage edited, and how active it was, are not predictable from branch length and site usage even
   with the colony-level activity classes of the correlated writer. This is the quantitative form of PREREG20's
   "heritable quiescence" residual, and it means the recorder's readable genealogy is below what the count-based
   closure implied.
2. **The reading factor above one was the measure, not the reader.** In information the reading factor is
   0.80–0.87 on every generation and split; the state-count version (0.99–1.16) counted readout noise as
   distinctness. The pooled plug-in estimator of the readout stage reproduces the same inflation (20–45% above the
   exact value even with 400 replicates), which is why amendment (i) computed that stage analytically.
3. **Information efficiencies are lower than state efficiencies.** η_MI,pred6 = 0.04–0.09 against η_count,obs =
   0.12–0.20 at the same generations; the fill factor (information written against room) is 0.12–0.20, collisions
   0.65–0.80, reading 0.80–0.87, correlation 0.67–0.79.
4. **The null-subtracted plug-in** (0.00–0.45 bits) and the raw plug-in (1.0–2.3 bits, equal to H(ℓ) when records
   are unique) bracket nothing useful, as amendment (ii) anticipated; they are reported for the record.

## What this does and does not establish
Established: the data-processing chain orders the recorder's audit by construction, the count-based reading
anomaly was an artefact of counting states, and the information-level closure fails on both splits with a
consistent sign: the real colonies are less lineage-predictable than the fitted writer. Not established: a writer
model that closes in information; whether a lineage-specific activity model (heritable rate per lineage) would.
That is the next registration for the recorder arm.
