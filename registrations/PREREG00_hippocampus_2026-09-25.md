# Pre-registration: addressability efficiency of CA1 during first exposure to a 1-D track

Written 2026-09-25 before any spike data from DANDI:000044 was analysed. Only
metadata (epoch table, unit counts, position series shapes) had been read.

## Data
DANDI:000044 v0.250624.0426 (Grosmark & Buzsáki 2016, CC-BY-4.0): 8 sessions,
4 rats. The novel maze epoch (~40 min) is on a 1.6 m linear track, a 2 m linear
track, or a 1 m circle. We use excitatory CA1 units only, running periods only
(speed > 5 cm/s) unless stated.

## Quantities
- Familiarity T: cumulative running time on the maze at the window centre.
- Windows: fixed length (10 min), stepped by 5 min. Fixed length is required
  because the topological radius estimate grows with window length (Zhang et al.
  ED Fig. 9b).
- Demand beta: Eq. 2 of Zhang et al. gives 1 nat per e-fold of T once T >> t0.
  Secondary, empirical: the growth per e-fold of decoded positional information
  (Bayesian decoder, leave-one-lap-out).
- Room R, primary: topological radius. We fit Betti curves (beta1, beta2 of the
  clique complex of the pairwise-correlation matrix) against uniform samples from
  unit-curvature H^d, taking the R with the best product of p-values, as in Zhang
  et al. The dimension d is fitted per session on the whole maze epoch; h = d - 1.
- Room R, secondary: field-size exponent. zeta is the truncated-exponential MLE
  (Eqs. 7-9), with R = zeta * s_max and s_max = the fixed upper truncation. This
  gives h = 1 (H^2: 1-D space plus scale). Absolute eta from this estimator
  depends on the s_max convention; its slope is reported, not claimed.
- Slope a = dR/d ln T, pooled across sessions (session-level fits combined by
  inverse-variance weighting). eta = beta / (h * a).

## Hypotheses and decision rules
- H_sat (saturation): eta = 1. Supported if the pooled 95% CI of eta contains 1
  and its lower bound is > 0.6.
- H_opt (Fisher operating point, as found in the familiar 2-D box): eta ~ 0.4.
  Supported if the CI contains 0.4 and its upper bound is < 0.8.
- H_kin (kinematic artefact), which gates the field-size estimator: if the
  familiarity slope of field size vanishes once speed is matched (CI includes 0)
  while the unmatched slope does not, the field-size expansion is attributed to
  running speed and not interpreted.
- Otherwise: inconclusive. We report it as such and do not re-analyse with new
  choices to reach a decision.

## Fixed analysis choices (not to be tuned after seeing results)
- 2 cm spatial bins; 3 cm Gaussian smoothing.
- A place field is a contiguous region with rate > max(1 Hz, 0.2 * peak) and a
  peak >= 2 Hz; the two running directions are treated separately.
- Correlation matrix: Zhang et al.'s CCG-integral correlation, tau_max = 1 s,
  units with 0.1-7 Hz mean rate in the window. The same unit set is used for all
  windows of a session.
- R grid 3:0.5:24; 200 model replicates per (d, R, N); multiplicative noise 0.05.
