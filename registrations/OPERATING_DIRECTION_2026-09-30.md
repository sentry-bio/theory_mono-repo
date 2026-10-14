# Operating direction (adopted 2026-09-30)

## The law, in one sentence
A reader at resolution ε recovers at most the ε-entropy rate of the process's retained image on the tree; that rate
lies between the lineage's branching entropy and the host's packing entropy; every count made upstream of collision
over-states it. (Theorem 1 in min form is machine-checked; the rigidity of the equality case is proved in prose.)

## The reframe
1. **Two fixed points, not one.** The inequality has an equality face (room-limited; saturation forces the host to be
   tree-like at scale ε) and a reader-optimal interior (the expansion rate or reader chosen to maximise resolution).
2. **Nature sits off the room face.** Room is exponentially cheap in every natural medium measured (4^L states; e^{(d−1)R}
   in a hyperbolic representation), so the room term never binds: sequence η ≈ 10⁻⁸; composition slack by construction;
   CRISPR erasure-limited; hippocampus room grows ~T^2.6 against experience ~T (η ≈ 0.38, at the Fisher-optimal point
   0.41). Zero of four natural media at capacity. What binds in nature is writing and erasure.
3. **Saturation is a design regime.** The one medium that touched the room term is a 10-site engineered recorder, and it
   is where the tree-aware packing prediction was exact (T1). The rigidity theorem is therefore an engineering statement:
   build a recorder that saturates and its readout geometry is forced tree-like at the readout's ε.
4. **η is a trait.** Filling efficiency at the reader's resolution is a measurable property of any memory medium, stable
   across days in the hippocampus, and it lands on an independently derived optimum there.
5. **The one-sign law.** Every refuted predictor assumed less dependence in the realised image than there is
   (independent sites, pooled clades, isotropic spread, un-clumped writing, family-average rates). More dependence means
   more collisions, so the error is always an over-count of distinguishable states, growing with ε. The ladder
   h_written ≥ h_joint ≥ h_ε is this law stated for entropies. Candidate mechanism: counting under a saturating reader
   is concave in the process rate, so averaging heterogeneity before counting over-predicts (Jensen); the drop is then
   set by the heterogeneity variance the model left out.

## What it forbids (so it is not a vocabulary)
- A natural medium with exponential room found at the room face falsifies point 2.
- A second hyperbolic neural dataset with an experience axis giving η near 1 falsifies point 2; near the Fisher point
  supports it.
- If the drop does not derive from train-measured heterogeneity (PREREG11), the one-sign law is a description and the
  middle tier collapses toward the floor.

## Program order
1. **PREREG11: the drop as the swing test** (local, on-disk data): derive the AC1 residual per family from train-genera
   heterogeneity and spectral shape; no residual used in the derivation.
2. If derived: reformulate the hippocampal bridge with the derived form (heterogeneity of the neural process against the
   noise floor) and register a parameter-free η prediction against the already-measured 0.38.
3. Recorder out of sample (Synapse in-silico sets or a second imaged dataset): turns the readout mixture from patch to
   result; the same drop mechanism (clumped writing) is registered for the ε = 2 cells.
4. One registered hippocampal run on the untested regimes (first passes; days), with a = dR/dlnT = 0.50 as the number;
   the reframe predicts a negative.
5. The artefact: one inequality, two theorems, one figure (packing curves with both baselines breaking), one ledger.

## Ceiling ledger (my wagers, 2026-09-30)
- As first defined (natural instance at capacity): ~1 in 33.
- Reframed (two fixed points; nature reader-optimal; saturation built; η a trait): ~1 in 8–10.
- If the drop derives and matches the Atlas residuals: ~1 in 5. If the same form then predicts hippocampal η within its
  CI with nothing fitted: 1 in 2–3.
- Kill conditions: the drop is medium-specific; or the bridge predicts an η nowhere near 0.4.

## Housekeeping
Folders: ~/Documents/addressability-{heredity,atlas,harness,recorders,crispr,hippocampus,math,direction}-2026-09-*.
Local scratch copies (base map package etc.) to be deleted when the Atlas arm is finally closed. biosphereatlas is at
baseline. hc-31 authorship condition stands for any publication using it.

## Atlas derivation closed — 2026-09-30 16:04 (PREREG11 → 12 → 12a → 13; final-attempt clause applied)
What the day established, at the level the passed rules justify:
- The one-sign over-prediction of the Atlas is heterogeneity the family-average image left out, and the part of it
  that grows with resolution is heritable heterogeneity below the genus: a train-fitted heritable clock removed the
  ε-dependence entirely (residual flat at −0.04 from −0.04 → −0.12) and predicted which families over-predict and by
  how much (Spearman +0.62, slope 0.77 over 29 held-out families). That is PREREG12 v1, on record as PARTIAL because
  its marginal was mis-specified (root mean 1.38) and its per-genus rule was ill-posed.
- No scalar-rate model fits the training statistics jointly: the mean-1 Brownian clock cannot reach the right tail
  (12a), and the stationary OU clock cannot give deep pairs their spread without over-sharing at the genus level (13).
  Deep pairs are heterogeneous without being genus-shared; that is direction, not rate: lineages differ in where they
  move in composition space, and convergence brings unrelated lineages closer than divergence implies.
- The drop at the Atlas is therefore a MEASURED quantity (a calibration term per family), the genus-rate rung is small,
  the subclade rung is real and transferable, and the deep rung is directional and outside the rate family. A
  retraction is on record: the "kernel bias" reading of v1's remainder was wrong (median < mean is σ²/2).

Consequences for the program:
- The Atlas arm is closed for derivation. Its product use stands: depth-of-validity per family = kernel + measured
  heterogeneity calibration.
- Direction is the next term, to be studied where it can be controlled: the synthetic harness with a directional
  trait process (clade-specific drift directions with convergence), then measured on the Atlas as a convergence
  statistic, not fitted to the residual.
- The recorder arm (clumped writing) and the hippocampal bridge proceed on their own registrations.

Ledger (revised): middle tier ≈ 0.45 (mechanism supported and half-derived: shape and family transfer yes, marginal
no); reframed ceiling ≈ 1 in 8; as-first-defined ceiling unchanged (~1 in 33). Kill conditions unchanged.

## Hippocampal bridge closed — 2026-10-04 16:39 (PREREG14: DANDI REFUTED, hc-31 REFUTED; pre-committed map applied)
- The pre-committed consequence stands: reframed ceiling ≈ 1 in 15; the frame is classified a theory of heredity.
- What survived, at the level the data justify: the small-ε sign law (a second-moment Gaussian over-counts resolvable
  states at the noise floor) held in 18 of 19 directional tracks across two datasets, by 0.62 in log on the 48-m track.
  That is the data-processing content of the ladder in a neural medium, and only that.
- What did not transfer: the heterogeneity mechanism (variance profile), the Atlas's term, is not what makes the gap in
  a neural code; and the Gaussian is the wrong room at coarse ε because the code is a curve, not a cloud (sign reversal
  +0.87 at 2 × ε_halves). B1 was mis-specified by me across all ε; the verdict is taken as registered regardless.
- One echo recorded as a reading: in both media the diffusive image fails at depth/coarse scale for want of directional
  persistence (convergence in the Atlas, trajectory in CA1). If direction is ever registered as a term, it is the same
  term in both.
- Program: no further bridge attempts without a direction-aware null designed in the harness first. The artefact is now
  the honest deliverable: one inequality, two theorems, one figure, a ledger in which four registered stops are the
  argument for what the frame is and is not.
