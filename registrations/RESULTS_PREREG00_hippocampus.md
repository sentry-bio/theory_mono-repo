# Addressability efficiency of hippocampal maps — results (2026-09-25)

Question: does CA1 run on the equality face of the addressability limit
(beta = c * h_pack)? The candidate case was 1-D tracks, where Zhang et al.
(Nat Neurosci 2023) report hyperbolic H^2 expansion with familiarity.

## 1. Published source data (Zhang et al., 2-D box, H^3) — `code/eta.py`
- Radius grows a = dR/dlnT = 1.32 (95% CI 0.83–1.98). eta = 1/(2a) = 0.38 (0.27–0.58).
- Saturation needs a = 0.5. It is excluded in every resampling, including a
  cluster bootstrap over exposure blocks.
- This matches the paper's own Fisher-optimal model (dR/dlnN = 1.23, eta ~ 0.41).

## 2. Original 48-m track (CRCNS hc-31), the authors' own place fields — `results/hc31.txt`
- 2,710 accepted fields from 5 rats. Familiarity is measured as cumulative
  exposure to the field's track section (about 100 s to 1,000 s), not as inverse
  speed as in the paper's Fig. 3d.
- Field size ∝ speed^0.50 (mean pass speed; 0.33 for first-pass speed, matching Fig. 3e).
- Net of speed, the familiarity effect on field size is +0.004 per e-fold
  (animal-bootstrap 95% CI −0.013 to +0.019).
- H^2 saturation would need about −0.33 to −0.5 per e-fold; the Fisher
  operating point about −0.8. Both are excluded.
- Conclusion: the track "expansion with familiarity" is a running-speed effect.
  In Fig. 3d familiarity was defined as 1/speed, so the two were never separable.

## 3. Independent replication, DANDI:000044 (Grosmark & Buzsáki; 8 sessions, 4 rats) — `results/summary.txt`
Pre-registered in `code/PREREGISTRATION.md`.
- Kinematic gate triggered. Field-size slope vs familiarity: raw +0.039, but
  speed-matched −0.014 (CI −0.053 to +0.025). Field-level, net of speed: −0.034 ± 0.014.
- Topological radius: no growth, pooled h·a = −0.20 (CI −0.54 to +0.14).
  - Caveat: the estimates sit near the pre-registered grid ceiling (R ≈ 19–24).
  - Recovery tests show the estimator is identifiable there but noisy (±3).
  - Treat this estimator as weak.
- Decoded positional information grows only 0.06 nats per e-fold, about 16x
  below the paper's Eq. 2 maximum-information demand.
- Pre-registered decision: neither H_sat nor H_opt supported.

## Bottom line
- On 1-D tracks there is no detectable representational expansion with
  familiarity over the minutes-to-hour range once speed is controlled. The H^2
  saturation hypothesis fails in both datasets.
- The only real-data eta remains the 2-D box, about 0.4, across days.
- The addressability bound is far from binding for place codes at these scales:
  room (e^R) vastly exceeds what the code actually resolves.

## Not tested
- The first one or two passes (seconds scale). Fields here are defined over 3–5 passes.
- Timescales of days or more on the tracks.

## Data conditions
- hc-31: publications using it must list P. Dylan Rich and Albert K. Lee as
  authors, or discuss this with them.
- DANDI:000044: CC-BY-4.0.
- Raw data was deleted from biosphereatlas after import. To re-fetch:
  - hc-31: `code/fetch.sh` with a CRCNS login.
  - DANDI: `code/extract.py`, which streams it; no login needed.
