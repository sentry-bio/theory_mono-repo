# PREREG21 — composition's own horizon on the Atlas kernels, with an ancestor-aware reader (formerly 15c)
# Registered 2026-10-09, ≈02:12 CEST (before the disclosed smoke test of 02:14:58 in run.log; the clock time first
# written here, 03:30, was mis-stated and is corrected to the log), before any split-level statistic was computed.

## The claim
The theory page: "Composition cannot carry deep genealogy alone. Its room is bounded and its readers pay a tax; its own
horizon is set by the trait's mean reversion against branching." For a mean-reverting (Ornstein–Uhlenbeck) trait
broadcast on a tree, the correlation between a lineage and its ancestor decays as e^{−θτ}, and the Gaussian
broadcast's reconstruction threshold is the Kesten–Stigum line b·e^{−2θτ_edge} > 1 (Mossel–Peres 2003: tight for
Gaussian channels), i.e. β > 2θ in rate form, the same line as the sequence window with the substitution rate
replaced by the trait's mean-reversion rate. Two readers see this line differently:
- a pairwise reader (the four-point method on composition distances) pays a cost exponential in depth whatever
  the side of the line, because its signal is a single pair's covariance e^{−θτ};
- an ancestor-aware reader (one that estimates each clade's ancestral composition from all its leaves — the clade
  centroid, which is the OU ancestor estimate at leading order — and reads genealogy by proximity to ancestors)
  keeps a signal above the line, where the many-leaf average beats the trait's forgetting.
This registration measures both readers at every qualifying family's deepest split on the Atlas, predicts both from
the family's frozen kernel with nothing fitted to the outcome, and reports the line.

## Data and objects (A-curve's, unchanged)
Base map v1.0 coordinates (recipe metric; for bacteria the atlas_predictions projection as in acurve.py), bac120 and
ar53 r220 trees, E-D train/test split by genus; the 36 bacterial families and the archaeal families that A-curve
qualified, with their fitted family kernels S_fam (variogram bins, EDGES, 150 pairs per bin; the shallow fallback as
in acurve.py). Nothing is refitted.

Per family f:
- The family subtree: the MRCA of its catalogued genomes on the reference tree. The deepest split: the MRCA's two
  child clades; if either carries fewer than 10 genomes (6 for archaea), descend into the larger child and take its
  split, repeating until both sides qualify. Sides A and B are capped at 30 genomes each (seed 21001).
- θ_f (mean reversion): from the family variogram, each bin k with tr Γ(c_k)/tr Σ ∈ (0.05, 0.95) gives
  θ_k = −ln(1 − tr Γ(c_k)/tr Σ)/(2c_k); θ_f is their median.
- β_f (branching): ln(n_f)/mean patristic depth of the family's genomes below the MRCA.
- Side of the line: β_f − 2θ_f.

Readers at the split (the genomes of A ∪ B):
- Pairwise: 200 quartets with two genomes from each side (seed 21002); the four-point method on Euclidean
  composition distances; accuracy = fraction resolving AA|BB.
- Ancestor-aware: leave-one-out centroid classification — each genome is assigned to the side whose centroid
  (computed without it) is nearer; accuracy = fraction assigned to its own side.
Predictions: the joint Gaussian draw from S_fam on the split's genomes (their true pairwise τ; 100 replicates, seed
21003), the same two statistics on each simulated cloud; predicted accuracy = the replicate mean, with its SD.

## Rules (families with both readers computable; ≥ 25 bacterial families expected)
- H1 kernel prediction: pooled over families, |mean observed − mean predicted| ≤ 0.05 for each reader, and the
  per-family median |error| ≤ 0.10 for each reader.
- H2 the ancestor-aware reader's advantage: in ≥ 80% of families the observed centroid accuracy exceeds the observed
  quartet accuracy; and the observed advantage (centroid − quartet) is within 0.10 of the predicted advantage in
  ≥ 70% of families.
- H3 the line (reported, one rule): per family θ_f, β_f, β_f − 2θ_f, the split depth, both accuracies. Rule:
  Spearman ρ ≥ 0.4 between β_f − 2θ_f and the observed centroid accuracy across families (bacteria), the sign the
  theory predicts: further above the line, more of the ancestor survives.
- Verdict (bacteria): HORIZON READ if H1 and H2 pass; PARTIAL if exactly one passes; FAIL otherwise. H3 is scored
  separately. Archaea are reported as replication with the same rules.

## Predictions stated before the run
The centroid reader beats the pairwise reader at every deep split by a margin the kernel predicts (0.05–0.25),
because averaging n leaves per side shrinks the ancestor estimate's noise as 1/√n while a pair's does not. Most
qualifying families sit above the line (dense sampling raises β_f); families near or below it will show the lowest
centroid accuracies. If H1 fails for the centroid reader only, the kernel's covariance across the split is wrong
(the family image is fitted within genera and families, not across the deepest split), which is the Atlas's
"deep collision remainder" again and is reported as such.

## Caveats stated in advance
τ is in substitutions per site of the marker alignment, so θ_f and β_f share units but neither is a clock. The OU
summary θ_f compresses a matrix kernel to one rate. The deepest split's depth differs across families, so H3 is a
cross-family correlation, not a within-family test. The pairwise reader's depth curves (AC2) are already known within
0.02 and are not re-scored.

## Amendment — 2026-10-09 02:18 CEST (file modified 02:18:34; the full run launched 02:18:56 per run.log; the time
## first written here, 03:50, was mis-stated), after a disclosed smoke test on one family (10 replicates), before the
## full run
The deepest split's two sides are drawn from the family's TEST genera only (the genera held out from the kernel fit,
A-curve's convention), so that no genome that shaped the kernel enters the statistics it predicts; the split search
descends the test genomes' MRCA with the same ≥ 10 (≥ 6) rule. The family MRCA, depth, θ_f and β_f use the whole
family as written. The smoke test (one family, both readers, predictions) ran end to end; its numbers are not scored.

## Frozen files (sha256 in horizon21/run.log at launch)
horizon21.py, and acurve.py, k2_packing.py, exp_D_family.py, atlas_predict.py, atlas_predict2.py, atlas_data.py
(unchanged copies in closure/atlas), the Atlas inputs by CHECKSUMS.sha256.
