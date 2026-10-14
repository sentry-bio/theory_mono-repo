# PREREG20 — recorder arm results (main split; run 2026-10-09 02:05:14 CEST, 46 s; hashes in run_recorder_main.log;
# closure_recorder_main.json)

Writer: PREREG4 fit on the 60 train colonies (rec_fit.json); readout mixture from 240 short train cherries
(π = 0.136, ε_clean = 0.0005, ε_noisy = 0.268); correlated writer = internal donors + colony classes (R-mix, train only).
Scored on the 47 test colonies, 400 replicates; generations 1–5 gated (≥ 50 lineages).

## Stage counts (mean distinct lineages per colony; D̄_2∞ independent writer with infinite sites, D̄_2 finite sites,
## D̄_5 = D̄_2 read through the mixture, D̄_2′ correlated writer, D̄_5′ = D̄_2′ read; err = ln(predicted/observed))
| g | colonies | N̄ | r̄ edited sites | log₂ room | D̄_obs | D̄_2∞ | D̄_2 | D̄_5 | D̄_2′ | D̄_5′ | err_5 | err_5′ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 46 | 2.43 | 2.79 | 9.64 | 2.17 | 2.33 | 2.38 | 2.37 | 2.20 | 2.25 | +0.085 | +0.035 |
| 2 | 46 | 4.61 | 3.96 | 12.07 | 3.89 | 4.29 | 4.24 | 4.34 | 3.62 | 3.90 | +0.110 | +0.003 |
| 3 | 41 | 8.15 | 4.54 | 12.94 | 6.05 | 6.74 | 6.60 | 7.00 | 5.10 | 5.85 | +0.146 | −0.034 |
| 4 | 35 | 10.00 | 4.45 | 12.80 | 6.11 | 6.90 | 6.70 | 7.48 | 4.95 | 6.03 | +0.201 | −0.014 |
| 5 | 11 | 9.82 | 4.09 | 12.28 | 4.73 | 5.30 | 5.15 | 6.17 | 4.17 | 5.26 | +0.266 | +0.107 |
Simulation SDs of the stage means are 0.03–0.3 (0.3–0.6 at g = 5); see the JSON.

## Factors (ratios of log₂ counts)
| g | occupancy log N̄/log M | writer speed | collisions | correlation (sixth) | reading (six-factor) | reading (five-factor) |
|---|---|---|---|---|---|---|
| 1 | 0.133 | 0.951 | 1.026 | 0.907 | 1.030 | 0.993 |
| 2 | 0.183 | 0.953 | 0.992 | 0.890 | 1.058 | 1.016 |
| 3 | 0.234 | 0.910 | 0.989 | 0.863 | 1.084 | 1.032 |
| 4 | 0.260 | 0.839 | 0.985 | 0.840 | 1.124 | 1.058 |
| 5 | 0.268 | 0.730 | 0.983 | 0.872 | 1.162 | 1.110 |
Availability and retention are 1 by construction (stated in the registration).

## η (one operational definition, ε = 0; ε = 1 in brackets)
| g | η_obs | η_pred five-factor | η_pred six-factor | demand/room |
|---|---|---|---|---|
| 1 | 0.116 (0.122) | 0.129 | 0.121 | 0.133 |
| 2 | 0.162 (0.160) | 0.176 | 0.163 | 0.183 |
| 3 | 0.201 (0.189) | 0.217 | 0.197 | 0.234 |
| 4 | 0.204 (0.179) | 0.227 | 0.202 | 0.260 |
| 5 | 0.183 (0.156) | 0.214 | 0.195 | 0.268 |

## Rules
- CL1 five-factor closure: **FAIL**, as predicted (err_5 = +0.201, +0.266 at g = 4, 5; +0.146 at g = 3).
- CL2 six-factor closure: **PASS** (|err_5′| ≤ 0.035 at g ≤ 4; +0.107 at g = 5).
- CL3 residual at the writing stage: **PASS** (correlation factor < 1 at every gated g; |err_5′| < |err_5| at g ≥ 3).
- CL4 ordering at the deepest gated generation (g = 5, 11 colonies): **FAIL** — |log| writer 0.315 ≥ correlation
  0.137, but reading 0.150 > correlation; collisions 0.017 last. At g = 4 (35 colonies) the registered order holds:
  0.176 ≥ 0.174 ≥ 0.117 ≥ 0.015.
- **Verdict: CLOSURE LOCATED.** The audit closes on the recorder once the sixth loss named in advance (correlated
  writing: clumped edits and heritable quiet) is included, and the residual sits where predicted.

## Readings (separate from the verdict)
1. The independent-site writer over-predicts distinct lineages by a margin that grows with depth (+9% → +31%); the
   correlated writer removes it. Correlated writing costs 9–16% of the lineage bits at every generation.
2. The reader does not lose bits here; it fabricates them. The readout mixture raises the distinct count by 3–16%
   (reading factor 1.03–1.16): a noisy cell (13.6% of cells, 27% per-site error) creates spurious fixed edits in
   small clades, so lineages that share a tape are read as different. This violates the audit's `Lossy` assumption
   at the reading stage and is a finding, not a defect of the test: a reader can overcount, and a closure test that
   only allowed losses would have mis-attributed it to writing.
3. Collisions are negligible on a ten-site, two-state tape (factor 0.98–1.03).
4. The recorder's η rises from 0.12 to 0.20 over generations 1–4 and dips at 5; it is three-quarters of the demand
   (η/occupancy = 0.78–0.89): the tape retains most of the lineage bits the tree generates, inside a room it occupies
   to a quarter (r̄ ≈ 4 edited sites of 10, log₂ M ≈ 12–13 bits against log₂ N̄ ≈ 1–3 bits).
5. For the one-page theory: the audit identity is now a measured chain on one medium, with its sixth loss named
   and sized; the efficiency table's recorder row gets a number with a provenance.

## Replication on the swap split (writer re-fitted on the 47 by L-BFGS-B, converged, −log L 3408.7; readout mixture
## from 164 cherries π = 0.096, ε_noisy = 0.236; scored on the 60; run 02:08:19 CEST, 112 s)
| g | colonies | N̄ | r̄ | log₂ room | D̄_obs | D̄_2∞ | D̄_2 | D̄_5 | D̄_2′ | D̄_5′ | err_5 | err_5′ | η_obs |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 60 | 2.40 | 2.79 | 9.65 | 2.13 | 2.27 | 2.31 | 2.30 | 2.09 | 2.14 | +0.076 | +0.003 | 0.113 |
| 2 | 60 | 4.47 | 4.15 | 12.37 | 4.05 | 4.24 | 4.21 | 4.25 | 3.54 | 3.70 | +0.047 | −0.089 | 0.163 |
| 3 | 55 | 8.04 | 4.86 | 13.41 | 6.09 | 6.84 | 6.71 | 6.93 | 5.38 | 5.81 | +0.130 | −0.047 | 0.194 |
| 4 | 45 | 10.18 | 4.97 | 13.57 | 6.49 | 7.51 | 7.32 | 7.78 | 5.85 | 6.48 | +0.182 | −0.001 | 0.199 |
| 5 | 18 | 11.89 | 5.03 | 13.65 | 6.44 | 7.28 | 7.05 | 7.78 | 5.96 | 6.74 | +0.188 | +0.044 | 0.197 |
Factors: writer speed 0.94/0.97/0.92/0.87/0.80; collisions 1.02/1.00/0.99/0.99/0.98; correlation
0.88/0.88/0.88/0.89/0.91; reading (six-factor) 1.03/1.04/1.05/1.06/1.07.
CL1 FAIL as predicted (err_5 = +0.182/+0.188 at g = 4/5); CL2 PASS (|err_5′| ≤ 0.089); CL3 PASS; CL4 PASS at g = 5
(|log| writer 0.221 ≥ correlation 0.090 ≥ reading 0.066 ≥ collisions 0.016). **Verdict: CLOSURE LOCATED** on the
replication as well, with the ordering rule holding here (18 colonies at g = 5 against 11 on the main split).
η_obs 0.11–0.20 matches the main split within 0.01 at every generation.

The Atlas arm is reported separately (RESULTS_PREREG20_atlas.md) when it finishes.
