# PREREG14 — the hippocampal bridge (registered 2026-10-04, before any hc-31 or DANDI spike data of this run was read)

## Claim
The ladder that predicts heritable memory predicts the hippocampal position code's resolvable states: a homogeneous
Gaussian image with matched second moments over-counts distinguishable position states (the sign law, i.e. the
data-processing inequality in a neural medium), and restoring the observable heterogeneity of the code closes the gap
with nothing fitted. If it holds, the frame is a theory of memory; if the sign law fails, it is a theory of heredity.

## Mapping (fixed)
- Lineages → position states: 10-cm bins along the track (hc-31, 48 m) or 5-cm bins (DANDI tracks, 1.6–2 m);
  running direction kept separate (two directional tracks per session); running periods only (speed > 5 cm/s).
- Image → population vector of excitatory CA1 units with ≥ 50 spikes in the epoch, as lap-averaged square-root rates
  (variance-stabilising for counts; raw rates as a sensitivity, reported). Each session is reduced to its top 40
  principal components of the bin × unit matrix (fewer if fewer units), applied identically to observed and simulated.
- Reader ε → split-half noise floor: the median Euclidean distance between odd-lap and even-lap averages of the same
  bin (ε_halves), per directional track. ε grid: {0.5, 0.75, 1, 1.5, 2} × ε_halves.
- τ → track distance |Δx| between bins; the kernel C(Δx) (a 40 × 40 matrix per 10-cm lag) is the empirical covariance
  of the track-mean-centred bin vectors at lag Δx, stationary along the track.
- Heterogeneity → the per-bin signal variance profile v_i = ‖z_i − μ‖² − noise_i, smoothed over ±1 bin; s_i = v_i / mean v.
- Noise → per-bin residual noise of the lap mean, estimated from the odd/even half difference ((odd − even)/2, squared,
  per component), added to every simulated bin.

## Three images
- G0 (homogeneous rung): Gaussian process along the track with kernel C(Δx), plus noise. The matched-second-moment null.
- G1 (heterogeneity restored): Cov(i, j) = √(s_i s_j) · C(Δx_ij), plus noise. Direction structure stays stationary by
  design; a remainder after G1 is the direction/sparsity rung and is reported with its ε-shape.
- Observed: the lap-mean vectors themselves.
Simulation: joint Gaussian draws over bins in segments of 120 bins (12 m; DANDI tracks are one segment), 100 replicates
per image per directional track; statistic D_ε = greedy ε-packing count of the bin vectors, averaged over replicates.

## Rules
- B0 sanity: a directional track enters if it has ≥ 30 units, ≥ 10 laps, ≥ 20 bins with data, and the split-half
  distance distribution has CV < 0.5 (a well-defined floor). Everything else is excluded before any count is taken.
- B1 sign law: D(G0) > D(obs) at every ε ≥ ε_halves in ≥ 90% of track × ε cells, and the aggregate gap
  log(ΣD(obs)/ΣD(G0)) is monotone decreasing in ε over {1, 1.5, 2} × ε_halves.
- B2 heterogeneity closes the gap: |log(ΣD(obs)/ΣD(G1))| ≤ 0.05 at every ε ≥ ε_halves (aggregate over tracks), and
  ≤ 0.10 for ≥ 80% of tracks at ε = ε_halves and 2·ε_halves.
- B3 Kolmogorov consistency (reported): water-filling ε-entropy of G1's covariance vs its Monte Carlo packing count.
- B4 cross-animal transfer (secondary, hc-31 only): G1′ builds s_i from the authors' field density per bin with the
  density→variance exponent fixed on rats {5, 6, 7} and applied to {8, 9}; |log(ΣD(obs)/ΣD(G1′))| ≤ 0.10 aggregate.
- Verdict: BRIDGE CONFIRMED if B1 and B2 hold on hc-31 (DANDI reported as replication with its power limit stated);
  SIGN ONLY if B1 holds and B2 fails; REFUTED if B1 fails. Ceiling map, stated now: CONFIRMED → reframed ceiling
  ≈ 1 in 3; SIGN ONLY → ≈ 1 in 6; REFUTED → ≈ 1 in 15 and the frame is a theory of heredity.

## What is deliberately out
The room-face fraction φ against the hyperbolic ball is not scored: the Betti-curve radius carries ±3 in R, a factor of
hundreds in room. The reader-optimal coincidence (η 0.38 vs Fisher 0.41) is Zhang et al.'s prediction and is not a rule
here. No per-unit rank rule on a stochastic prediction (lesson of PREREG12 D4).

## Data, provenance, conditions
hc-31 (CRCNS; Rich, Liaw & Lee 2014): fetched by the user with code/fetch.sh from the 9/25 folder into
biosphereatlas:/fast/scratch_hc31_eta; sessions = rat × period (RUN2 per rat primary; RUN1 sub-epochs where B0 holds).
Publications using hc-31 must list P. Dylan Rich and Albert K. Lee as authors. DANDI 000044 (Grosmark & Buzsáki;
CC-BY-4.0): streamed with code/extract.py, no login. All staging on biosphereatlas in one scratch directory under
nice; deleted after import; nothing outside it touched.

## Caveats stated in advance
Position × direction as the state definition is a modelling choice; one sensitivity (20-cm bins) is reported.
Stationarity of C(Δx) along a 48-m track is an approximation (the first 3-m section is seen more often). Segmenting at
120 bins removes correlations across 4 cut points per directional track, a small bias toward fewer simulated collisions
(against B1, not for it). Lap definition: a full traversal in one direction between the track ends. This registration
was written with knowledge of the 9/25 results (no expansion with familiarity on tracks once speed is controlled;
field size ∝ speed^0.5), none of which enters the statistics here.

## Amendment before any real data — 2026-10-04 16:16: the Gaussian images are Fourier surrogates
Synthetic calibration (24-m track, 60 units, 20 forward laps, Poisson spikes): the two estimator-based Gaussian
images first written (truncated empirical kernel with eigenvalue clipping; Daniell-smoothed periodogram with noise
subtraction and PSD clipping) were BIASED on a Gaussian-like dense code (log obs/G0 = −0.72 and −0.80 at ε_halves):
both leak power to high frequencies, making simulated paths rougher than a smooth code and under-producing
adjacent-bin collisions. They are withdrawn. G0 is now the multivariate Fourier phase-randomised surrogate of the
bin series (common random phases per frequency, Hermitian symmetry): all auto- and cross-spectra, hence all circular
lagged covariances including the lap-mean noise, are preserved exactly, with no smoothing or clipping. Calibration on
the Gaussian-like synthetic: log(obs/G0) = 0.00/−0.04/−0.05/0.00/+0.07 across the ε grid (unbiased within Monte Carlo
and finite-sample noise). On the sparse Poisson place code: 0.00/−0.17/−0.08/−0.03/−0.04, the resolution-dependent
over-count expected for a non-Gaussian code. G1 = G0 surrogate × √s_i per bin, with s_i the smoothed (3-bin) TOTAL
per-bin variance profile normalised to mean 1 (signal and noise together, so the per-bin variance of the observed
code is matched exactly). On the sparse synthetic G1 over-corrected at ε_halves (−0.17 vs G0's −0.08): a variance
profile does not describe a sparsity departure. Rule reading fixed now: a B2 miss with the sign flipped past +0.05 is
read as "marginal shape (sparsity), not variance heterogeneity" and reported as such; B2 passes only within ±0.05.
B1 is expected on theoretical grounds for any non-Gaussian code (the Gaussian maximises entropy, hence ε-entropy at
small ε, for given second moments); it is retained as a calibration-and-sign check, and the test's content is B2.
B3 (reported) uses the exact eigenvalues of the circulant block covariance (the periodogram's per-frequency
cross-spectral matrices), so no estimator enters it. 100 surrogates per image per directional track.

## Pre-data clarification — 2026-10-04 16:20: occupancy floor
The first DANDI pass excluded every directional track under B0 ("bins 0") because the code required ≥ 0.10 s of
running occupancy per bin per lap, which a 5-cm bin at 40–60 cm/s does not reach; no statistic was produced. The floor
is set to 0.04 s (two position samples at 40–50 Hz); rates are noisier in fast bins and that noise enters ε_halves,
as the design intends. B0's bin criterion (≥ 10 complete laps) is unchanged.

## Pre-data clarification — 2026-10-04 16:23: DANDI time axis and paused samples
Inspection of one session's position series (no statistic computed) showed the 9/25 extractor built lin_t with the
sampling rate as the interval (median Δt 39.06 instead of 0.0256 s), so all speeds were ~0, and that 93% of linearised
positions are NaN (animal paused at the ends or off-track). Fixes: the time axis is rebuilt as a uniform grid over the
stored maze-epoch bounds; NaN-position samples are dropped; Δt is capped at 3× its median so gaps never count as
occupancy and never produce spurious speed. The hc-31 driver will apply the same handling. The second "bins 0" pass
was this, not the occupancy floor (which stays at 0.04 s).

## Pre-data clarifications from the hc-31 layout — 2026-10-04 16:28 (structure read; no spike statistic computed)
- resSave.mat checksum matches CRCNS (f97e5810…). Animals are elements 5–9 with 63/58/27/59/53 cells; cells with
  any ID > 2 (interneurons/poor) are excluded as the authors prescribe; the ≥ 50-spikes-in-epoch rule is applied on top.
- Spike times (spEpochSep, columns sleep1/run1/run2/run3) and positions (posMazeLin: time, linear position, offset,
  velocity, direction) are in Neuralynx microseconds and are converted with the stored unitsPerSecond.
- The linearised track reaches 18.9 m in the last RUN1 sub-epoch (sectExt), not 48 m as I had assumed from memory;
  10-cm bins give ~190 bins per direction. Sessions per animal: RUN1 sub-epoch 4 (window sectInt[3], full track
  available), RUN2, and RUN3 (a third familiar run present in the file; included as the same kind of session). All
  other rules unchanged.

## DANDI 000044 (replication arm) result as registered — 2026-10-04 16:31: REFUTED
13 directional tracks scored (29–53 bins at 5 cm; 3 circular-maze directions excluded with 0–2 laps). Aggregate
log(Σobs/ΣG0) over the ε grid {0.5, 0.75, 1, 1.5, 2} × ε_halves = −0.013/−0.095/−0.152/−0.145/−0.013; with G1:
−0.003/−0.052/−0.119/−0.129/−0.049. B1 FAIL: G0 > obs in 77% of track × ε cells (rule 90%) and the aggregate gap is not
monotone (it vanishes at 2 × ε_halves). B2 FAIL: G1 leaves −0.12/−0.13 at 1 × and 1.5 ×; per-track within 0.10 for 50%.
Readings, verdict first: (i) at the noise floor the Gaussian over-counts in 12 of 13 tracks and by 0.15 in aggregate,
which is the sign law; (ii) the B1 rule over-reached: the maximum-entropy argument makes the Gaussian over-count a
small-ε statement, and at 2 × ε_halves these short tracks collapse to 2–12 states, where a single realisation's count
noise is ±2 and five tracks show obs > G0; (iii) the variance-profile image G1 is not the mechanism here; on the sparse
synthetic it also failed, and the remainder's shape (largest at 1–1.5 ×, gone at 2 ×) is the sparsity/marginal-shape
signature, not variance heterogeneity. Power limit as stated in the registration. Verdict stands.

## Amendment before any hc-31 statistic — 2026-10-04 16:31: replicate unit for hc-31
hc-31 animals make 3–4 end-to-end traversals of the 48-m track (RUN2: 1,284 s for animal 5) but 55–90 running
segments per direction; 10-cm bins see a median of 4 passes in RUN2 (364–421 of 481 bins with ≥ 4; none with ≥ 10)
and 3 in RUN1 sub-epoch 4 (62–73 bins with ≥ 4). The authors defined fields over 3–5 passes. For hc-31 the replicate
is therefore a PASS: a contiguous running segment (speed > 5 cm/s, consistent direction, ≥ 1 m net displacement); a
bin enters with ≥ 4 passes; odd/even halves are alternate passes. RUN1 sub-epoch 4 will largely fail this and is
reported; animal 7 (24 valid cells) fails the ≥ 30-unit rule as registered. All verdict rules for hc-31 are UNCHANGED.
Because DANDI's coarse-ε behaviour was seen first, a secondary small-ε reading (ε_halves and 1.5 × only) is reported
for hc-31 and labelled DANDI-informed; it does not enter the verdict. The 48-m track corrects my earlier "19 m" note
(that was RUN1's extension stages).

## hc-31 (primary arm) result as registered — 2026-10-04 16:39: REFUTED
6 directional tracks scored (animals 5 and 9: RUN1 sub-epoch 4 and RUN2; 59–438 bins at 10 cm; 48–111 passes), 24
excluded under B0: animals 6 and 7 by the ≥ 30-unit rule (25 and 15–17 units with ≥ 50 spikes), RUN3 (a different
1–2 m track with 0–2 passes), and 8 tracks by the split-half CV ≥ 0.5 gate, which pass-based halves of ~2 vs 2 passes
make hard to meet. The first pass-based output had a halves bug (a bin's passes could all fall on one global parity,
giving ε = NaN) and is kept as SUPERSEDED; the corrected run is scored.
Aggregate log(Σobs/ΣG0) over {0.5, 0.75, 1, 1.5, 2} × ε_halves = −0.394/−0.697/−0.617/−0.159/+0.869; with G1:
−0.222/−0.412/−0.541/−0.424/−0.092. B1 FAIL (G0 > obs in 56% of cells; non-monotone). B2 FAIL (G1 leaves −0.54 at
ε_halves; per-track within 0.10 for 17%). Verdict: REFUTED. Combined with DANDI (REFUTED), PREREG14 is REFUTED and the
pre-committed ceiling map applies: reframed ceiling ≈ 1 in 15; the frame is classified a theory of heredity.
Readings, verdict first: (i) at the noise floor the Gaussian image over-counts resolvable position states in every
hc-31 track (−0.20 to −0.76; aggregate −0.62, i.e. the real code resolves 54% as many states as a Gaussian with its
second moments) and in 12 of 13 DANDI tracks (−0.15): the small-ε sign law held in 18 of 19 tracks across two
datasets. (ii) At 2 × ε_halves the sign reverses hard (+0.87): the real code is a long one-dimensional curve whose
far-apart positions stay far apart, while a stationary Gaussian with the same spectrum is a cloud whose coarse-ε
packing collapses; B1's all-ε clause was mis-specified by me, since the maximum-entropy argument is a small-ε
statement. (iii) The variance-profile image G1 is not the mechanism in a neural code (SD of log s_i = 0.74 yet only
−0.62 → −0.54): phase randomisation destroys the smooth deterministic curve, whose near-uniform adjacent-bin increments
collide more than a Gaussian field's chi-square-distributed ones; the fine-ε over-count is a uniformity-of-increments
effect, the opposite kind of departure from the Atlas's mixture heterogeneity, with the same sign. (iv) In both media
the Gaussian/diffusive image fails at depth or coarse scale because the real process has directional persistence
(convergence in the Atlas; a trajectory in CA1). That echo is post hoc and is recorded as a reading, not a result.
