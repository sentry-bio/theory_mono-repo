# Parsimony tests — pre-registration (2026-09-28, before any of this code ran)

Claim under test: retained distinct histories are set by ONE process quantity, the distinguishing entropy written
along a lineage since its branching point, evaluated at the reader's resolution and propagated on the tree; and
the room a medium offers is that quantity's ceiling. Two media, same term.

## T1 — recorders (intMEMOIR; 60 train / 47 test as before)

- Reader's resolution: signatures within Hamming distance 1 are identical (single-linkage clusters), as PREREG6.
- Primary predictor P1 (tree-aware): the empirical writer of PREREG5 (validated on train; donor pools by start
  bin and duration; founder edits from root-edge donors; misread ε from the PREREG4 fit) simulated 400 times on
  each test tree; D_g = mean number of clusters among the colony's generation-g lineage signatures; summed over
  test colonies. No parameter is fitted to test data; nothing is fitted at all beyond the donor pools.
- Secondary predictor P2 (closed form, iid approximation): post-root signatures = lineage signature with sites
  masked where the colony's root clade is edited (edits shared by all lineages). Pool train post-root signatures
  per generation; cluster at resolution; empirical p_k. Predicted distinct among a test colony's N_g lineages =
  Σ_k [1 − (1 − p_k)^N_g]. Ignores shared ancestry inside the colony, so it should over-predict D_g at depth.
- Baseline: PREREG6's pooled H_path prediction (log-errors −0.21/−0.31/+0.14/−0.02/−0.77).
- Rules (generations with >= 50 test lineages): P1 PASS if every |log D_obs − log D_pred| <= 0.15. P2 reported
  with the same rule. Supported if P1 passes; partial if P1 fails only at g = 5; refuted otherwise.
- Decomposition (test, reported): among colliding same-generation lineage pairs, the share with both post-MRCA
  paths carrying no placed edit ("nothing written") vs the rest ("same thing written"). Registered expectation:
  nothing-written dominates at g <= 2 and same-written at g >= 3. Also the fraction of lineages whose post-root
  signature is empty, by generation.

## T3 — Atlas (base map v1.0, GTDB r220; E-D family split by md5("E-D:" + genus); families >= 300 genomes)

- Room term per family: participation ratio PR_f = (tr Γ_f)² / tr(Γ_f²) of the within-family variogram matrix at
  the bin nearest τ*_f, the median sister distance of the family's TRAIN-genera F4 quartets.
- Kernel per family: c_f(τ) = 1 − tr Γ_f(τ) / tr Σ_f, interpolated in log τ over the family's bins (>= 150 pairs),
  clipped to [0, 1]. Both from train genera only.
- Prediction: the Gaussian channel model with PR_f isotropic channels of kernel c_f (Cov = c_f(τ)·I), evaluated
  by the validated bivariate-normal formula on each quartet's six patristic distances.
- Comparator: PR = 56 with the round-1 pooled kernel (trace form of the pooled variogram).
- Test quartets: NEW F4 quartets (four genera, one genome each) from test genera, seed 7003, up to 300 per family.
  Caveat stated: family-level observed accuracies from E-D's earlier quartets have been seen; new quartets reduce
  but do not remove that exposure. Rules were fixed before drawing them.
- Rules (families with >= 50 test quartets): T3-P1 Spearman(pred, obs) >= 0.6 and mean |error| <= 0.07;
  T3-P2 family-room mean |error| <= 0.75 × pooled-room mean |error|. Supported if both pass.
- Reported: calibration by t bin pooled over families (as D-a), and PR_f vs observed accuracy.

## Results (2026-09-28)
T1 SUPPORTED: tree-aware writer at resolution, log-error by generation −0.002/+0.031/+0.110/+0.051/+0.000
(PREREG6 baseline −0.21/−0.31/+0.14/−0.02/−0.77). Closed-form iid P2 FAILS (+0.25/+0.21/+0.34/+0.10/−0.40):
shared ancestry inside a colony matters. Decomposition: colliding pairs with nothing written since the MRCA
0.38/0.39/0.37/0.34/0.59 — my registered expectation (nothing-written dominates early, same-written late) was
wrong; both causes act at every depth, and "same written" dominates until the last generation.
T3 NOT SUPPORTED: 36 families; family-room (PR_f + trace kernel) mean |error| 0.081 vs pooled 0.174 (T3-P2 PASS)
but Spearman 0.48 (< 0.6) and error > 0.07 (T3-P1 FAIL). Pooled ranks better (0.65) despite gross
miscalibration; PR_f anti-correlates with observed accuracy (−0.35). The two-scalar reduction (room × kernel)
loses what the full anisotropic family model (E-D: error 0.069) and the recorder's joint writer keep: WHICH
directions are written slowly. Reading: the one process term is a distribution, not a product of scalars.
