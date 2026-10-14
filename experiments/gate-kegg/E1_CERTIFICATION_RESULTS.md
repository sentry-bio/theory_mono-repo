# E1 — Meter Certification: Results

**Run date:** 2026-08-13
**Protocol:** `theory/DECISIVE_EXPERIMENTS.md` :: E1, branch `cursor/rigorous-mathematical-spine-2c19` (PR #5)
**Estimators under test:** `tools/addressability_meter.py` — `measure_ball_growth` (M3), `measure_quartet_defect` (M4). M2 (radial rate) implemented here, as the doc lists it open and no implementation exists in the repo.
**Baseline:** the repo's own 6 unit tests pass (`pytest tests/test_addressability_meter.py`).

---

## Headline

| Estimator | Verdict |
|---|---|
| **M2** (radial rate `c`) | **CERTIFIED** — exact recovery, 0.00% error in all 16 cells, r = 1.0000 |
| **M4** (tree defect `δ`) | **CERTIFIED** — exactly 0 on pure trees at every `b`, tracks reticulation r = 0.946, orthogonal to branching factor |
| **M3** (packing entropy `h_pack`) | **NOT CERTIFIED as a single-point estimator** — see below |

M3 passes the doc's stated correlation thresholds but fails on absolute accuracy, on the Euclidean-null criterion, and under non-stationarity. A fix is implemented and validated at the end of this document.

---

## Arm A — M2/M3 absolute recovery on exact-radius hyperbolic ground truth

Grid: `b ∈ {2,3,4,5}` × `κ ∈ {0.5,1,2,4}`, exact-radius construction (radius exactly `c·R`, so `c` and `h_pack` are known analytically), subsampled to fixed n = 700 with the root always preserved.

- **M2:** r = 1.0000 vs true `c`; median and max absolute error **0.00%**. Exact in every cell.
- **M3:** r = 0.9744 vs true `√κ` → **passes** the doc's `r > 0.95`. But absolute error: median 2.73%, **max 16.02%** → fails a 15% absolute threshold.

**The consequential finding:** the grid is constructed so that `η = β/(c·h_pack) = 1` exactly in every cell. Measured η ranged 0.873–1.191, with **11 of 16 cells returning η > 1** — apparent violations of the framework's fundamental bound `β ≤ c·h_pack`, arising purely from M3 estimator error on data that sits exactly at the bound.

E1's kill rule reads *"Kill (instrument/bound): η > 1 at certified estimators."* As things stand, M3 manufactures that signature at a 69% rate on clean synthetic data. A field measurement of η ≈ 1.05 could not be distinguished from estimator noise. **The instrument's error bar is wider than the effect it exists to detect.**

Error tracks the number of usable radial shells (`fit_points`): b=2 cells get 6–7 points and ≤5.9% error; b=5 cells get 4 points and up to 16% error.

## Arm B — M3/M4 orthogonality under reticulation

Graph metric on b-ary trees, shortcut fraction `f ∈ {0, 0.01, 0.05, 0.25}`.

| Check | Result | Threshold | Verdict |
|---|---|---|---|
| M3 vs true `ln b` | r = 0.9712 | > 0.95 | PASS |
| M3 vs reticulation `f` | r = 0.0394 | \|r\| < 0.1 | **PASS** |
| M4 vs reticulation `f` | r = 0.9458 | tracks f | PASS |
| M4 vs branching `b` | r = −0.1334 | small | PASS |
| M4 exact fraction at f=0 | 1.000 at every b | ≈ 1.0 | PASS |

**This reproduces the orthogonality claim that `DECISIVE_EXPERIMENTS.md` cites `kernel_orthogonality.py` for.** That file does not exist anywhere in the repository, so the "partially done" status was not independently checkable; it is now. The claim holds: δ tracks reticulation while h_pack ignores it, and δ is exactly zero on pure trees at every branching factor.

M3's absolute error remains high here (median 3.8%, max 21.0%), again concentrated where few radial shells are available.

## Arm C — Euclidean / product-space nulls  ← **the failure**

Doc criterion: *"Euclidean nulls give M3 exponential rate consistent with zero."*

| Host | n | M3 slope |
|---|---|---|
| 2D grid, side 20 | 400 | 0.2051 |
| 2D grid, side 40 | 1600 | 0.1103 |
| 3D grid, side 10 | 1000 | 0.3697 |
| 3D grid, side 12 | 1728 | 0.3220 |
| Euclidean MST | 1500 | 0.0245 |
| *(hyperbolic, √κ=0.707, for contrast)* | 1093 | *0.594* |

A polynomial-growth 3D grid returns 0.32 against 0.59 for a genuine hyperbolic host — within a factor of two. **Not consistent with zero.**

A scaling check confirms the estimator is *asymptotically consistent* but converges slowly:

```
2D grid:  n=100 -> 0.348   n=400 -> 0.205   n=1600 -> 0.110      (true 0)
3D grid:  n=216 -> 0.539   n=1000 -> 0.370  n=1728 -> 0.322      (true 0)
binary tree: n=255 -> 0.744  n=1023 -> 0.733  n=4095 -> 0.726    (true ln2 = 0.693)
```

The tree is stable across a 16× size range; the grids decay toward zero but are still far from it at sizes typical of real phylogenetic datasets.

**Why this matters beyond E1.** Corollary 4.3 (polynomial-growth exclusion) — *"no polynomial-growth host can represent retained exponential novelty"* — is described in the spine as "the coordinate-free content of the theory." E5 makes it a kill line (*"Kill: a Euclidean host successfully carries retained exponential novelty at finite c"*). The instrument designated to test that cannot currently separate a polynomial host from a hyperbolic one at realistic sample size.

This is the same failure mode the collapse preregistration records for the older `tri_kappa` estimator (*"returned 0.18–0.47, tracking dimension"*). `certified_volume_entropy.py` in `experiments/universality/` has a "flat null → exactly 0" gate for precisely this reason. **`tools/addressability_meter.py`, which `DECISIVE_EXPERIMENTS.md` designates for M3, does not have that gate.**

## Arm D — Non-stationary rate schedules *(listed OPEN in the doc)*

| Schedule | true β | M3 error | η (true = 1) |
|---|---|---|---|
| stationary b=3 | 1.099 | 5.5% | 1.058 |
| **step 2→4** | 1.089 | **25.0%** | **0.800** |
| ramp 2→5 | 1.138 | 6.9% | 1.074 |
| decel 5→2 | 1.170 | 11.4% | 1.128 |

A step change in branching rate produces 25% error in M3 and drives η to 0.80 on data that sits exactly at η = 1. Non-stationarity would be read as *failed saturation*. This arm was correctly flagged open; it now has a result, and it is a failure.

---

## Fix: a growth-class gate for M3 (implemented and validated)

A first attempt — a size-scaling gate over nested random subsamples — **failed**, and the reason is worth recording: randomly thinning points from a fixed matrix does not shrink the space, so the slope does not decay (all decay slopes came out positive, and the gate classified 6/12 correctly, i.e. it called everything exponential).

The correct discriminator requires no subsampling and reuses the occupancy curve the meter already computes:

- exponential host: `P(ρ) ~ exp(hρ)` ⟹ `log P` linear in `ρ`
- polynomial host: `P(ρ) ~ ρ^d` ⟹ `log P` linear in `log ρ`

Fit both; compare adjusted R². Results:

| Host class | R²(exponential) | R²(polynomial) | Verdict |
|---|---|---|---|
| Trees b=2,3,4 | 0.9988–0.9999 | 0.923–0.934 | exponential |
| H² at κ=0.5,1,2 | 0.9998 | 0.926 | exponential |
| 2D grids | 0.855–0.914 | 0.987 | polynomial |
| 3D grids | 0.909–0.927 | 0.984–0.985 | polynomial |
| Euclidean MSTs | 0.780–0.796 | 0.981–0.990 | polynomial |

**13/13 correctly classified, with no overlap between classes.** The recovered polynomial dimension also orders correctly (2D grids ≈ 1.5–1.6, 3D grids ≈ 1.95–2.0).

Proposed rule: **M3 may report a packing entropy only when the exponential model wins.** When the polynomial model wins, `h_pack = 0` by Corollary 4.3 and the slope is a finite-window artifact. This makes the polynomial-growth exclusion mechanically enforceable rather than an assumption.

Code: `m3_growth_class.py` (gate), `e1_certification.py` (generators), `run_e1.py` (battery), `e1_results.json` (raw).

---

## Recommended amendments to `DECISIVE_EXPERIMENTS.md`

1. **Add an absolute-error threshold to E1.** Correlation is scale-blind; h_pack enters η as an absolute number. r = 0.9744 coexists with 16% error here.
2. **Pin the E1 generator construction.** The natural b-ary hyperbolic embedding (composed boosts at the theory-saturating edge length) has severe radial drift — measured mean radius 2.07 vs c·R = 4.16 at depth 6, giving ĉ = 0.24 against c_true = 0.69. That is embedding distortion, not estimator error, and E1 currently conflates the two failure modes. The exact-radius construction used here separates them.
3. **Adopt the growth-class gate as part of certified M3**, so Corollary 4.3 and E5's Euclidean kill line are enforceable.
4. **Add a minimum-radial-shells precondition.** Error tracks `fit_points` directly; cells with 4 shells carry 3–4× the error of cells with 7.
5. **Correct two status claims.** `kernel_orthogonality.py` is cited twice but absent from the repo; the independence firewall is described as mechanically enforced (*"the meter already refuses this"*) but `addressability_meter.py` has no provenance tagging — the separation is a CLI convention, not a runtime check. Both are straightforward to implement; the orthogonality result they refer to does replicate (Arm B).

## Bearing on the wider protocol

E3–E8 all compute η through M3. Until M3 carries the growth-class gate and a stated absolute error bar, an η within roughly ±20% of 1 is not interpretable — which is the entire decision range for E3 (`η ≥ 0.8` = saturation) and E5 (`η → 1` vs controls "well below 1"). **E1 is correctly placed as the gate on everything else, and it does not currently pass.**
