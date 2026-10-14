# Natural CRISPR arrays as tapes — pre-registration (2026-09-28, written before any array statistic was computed)

Claim under test (the ceiling shot): a natural, selected recorder operates on the bound. A CRISPR array is an ordered
tape: spacers are written at the leader end at some rate a, the array length is held near a cost-set cap L, and old
spacers are lost from the trailer end. The packing law then predicts the tape's whole memory curve from two
independently measured numbers, with the two horns of the recorder law visible in nature:
- write-limited horn (shallow): strains that diverged recently carry identical arrays (nothing written);
- room-limited horn (deep): beyond a horizon the arrays share no spacer (history pushed off the tape).

## Data
- Genomes: bacterial and archaeal catalogue genomes that are GTDB r220 tree leaves with local FASTA on biosphereatlas
  (≤ 200 contigs, ≥ 1 Mb). Arrays called with pilercr 1.06 (defaults; MinCED 0.4.2 if pilercr fails to build),
  arrays with ≥ 3 spacers kept; spacer sequences canonicalised (lexicographic min of sequence and reverse
  complement); per-array repeat consensus canonicalised.
- Homologous arrays between two genomes: identical canonical repeat consensus. Genomes with several arrays sharing a
  repeat contribute their union of spacers to sharing counts but are excluded from the order test.
- Pairs: genomes of the same GTDB species (and, for the horizon, the same genus), patristic τ from the r220 tree.
  A species qualifies with ≥ 20 array-bearing genomes and ≥ 50 pairs; τ bins geomspace over the species' range, 8 bins.

## Statistics per species
S = shared spacers of a pair; L_A, L_B = array lengths; P = private spacers; I(τ) = fraction of pairs with identical
spacer sets; L̄ = mean array length over the species' arrays.

## Predictions and rules
- C1 write-limited horn: I(τ) ≈ exp(−2aτ) at shallow τ. a is fitted by log-linear regression of I on τ over the
  three shallowest bins with ≥ 20 pairs. Reported: a per species; PASS if the fit explains I in the next bin within
  ±0.15 (a genuine extrapolation).
- C2 tape horizon (the bound's identity: memory depth = capacity / write rate): predicted τ_h = L̄ / a. Observed
  τ_h = the smallest τ bin (≥ 20 pairs) whose median S / min(L_A, L_B) ≤ 0.1. PASS if observed within a factor of 2 of
  predicted in ≥ 2/3 of qualifying species with a finite observed horizon. Alternative that would fail it: random
  spacer loss (an unordered set), which makes S decay exponentially with no finite horizon tied to L̄/a.
- C3 order is the resource: for pairs with 1 ≤ S < min(L_A, L_B) and single arrays, shared spacers form a contiguous
  block at the same terminal end of both arrays. Null: 1,000 within-array order permutations. PASS if the observed
  contiguous fraction is ≥ 0.5 and ≥ 3× the null median in ≥ 2/3 of qualifying species.
- C4 filling fraction (at capacity): among pairs beyond the observed horizon, median P / L̄ ≥ 0.8 in species passing
  C2 (full tapes). Species whose I(τ) stays ≥ 0.5 at the deepest bin are STATIC (write rate ≈ 0: the slack, no-writing
  horn) and are reported separately; the prediction is that such species also show no finite horizon.

## Caveats stated in advance
τ is marker-protein divergence, so a is per unit τ and only the product L̄/a is unit-free. Horizontal transfer of
whole CRISPR loci breaks the lineage assumption; species where spacers are shared across large τ but not at
intermediate τ will be flagged as transfer-affected and excluded from C2 only if the pattern is non-monotone.
Multiple CRISPR–Cas types per genome are handled by repeat matching. The GTDB tree is not ultrametric; τ is a
distance, not a time.

## Verdict
The tape identity is SUPPORTED if C2 and C3 pass; the two horns are DEMONSTRATED if C1 and C4 pass in addition.

## Clarification — 2026-09-28 14:08, after the pilercr smoke test, before any array statistic
pilercr reports arrays in contig orientation; the leader end and strand are not identified. C3 is therefore
evaluated as: the shared spacers form a contiguous block at a terminal end of each array (either end), which is the
FIFO signature independent of strand; the permutation null is unchanged. Arrays with ≥ 3 spacers are kept (so ≥ 4
repeats). Runtime measured: 0.85 s per genome; 12,151 genomes (9,928 bacteria, 2,223 archaea) will be called.

## Amendment — 2026-09-28 14:39, before any array-sharing statistic (structural findings only so far)
- The GTDB r220 trees carry one genome per species (77,330 bacterial leaves = 77,330 species), so the registered
  within-species pairs do not exist on the tree; within-genus species-representative pairs are deep (median τ
  0.19–0.64) and only 7 bacterial genera have ≥ 20 array-bearing species. Arrays were called on 12,151 tree genomes
  (4,440 with ≥ 1 array of ≥ 3 spacers); no sharing statistic has been computed.
- The species-level design is therefore run on STRAINS from the full catalogue with local FASTA (bacteria, ≤ 200
  contigs, ≥ 1 Mb, named species): 116 species have ≥ 20 such strains; ≤ 60 strains per species are drawn (seed 11).
  Divergence: Mash distance d = −(1/21)·ln(2J/(1+J)) from bottom-5,000 sketches of canonical 21-mers (J = Jaccard),
  in place of tree τ; all rules C1–C4 unchanged with d for τ; qualification ≥ 20 array-bearing strains and ≥ 50 pairs
  (all pairs used). Bins: geomspace over the species' d range, 8 bins, ≥ 20 pairs each.
- The genus-level species-representative pairs are reported as the deep-regime complement (shared fraction vs τ
  only); C2 is not evaluable there because a is not identifiable without shallow pairs.

## Strain-level result as registered — 2026-09-28 15:17
4,851 strains called (2,425 with ≥ 1 array of ≥ 3 spacers); 114,653 within-species pairs; 56 qualifying species.
C1 23/28 (largely trivial: identical arrays ≈ 0 at every depth in most species; substantial only in C. difficile 0.48,
T. cocleata 0.56, T. ramosa 0.89, Muribaculum 0.60, A. muciniphila_A 0.50, where a > 0). C2 0/14: observed horizons
d_h ≈ 0.003–0.02 are 10–100× shallower than L̄/a in every evaluable species. C3 9/32: contiguity of shared spacers
is 10–1000× above the permutation null in most species but below the absolute 0.5 rule. C4 not evaluable (0/0);
beyond the observed horizon P/L̄ = 0.7–1.1 everywhere. Static: 1 species. Verdict as registered: NOT SUPPORTED.
Flag raised before any re-analysis: the horizon is implausibly shallow and uniform (including M. tuberculosis, whose
DR locus is species-wide), consistent with inconsistent repeat-boundary placement between genomes defeating exact
spacer matching. Diagnostic to follow; any re-scoring with a tolerant matcher will be recorded as an amendment.
- 2026-09-28 15:19 Diagnostic outcome: the boundary-artifact explanation is RULED OUT. Over 8,012 very close
  pairs (Mash d < 0.001), exact spacer matching gives a median shared fraction of 1.00 (a central-24-mer matcher is
  worse, 0.84). Close strains share arrays exactly; the shallow horizons are real. The registered verdict stands.
