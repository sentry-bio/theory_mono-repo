# PREREG22 — Two-reader rate-spectrum horizon (synthetic)

Registered 2026-10-14, clock time at freeze in `run.log` (the `date` line precedes the file hashes). Written
before any verdict data were generated. The derivation it tests is `paper2/RATE_TAIL_DERIVATION.md`
(same date, written first). Supersedes the unarchived Gamma(0.5) run quoted in Paper II vG §5.3.

## Claim under test
Readable depth of a quartet (distance) reader on a Jukes–Cantor tape of L sites with Gamma(a) site rates is
given by the exact signal-to-noise curves of the derivation (§2–3), with the asymptotic exponents
1/(2(a+1)) for the unweighted mismatch reader and 1/(a+2) for the rate-weighted contrast reader, and the
logarithmic law (3/16) ln L for uniform rates, where the two readers coincide.

## Fixed design (frozen with this file; hashes in run.log)
- Simulator: `horizon22.py` (sim / predict / score). Jukes–Cantor, four letters, quartet AB|CD, tips at
  duration t below the internal nodes, internal branch τ = 1.0. Depth unit: expected substitutions per site at
  the mean site rate (Gamma mean fixed at 1).
- Readers: (U) unweighted four-point mismatch reader; (W) oracle rate-weighted contrast reader with per-site
  weights s_i/v_i computed from the true r_i and the true t. Both read the same simulated data.
- Success criterion: true split returned with probability P₀ = 0.90; t*(L) found by bracketing and 12
  bisection steps on t with 2000 quartets per evaluation. Each evaluation's RNG is seeded by
  sha256(seed=22 | a | L | t | τ).
- Shapes a ∈ {0.5, 1.0, ∞}. Sites L ∈ {256, 512, 1024, 2048, 4096, 8192, 16384, 32768}.
- Prediction: κ (one nuisance constant per reader) is fitted on the single cell a = 0.5, L = 256, and every
  other cell is predicted by solving SNR(L, t) = κ with the exact per-site s, v of the derivation integrated
  over 400,000 fixed-seed Gamma(a) rate draws. The a = ∞ cells are predicted with the same κ.

## Verdicts (one per claim; scored by `horizon22.py score`, rules fixed here)
- V1 form, unweighted: every predicted cell (a ∈ {0.5, 1.0}, excluding the fit cell) within ±10% of observed t*.
- V2 form, weighted: same rule, weighted reader.
- V3 slopes: for each (a ∈ {0.5, 1.0}, reader) the observed log–log slope over the top three L values is within
  ±0.03 of the exact-curve slope over the same values. The asymptotic exponents are reported beside as a
  reading, not a verdict (the derivation §5 says the asymptote is approached from above at these L).
- V4 ordering: at a ∈ {0.5, 1.0} the weighted reader's t* exceeds the unweighted at every L, and the ratio at
  L = 32768 exceeds the ratio at L = 256 (the exponents differ).
- V5 uniform-rate control: at a = ∞ both readers' t* are linear in ln L with slope within ±15% of 3/16, and the
  two readers' t* agree within 5% at every L.
Overall: the law is CONFIRMED only if V1–V5 all pass; any failure is reported as such with its cell values.
No post-hoc change of tolerance, grid, κ-fit cell or reader definition is permitted; any amendment must be
dated and precede the data it concerns.

## Disclosed smoke test
Before the verdict runs: a = 0.5, L ∈ {256, 1024}, 200 quartets per evaluation, same code paths. Its output is
kept (`smoke.json`) and no verdict is read from it. If it reveals a code error, the fix is dated in this file
under "Amendments" before the verdict runs start.

## Readings (reported, not scored)
- Local slopes vs asymptotic exponents at each a; the implied Fusi–Abbott–Benna cascade correspondence.
- The fitted κ per reader against Φ⁻¹(0.90) = 1.28.

## Amendments
- 2026-10-14 04:29 CEST per `run.log` (first written as 04:31, corrected to the log at 04:30 before any
  verdict data were read; the verdict runs launched at 04:29:36 per the log), before any verdict run: `simulate_success` now draws replicates in batches of 250 and
  uses int8 letters (memory at L = 32768 × 2000 quartets would otherwise exceed the machine). Statistics,
  readers, grid, criterion and seeds are unchanged; the per-evaluation RNG stream differs from the smoke run's,
  so the smoke numbers are not bitwise reproducible by the amended code. Re-hashed in `run.log`.
