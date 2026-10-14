# RESULTS — PREREG23b, the rate-tail law on vertebrate mitogenomes (14 October 2026)

Registration frozen 07:40:28 CEST (hash 03dee339…); amendments (i) 07:46:12 CEST (truth-set rule without ranks),
(ii) 11:42:53 CEST (capped search; withdrawn 11:47:52 CEST before any reader result, the default search ran as
registered), (iii) see run.log, (iv) 18:18:06 UTC (the truth-set rule's second clause unsatisfiable by construction;
secondary analyses). Clock times below are UTC from `run.log` (CEST = UTC + 2).

## Verdict of record (the registered pipeline, unchanged, on the registered quartet draw)

**NOT SUPPORTED AS REGISTERED.** V1–V6 all fail: no cell is resolved. The registered truth-set rule kept 3 quartets
of 103 depth-balanced candidates (986 edges in the τ band, 3,944 targets), because its second clause ("C and D
share a taxon containing neither A nor B") cannot be satisfied by the sampling construction of step 3, which takes
C from the sister subtree and D from the complement above the edge; the three quartets it kept are tree–taxonomy
conflicts (full-length four-point recovery 0.33). This is a defect in the registered rule, found after the quartet
summary and before any reader result, and it is recorded as amendment (iv), not repaired in the verdict.

## Secondary analyses (amendment iv; reported as readings, not as the registered verdict)

S1: one-sided truth-set rule, registered depth balance (factor 1.5, four targets): 43 quartets, depth bins 4–5.
S2: one-sided rule, balance factor 2.0, eight targets: 256 quartets, bins 2–5 (1, 9, 143, 103). Scripts
`quartets23b_amended.py`, `pipeline23b.sh` (hashes in `run.log`); `run23b.py` unchanged (31d3e620…). The
registration's smoke test (100 quartets, L ∈ {64, 128, 2048}, 10 subsets, 20 replicates) ran on S2 at 18:18:10 and
is kept, not interpreted (`work/reads_S2smoke.json`, `work/pred_S2smoke.json`).

Applying the registered rules to S1 and S2 gives the same outcome: every cell UNRESOLVED (the plateau-normalised
isotonic depth curve has no interior crossing at 0.75; where a crossing exists it sits at the shallowest quartet,
t = 0.235). The reason is structural: on this tree every depth-balanced taxonomy-certified quartet lies at depth
0.23–1.08 substitutions per site (tip depths from the root run 0.14–2.0; the shallow bins are empty under any rule),
and about 30% of quartets are not recovered at full length, so the curve never falls from a plateau to 0.75 of it
inside the available depth range.

## Readings (S2, 256 quartets, 40 subsets per quartet, 200 predicted replicates per cell)

Pooled recovery, observed / predicted with no free parameter (per-quartet GTR+F+R10 simulation on the quartet's own
five branches with its own site rates, through the identical reader):

| L | U obs/pred | W obs/pred | S obs | U_RY obs/pred | W_RY obs/pred |
|---|---|---|---|---|---|
| 64 | 0.380 / 0.375 | 0.463 / 0.438 | 0.392 | 0.340 / 0.318 | 0.452 / 0.425 |
| 128 | 0.431 / 0.417 | 0.512 / 0.489 | 0.423 | 0.405 / 0.381 | 0.497 / 0.479 |
| 256 | 0.486 / 0.472 | 0.573 / 0.554 | 0.467 | 0.459 / 0.444 | 0.552 / 0.541 |
| 512 | 0.542 / 0.536 | 0.632 / 0.628 | 0.503 | 0.531 / 0.525 | 0.623 / 0.618 |
| 1024 | 0.592 / 0.618 | 0.692 / 0.721 | 0.544 | 0.608 / 0.612 | 0.691 / 0.707 |
| 2048 | 0.623 / 0.706 | 0.729 / 0.807 | 0.577 | 0.675 / 0.706 | 0.745 / 0.793 |
| 4096 | 0.658 / 0.791 | 0.772 / 0.886 | 0.621 | 0.729 / 0.796 | 0.796 / 0.873 |
| 8192 | 0.682 / 0.860 | 0.807 / 0.939 | 0.643 | 0.768 / 0.867 | 0.836 / 0.933 |
| full (11,422) | 0.691 / 0.885 | 0.820 / 0.959 | 0.648 | 0.770 / 0.894 | 0.863 / 0.953 |

1. **The parameter-free prediction matches the observed recovery at every L ≤ 512, for every reader**, within
   0.025 (U) and 0.025 (W) pooled, and within 0.03 in each populated depth bin. This is the finite-L content of
   the derivation (exact per-site contrast and variance under the fitted model and the measured rate spectrum)
   confirmed on real mitogenomes at the level of recovery curves. It is not the registered t*(L) form.
2. **The rate-weighted reader beats the unweighted one by the predicted margin, and the margin grows with L**:
   observed W − U from +0.08 at L = 64 to +0.125 at L = 8192; predicted +0.06 to +0.10 (V3's content, in recovery
   rather than depth). **The shuffled control does not**: S − U is −0.01 to −0.05 at every L, so the gain is carried
   by the rates themselves, not by the spread of the weights. This is the contrast PREREG23 could not reach at
   α = 1.74; here the fitted Gamma shape of the R10 spectrum is a = 0.43 (24% of sites at relative rate 0.005, a
   tail to 4.1).
3. **A floor, seen for the second time on real data** (readings 6–7, added 15 October, locate it on short internal
   edges, show it is reader-dependent, and show the shortfall falling with depth)**.** From L = 1024 the observed curves bend
   away from the prediction toward a plateau: full-length recovery is 0.69 (U), 0.82 (W), 0.77 / 0.86 in the RY arm,
   against predicted 0.89–0.96. About a quarter to a third of taxonomy-certified quartets are not recovered by a
   four-point distance reader with the whole alignment (PREREG23 on bacterial proteins: about a quarter). The
   derivation has no term for this; it is the obstacle to the depth law in its registered form on both data sets.
4. Full-length recovery does not fall with depth over the available range (bin 3, n = 9: 0.56; bin 4: 0.66;
   bin 5: 0.75), so the depth dependence the estimator needs is not present between 0.23 and 1.08 substitutions
   per site on this tree; the exponents 1/(2(a+1)) = 0.350 and 1/(a+2) = 0.412 (asymptotes for a = 0.43; regime
   depth 3a/8 = 0.16) are untested in nature in either direction.
5. S1 (43 quartets, bins 4–5) shows the same three features (prediction within 0.07 at L ≤ 512; W − U positive
   and growing; full-length 0.74 / 0.77).
6. **Post-hoc reading (00:56 CEST, 15 October; `floor23b.py`; not registered). The floor is a function of the reader and
   sits on short internal edges, not at depth.** Full-length shortfall below the parameter-free prediction: U 0.19,
   W 0.14, U_RY 0.12, W_RY 0.09 (observed 0.69 / 0.82 / 0.77 / 0.86 against predicted 0.89 / 0.96 / 0.89 / 0.95).
   A floor of wrong certifications would be reader-independent; this one is halved by rate-weighting plus RY-coding,
   and 14 of 256 quartets fail under all four readers (U fails and W recovers 44; the reverse 11; both fail 35).
   The quartets unrecovered by U at full length have median internal edge 0.035 substitutions per site against
   0.069 for the recovered ones, at the same median depth (0.61 vs 0.63), and the model predicts 0.80 for them.
   By tertile of edge length the U shortfall is 0.31 (edges < 0.039), 0.16 (0.039–0.079) and 0.12 (> 0.079); in the
   longest tertile the RY-coded readers show no shortfall at all (−0.006, −0.001) and W 0.02.
7. **Why the depth estimator saw recovery rising with depth.** Predicted full-length recovery falls with depth as
   the law says (bins 3/4/5: 0.98 / 0.90 / 0.86 for U) while observed rises (0.56 / 0.66 / 0.75), because the
   shortfall falls with depth faster (0.42 / 0.24 / 0.11). The contrast is a function of depth t and edge τ together
   (¾ e^{−2ρt}(1 − e^{−ρτ}), Paper I's window theorem); corr(t, τ) is only 0.13 on this draw, and τ spans
   0.026–0.17 between its 10th and 90th percentiles while t spans 0.23–1.08. The per-quartet prediction carries both
   variables; the registered one-dimensional isotonic curve in t cannot.

## What it means for Paper II

The law's two ingredients that the registration could test on this tree are confirmed: the finite-L recovery of
both readers is predicted with no free parameter up to 512 sites, and the rate-weighted reader's advantage is real,
rate-specific and growing with L; across the two alignments the gain is absent where the spectrum is flat (α = 1.74)
and present where it has a slow tail (a = 0.43), a two-point, sign-specific test of the mechanism. What is not
confirmed is the depth law itself, because (i) the registered truth-set rule was defective, (ii) the registered
estimator projected recovery onto depth alone while the contrast depends on depth and edge together, and (iii) a
reader-dependent floor on short internal edges, a bias that more sequence does not average away, is outside the
stationary model. The third design (Paper II §7.2) makes the prediction the estimator: a floor term fitted once;
observed against predicted recovery across L with the exponent entering through the model's length scaling;
quartets drawn with the edge-to-depth ratio controlled and certified below 0.2 substitutions per site; a one-sided
truth-set rule; and four-taxon maximum likelihood on every unrecovered quartet, to separate the reader's floor from
tree-level inconsistency.

## Data and provenance

RefSeq release 237 `mitochondrion.1.genomic.gbff.gz` (403,234,487 bytes, MD5 4491799651740f49c8f6a011cf9a96e5;
deleted after use). 18,235 records; 7,858 vertebrate; 7,770 complete; 7,749 with all 13 PCGs; 7,743 after the
length filter; 1,500 chosen (seed 23, cap 300 per class). MAFFT 7.526 `--auto` per gene; 14,527 raw columns, 11,422
kept. IQ-TREE 2.4.0, GTR+F+R10, default search, seed 23, 8 threads, 12 GB cap, under nice: 394 iterations, best
tree at iteration 293, log-likelihood −6,237,215.20, tree length 245.37 (search 05:46–17:34 UTC); site rates on the
fixed topology (`-te … -wsr`, 17:35–18:14 UTC), 11,422 rates. Quartets 18:15:00; diagnostic 18:16:43; amendment
(iv) 18:18:06; readers, predictions and scores 18:18:08–18:19:04. Files: `results/score23b*.json`,
`work/quartets*.json`, `work/reads*.json`, `work/pred*.json`, `work/iq.iqtree`, `work/iqr.iqtree`,
`work/iq.treefile`, `work/iqr.rate`, `logs/`; post-hoc reading script `floor23b.py` (15 October, on the S2 files, not
registered; its output is reproduced in readings 6–7). Scratch `/fast/scratch_h23b` audited against these copies and deleted.
