# Synthetic-lineage harness — pre-registration

Written 2026-09-26 before any harness simulation ran. Closed-form predictions are in harness_predictions.json
(computed by harness_theory.py, which reproduces the C3 closed form exactly: 0.199 for the uniform-π standardised
4-mer reader). Nothing below is fitted.

## Purpose

Test the theory's claims about readers and media on the frozen Atlas instrument, with the process known. Nature is
replaced by a known process on real sequences; the frozen base map v1.0 recipe is read exactly as distributed.

## Design

- Roots: 8 complete bacterial chromosomes (<= 3 contigs, >= 4.3 Mb), one per genus, GC 0.29–0.71
  (harness_roots.json); the largest contig, truncated to the stated length.
- Process: F81 with the root's own base composition π (so the root is at single-letter stationarity), every site
  independent. Quartet ((0,1),(2,3)), internal branch δ = 0.1, pendant t, rooted at the midpoint of the internal
  branch so that any drift of the root's higher-order composition is identical for all four leaves and cancels.
- Every quartet is an independent simulation (no shared history), so replicate error is ordinary.
- Readers: R1 frozen recipe (canonical 4-mers, pseudocount 0.5, centred log-ratio, W_zca); R2 standardised
  non-canonical 4-mers; R2b canonical standardised; R2c canonical log-ratio (decomposition only); R3 aligned
  Hamming; R4 centred gapped pairs at gaps 1..G.
- Horizon: depth t where mean/sd of the four-point margin X = d02 + d13 − d01 − d23 falls to 1 (C3 definition),
  log-interpolated on t = geomspace(0.01, 4, 18) with 60 quartets per depth (40 at 4 Mb and for R4).
- Arms: A1 iid roots drawn from each root's π (the theory's exact domain), L = 1 Mb. A2 the real roots, L = 1 Mb.
  Length ladder on real roots: 0.25, 1, 4 Mb. R4 on 4 real roots at 1 Mb (GC 0.29, 0.48, 0.60, 0.71).

## Predictions (closed form, per root) and rules

| Root | GC | R2 std4 | R2b canon | R2c log-ratio | R1 recipe | R3 Hamming 0.25/1/4 Mb | R4 G = 64/1024/16384 |
|---|---|---|---|---|---|---|---|
| GCF_006408335.1 | 0.29 | 0.193 | 0.161 | 0.122 | 0.126 | 1.66/1.90/2.15 | 0.336/0.566/0.807 |
| GCF_027563495.1 | 0.36 | 0.196 | 0.163 | 0.140 | 0.138 | 1.71/1.96/2.21 | 0.342/0.578/0.826 |
| GCA_020344415.1 | 0.42 | 0.198 | 0.165 | 0.155 | 0.147 | 1.74/2.00/2.26 | 0.346/0.586/0.839 |
| GCA_020353355.1 | 0.48 | 0.199 | 0.166 | 0.162 | 0.151 | 1.76/2.02/2.27 | 0.347/0.590/0.845 |
| GCF_020150455.1 | 0.54 | 0.199 | 0.166 | 0.161 | 0.149 | 1.75/2.01/2.27 | 0.347/0.589/0.844 |
| GCA_002998355.1 | 0.60 | 0.198 | 0.165 | 0.155 | 0.143 | 1.74/2.00/2.26 | 0.346/0.586/0.839 |
| GCA_026002855.1 | 0.66 | 0.195 | 0.163 | 0.136 | 0.127 | 1.70/1.95/2.20 | 0.340/0.575/0.822 |
| GCF_008087625.1 | 0.71 | 0.192 | 0.160 | 0.118 | 0.111 | 1.64/1.89/2.13 | 0.334/0.563/0.802 |

- H1 closed form, exact domain (A1): R1 and R2 each within ±0.02 of prediction in >= 7 of 8 roots, median |error|
  <= 0.01.
- H2 transfer to real sequences (A2): R1 and R2 within ±0.03 of prediction in >= 6 of 8 roots. (Under midpoint
  rooting the root's own structure enters only through a mean shared by all leaves, which cancels.)
- H3 medium property, length independence (real roots): R1 and R2 horizons at 0.25 and 4 Mb differ by <= 0.03 in
  >= 7 of 8 roots, while R3 Hamming rises by the predicted 0.49–0.52 within ±25% in >= 7 of 8 roots and each R3
  horizon lies within ±0.06 of its prediction.
- H4 reader property (A2): R1 < R2 in every root, and the deficit R2 − R1 rises with |GC − 0.5| (Spearman >= 0.7
  across roots). Predicted deficit 0.048 (balanced) to 0.081 (GC 0.71); the table's middle columns attribute it to
  strand merging (~0.033) and the log-ratio at skewed GC, with whitening a smaller step.
- H5 positional escape (real roots, 1 Mb): R4 rises by 0.24 ± 25% for each 16-fold step in G (both steps, all 4
  roots) and exceeds R1 and R2 at every G.

## H6 layer attribution: which half is nearest (real roots, 2 Mb, recipe)

- Halves: alternating 100 kb blocks (as in the base map's own test), counted per block.
- Record-only arm: F81 with the root's π on every branch.
- Trait-drift arm: each branch has its own GC, logit(g_child) = logit(g_parent) + 0.5·sqrt(ℓ)·N(0,1), and its
  substitutions draw from π(g) = ((1−g)/2, g/2, g/2, (1−g)/2); everything else identical.
- Depths t = 0.05, 0.1, 0.2, 0.4, 0.8; 40 quartets each; 4 roots (as for R4).
- For each of the 8 halves in a quartet: is its nearest other half its own genome's other half, the sister's
  homologous half, or another?
- PASS if record-only P(own) <= 0.2 at every depth and P(sister's homologous) >= 0.5 at t <= 0.1; and trait-drift
  P(own) exceeds record-only P(own) by >= 0.3 at t >= 0.4. (Record cannot make DNA-disjoint halves find each other;
  a genome-wide trait can.)

## H7 encoder (phase 1b, run after phase 1a on biosphereatlas)

- Same record-only real-root quartets; each leaf read at the same 20 kb coordinates (homologous windows), by the
  v10.9 encoder (cosine) and by the recipe on the 20 kb window.
- Predictions: the recipe's 20 kb horizon lies within ±0.03 of its whole-genome closed-form horizon (length
  independence down to 20 kb). The encoder's horizon is <= 0.5 × the recipe's 20 kb horizon, because training that
  places different windows of one genome together discards window-specific (record) composition. If the encoder
  matches the recipe, that account is wrong.
