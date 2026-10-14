# RESULTS — PREREG22, two-reader rate-spectrum horizon (synthetic)

Registration frozen 2026-10-14 04:28:48 CEST; amendment (batching, memory) 04:29:36 CEST; verdict runs launched
04:29:36 CEST; prediction and scoring 04:55:02 CEST (all per `run.log`; simulation start/finish stamps in
`sim_a05.json`, `sim_a10.json`, `sim_ainf.json`). Scored by `horizon22.py score` with the rules fixed in the
registration. Verdicts first, readings after.

## Verdict: LAW CONFIRMED IN SIMULATION (V1–V5 all pass)

| Verdict | Rule | Result |
|---|---|---|
| V1 form, unweighted | predicted t*(L) within ±10% at every non-fit cell, a ∈ {0.5, 1.0} | PASS, max |rel err| 0.025 |
| V2 form, weighted | same, weighted reader | PASS, max |rel err| 0.084 |
| V3 slopes | observed log–log slope over the top three L within ±0.03 of the exact-curve slope, each (a, reader) | PASS (largest gap 0.017) |
| V4 ordering | weighted t* > unweighted at every L, ratio at 32768 > ratio at 256 | PASS |
| V5 uniform-rate control | both readers linear in ln L with slope within ±15% of 3/16; readers agree within 5% | PASS (slope 0.190 vs 0.1875; readers identical) |

κ fitted once per reader on the cell a = 0.5, L = 256: unweighted 1.074, weighted 0.898 (reading: Φ⁻¹(0.90) = 1.28;
the three-way decision and the Gaussian approximation account for the difference). Every other cell predicted with
no free parameter.

## Observed / predicted readable depth t*(L), in mean substitutions per site (P₀ = 0.90, τ = 1.0)

| a | reader | 256 | 512 | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 |
|---|---|---|---|---|---|---|---|---|---|
| 0.5 | unweighted | 1.26 / 1.26 (fit) | 1.67 / 1.69 | 2.25 / 2.22 | 2.92 / 2.89 | 3.82 / 3.73 | 4.85 / 4.79 | 6.27 / 6.12 | 7.72 / 7.79 |
| 0.5 | weighted | 2.00 / 2.00 (fit) | 2.76 / 2.76 | 3.91 / 3.76 | 5.40 / 5.09 | 7.06 / 6.84 | 9.87 / 9.15 | 13.21 / 12.19 | 17.51 / 16.20 |
| 1.0 | unweighted | 1.26 / 1.27 | 1.61 / 1.61 | 2.04 / 2.03 | 2.54 / 2.52 | 3.10 / 3.11 | 3.81 / 3.81 | 4.60 / 4.64 | 5.56 / 5.64 |
| 1.0 | weighted | 1.81 / 1.88 | 2.43 / 2.49 | 3.22 / 3.25 | 4.24 / 4.21 | 5.52 / 5.43 | 7.00 / 6.96 | 8.97 / 8.90 | 11.38 / 11.33 |
| ∞ | unweighted | 0.94 / 0.96 | 1.07 / 1.10 | 1.20 / 1.23 | 1.34 / 1.36 | 1.47 / 1.49 | 1.61 / 1.62 | 1.74 / 1.75 | 1.86 / 1.88 |
| ∞ | weighted | 0.94 / 1.03 | 1.07 / 1.16 | 1.20 / 1.30 | 1.34 / 1.43 | 1.47 / 1.56 | 1.61 / 1.69 | 1.74 / 1.82 | 1.86 / 1.95 |

At a = ∞ the oracle weights are equal across sites, so the two readers make identical decisions by construction;
the weighted prediction at a = ∞ carries the weighted κ and sits 8–9% high, inside V5's 15% rule.

## Readings (not scored)

Local log–log slopes over L ∈ {8192, 16384, 32768} against the exact-curve slope and the asymptotic exponent:

| a | reader | observed | exact curve | asymptote |
|---|---|---|---|---|
| 0.5 | unweighted | 0.335 | 0.351 | 1/3 |
| 0.5 | weighted | 0.413 | 0.412 | 0.400 |
| 1.0 | unweighted | 0.271 | 0.282 | 0.250 |
| 1.0 | weighted | 0.351 | 0.351 | 1/3 |

The weighted reader's advantage grows with L as the derivation requires (ratio 1.58 → 2.27 at a = 0.5, 1.44 →
2.05 at a = 1.0). The weighted observed depths run 3–8% above the exact prediction at the largest L, uniformly in
sign: the constant-variance approximation in the predictor undercounts the slow sites' contribution slightly; the
exponent is unaffected (V3).

On the superseded figure: the earlier unarchived Gamma(0.5) run's 0.39 lies between this run's unweighted (0.335)
and weighted (0.413) local slopes and cannot be assigned to a reader; it is replaced by this record.

## What this does and does not establish
Established: in the model, readable depth of a distance reader follows the exact Fisher curves of
`RATE_TAIL_DERIVATION.md`, with the two reader-dependent exponents and the logarithmic law at uniform rates. Not
established: anything about real alignments (PREREG23), or about the best (census) reader, whose ceiling is the
Kesten–Stigum second-moment line and is not tested here.
