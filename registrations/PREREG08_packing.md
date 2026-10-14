# Packing-law validation — pre-registration (2026-09-28, before any of this code ran)

Claim: the number of distinguishable lineages at depth τ is the ε-packing number of the process's retained image on
the actual tree, where the reader enters only as a metric and a resolution ε (PREREG7 results; Kolmogorov
ε-entropy throughline). Three tests, three media, one statistic.

## K1 — recorder ε-scaling and algorithm-independence (intMEMOIR; same split; same validated writer)

- Resolutions ε ∈ {0, 1, 2} (signatures within Hamming ≤ ε are one lineage; single-linkage clusters). Same writer,
  same 400 simulations per test tree as T1; D_g(ε) predicted and observed.
- K1a PASS if |log D_obs − log D_pred| ≤ 0.15 at every ε and every generation with ≥ 50 test lineages.
  Registered expectation from PREREG5: ε = 0 may fail at g ≥ 4 (writer under-produced exact coincidences).
- K1b algorithm-independence: Fitch parsimony on the true topology with observed leaf states; a division is
  "recovered" if its two daughter clades are assigned different states at some site by the Fitch reconstruction
  (any assignment); the number of distinct reconstructed ancestor states at generation g must not exceed the
  ε = 0 packing number of the observed leaf-derived signatures. PASS if never exceeded in any test colony.

## K2 — Atlas packing (base map v1.0; E-D family split; test genera only)

- ε: the recipe distance between two DNA-disjoint halves (alternating 100 kb blocks) of one genome, median over a
  fresh sample of 300 bacterial genomes with local FASTA (≤ 200 contigs, ≥ 1 Mb), computed on biosphereatlas from
  FASTA with the frozen recipe. Also recorded: the 90th percentile, used as a sensitivity value.
- Process per family: full Γ_f(τ) bins (≥ 150 train pairs) and Σ_f from train genera, as E-D. Shallow
  mitigation: for τ below the family's first bin, use the pooled within-genus variogram shape scaled so its trace
  matches the family's first bin.
- Statistic: for each test genus with ≥ 4 genomes, simulate the family's Gaussian process on the genus subtree
  (patristic branch lengths; leaves start from the genus MRCA at 0, increments N(0, Γ-consistent)), 200 reps;
  greedy ε-packing number of the leaves in the recipe metric (fixed leaf order); observed = same greedy count on
  the real coordinates. Sum over genera within crown-depth bins (crown = max root-to-tip patristic depth of the
  genus subtree), bins geomspace(0.01, 0.6, 7).
- Simulation covariance: Cov(z_i, z_j) = Σ_f − Γ_f(τ_ij) (the E-D model); leaves drawn jointly from that
  Gaussian, so no branch-increment construction is needed.
- K2 PASS if log-error ≤ 0.15 in every crown bin with ≥ 40 test genera; PARTIAL if it passes for all bins with
  crown ≥ the family-median first-bin τ (shallow extrapolation excluded); FAIL otherwise. Pooled-process baseline
  reported.

## K3 — sequence packing (synthetic harness, record-only real roots, L = 1 Mb)

- Readers: raw standardised 4-mers and the recipe. ε per reader: the halves distance in that reader's metric,
  computed on the same 8 roots (alternating 100 kb blocks of the unevolved root).
- Statistic: for quartets at each depth t in TGRID, the greedy ε-packing number of the four leaves (1–4);
  predicted from the closed-form Gaussian channel model (leaf covariances from harness_theory), observed from
  harness_results (leaf coordinates re-simulated with the same seeds, 20 quartets per depth).
- K3 PASS if the mean packing number per depth is within 0.25 of prediction at every depth for both readers.

Verdict: the packing law is SUPPORTED if K1a passes at ε = 1 and 2, K2 passes or is PARTIAL, and K3 passes; the
ε = 0 outcome of K1a is reported as the writer's exact-coincidence calibration.

## Amendment — 2026-09-28 12:39, after K1 ran, before K2 or K3 ran

- K3 is withdrawn as ill-posed: in the record layer two DNA-disjoint halves share no record, so the halves
  distance is the maximum (infinite-depth) distance, not a noise floor; and with exact sequences a re-read has
  ε = 0, making the packing count trivially 4. The sequence medium's cross-medium evidence is the quartet form
  already validated on the same instrument (harness H1, H2). No K3 statistic will be computed.
- K2 ε: the halves distance measures two half-genome samples of one lineage; whole-genome coordinates have half
  that sampling variance, so ε = median halves distance / √2 (sensitivity: 90th percentile / √2).
- K2 genus size capped at 30 genomes (random subsample, seed 8003) for the joint Gaussian draw.
- K1b as registered compared Fitch-reconstructed ancestor states with the strict clade-signature packing number;
  a misread-tolerant reconstruction is a finer reader (smaller effective ε), so the comparator was mis-specified.
  It is reported as registered (FAIL) and not used in the verdict.

## Results (2026-09-28)
K1a: ε=1 PASS (−0.00/+0.03/+0.11/+0.05/−0.00); ε=0 FAIL at g4–5 (−0.15, −0.32; writer under-produces exact
coincidences, as registered); ε=2 FAIL at g5 only (+0.41, n=108). K1b FAIL as registered (mis-specified, excluded).
K2: ε = 1.115/√2 = 0.788 (p90 sensitivity 1.254); 593 test genera. Log-error (family / pooled) by crown bin:
0.010–0.020 (9 genera, ungated) −0.36/−0.42; 0.020–0.039 (17, ungated) −0.21/−0.25; 0.039–0.077 (82) −0.085/−0.100;
0.077–0.153 (178) −0.048/−0.055; 0.153–0.303 (248) −0.025/−0.026; 0.303–0.600 (58) −0.016/−0.018 → K2 PASS as
registered. Caveats: at this ε the statistic is near-saturated in gated bins (packed ≈ 95–98% of leaves), so
family and pooled processes are indistinguishable there and a trivial "all distinct" prediction would also pass;
the discriminating region (crown < 0.04) is ungated and shows both processes over-predicting distinguishability
(−0.2 to −0.36). Mean clipped negative-eigenvalue mass in joint covariances 0.082. ε p90 sensitivity: errors grow
(−0.16 to −0.05) with the same sign and depth trend.
Registered overall verdict: NOT SUPPORTED as written (K1a failed at ε=2 in one bin; K3 withdrawn). Reading: the
packing law holds at the registered resolution in both media through the well-sampled range; at the finest
effective resolution both media show real lineages MORE similar than the process predicts (recorders ε=0 late;
Atlas shallow crown) — a "quiet" component of real processes (nothing written / near-clonal strains).
