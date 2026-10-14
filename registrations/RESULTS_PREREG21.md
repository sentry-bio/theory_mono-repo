# PREREG21 — results (bacteria run 2026-10-09 02:18:56–02:50 CEST, 1,857 s; archaea 339 s; hashes in run.log;
# horizon21_{bac,ar}.json; scored by the registered rules, with the 02:18 amendment — test genera only — in force)

## Bacteria (36 families; every family's deepest split among its test genera, ≤ 30 genomes per side)
- H1 kernel prediction: pooled quartet accuracy observed 0.733 vs predicted 0.726 (median per-family |error| 0.087);
  pooled centroid accuracy 0.897 vs 0.892 (median |error| 0.044). **PASS** (both pooled gaps ≤ 0.05, both medians
  ≤ 0.10).
- H2 the ancestor-aware reader's advantage: centroid > quartet in 32 of 36 families (89% ≥ 80%); the observed
  advantage within 0.10 of the predicted advantage in 26 of 36 (72% ≥ 70%). **PASS**, the second clause narrowly.
- H3 the line: θ_f = 0.9–4.3, β_f = 9.3–23.0, so β_f − 2θ_f = +6.0 to +16.4 — **every family is above its
  composition line**; Spearman(β − 2θ, centroid accuracy) = +0.24 (sign as predicted, below the 0.4 rule). **FAIL** as
  registered; no family below the line, so the rule had no contrast to find.
- **Verdict: HORIZON READ** (H1 and H2).

Per family (obs/pred): quartet from 0.395/0.579 (Lachnospiraceae) to 1.000/0.891 (Cyanobiaceae); centroid from
0.750/0.797 (CAG-272) to 1.000/0.947. The four families where the pairwise reader beat the centroid are those with
quartet accuracy ≥ 0.93 already (Cyanobiaceae, Enterobacteriaceae, Sphingobacteriaceae, Xanthobacteraceae): a
ceiling, not a reversal.

## Archaea (9 families; replication)
- H1: quartet 0.908 observed vs 0.828 predicted (gap 0.080 > 0.05; median |error| 0.074); centroid 0.956 vs 0.915
  (gap 0.041; median 0.056). **FAIL** on the quartet reader's pooled gap.
- H2: advantage positive in 6 of 9 (67% < 80%); within 0.10 of prediction in 9 of 9. **FAIL** on the first clause.
- H3: all 9 above the line (+3.7 to +12.5); Spearman −0.05. **FAIL.**
- **Verdict: FAIL** (replication). The kernel under-predicts both readers in archaea — real archaeal genomes separate
  across their deepest splits better than their family image says (the same direction as A-arch's residual: reality
  more compact within clades, hence more separable between them) — and the pairwise reader sits at 0.92–1.00 in six
  of nine families, leaving the centroid reader no room to show an advantage.

## Readings (separate from the verdicts)
1. On bacteria, both readers are predicted from the frozen family kernels with nothing fitted: the pairwise reader
   to a median 0.09, the ancestor-aware reader to a median 0.04. The ancestor-aware reader recovers the deepest
   split at 0.90 against the pairwise reader's 0.73, a gain of 0.16 that the kernel also predicts (0.89 vs 0.73).
   Averaging a clade's leaves beats the trait's forgetting; a pair does not.
2. Composition's own line, β = 2θ, is not reached by any qualifying family: with dense sampling the branching rate
   (ln n over the family's mean depth, 9–23) is far above twice the trait's mean-reversion rate (θ ≈ 1–4). In the
   Kesten–Stigum sense the ancestor of every family survives in its leaves' mean, and the horizon that binds on
   the Atlas is the pairwise reader's exponential cost, not the trait's window. Where the window would bind is at
   depths or sampling densities below any family here; the cross-family rule could not see the line because no
   family sits on its far side. This is a finding about the Atlas's regime, not a failure of the line.
3. The archaeal miss is informative in the same way as A-arch: the family image is too diffuse for archaea, so it
   under-predicts separability (and over-predicts distinctness within genera). The Atlas's next kernel should be
   fitted across the deepest split as well as within genera and families.
4. For EAG v4 §5 (the contrast): "composition cannot carry deep genealogy alone" stands, with its mechanism now
   measured — bounded room (η ≈ 0.01, PREREG20 Atlas arm), a reader tax that an ancestor-aware reader halves at the
   deepest splits, and a line that the sampled families all sit above. The ancestor-aware reader is the Atlas's next
   reader.
