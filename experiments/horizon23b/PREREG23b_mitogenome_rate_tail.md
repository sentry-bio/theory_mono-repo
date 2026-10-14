# PREREG23b — The rate-tail law on vertebrate mitogenomes (real alignment, second attempt)

Registered 2026-10-14, clock time at freeze in `run.log` (the `date` line precedes the file hashes). Written before
any data file was downloaded. Supersedes nothing: PREREG23 stands as its own record; this registration is the
resolving design it called for (Paper II §5.3, §7.2 item 1), with the four adjustments of the 14 Oct review and the
two points on per-quartet branches and plateau normalisation.

## Claim under test
For a bounded four-point reader on a real nucleotide alignment, the depth to which a split is recoverable from L
sites is predicted, at every L and every depth, by the fitted substitution model and the measured site-rate
spectrum passed through the identical reader, with no free parameter; the rate-weighted reader reads deeper than
the unweighted one and its advantage grows with L; and the readable depth grows as a power of L whose exponent
is set by the density of slow sites, the asymptotes 1/(2(a+1)) and 1/(a+2) for a Gamma fit of shape a.

## Why mitogenomes
Four letters (the derivation's alphabet); a heavy-tailed rate spectrum by construction (second codon positions
near zero rate, third positions saturating); divergences to 2–3 substitutions per site; about eleven thousand
columns, two decades of L; an independent taxonomy (NCBI) to validate splits. PREREG23 failed to resolve on a
shallow, nearly homogeneous protein alignment; the asymptotic regime needs depth well beyond 3a/8.

## Data (public; downloaded after this file is frozen)
NCBI RefSeq release 237, `refseq/release/mitochondrion/mitochondrion.1.genomic.gbff.gz` (403,234,487 bytes;
MD5 from the release's `.md5` file or `release-catalog` checked before use). Complete mitochondrial genomes
whose lineage contains "Vertebrata"; the thirteen protein-coding genes by their standard names (ND1, ND2, COX1,
COX2, ATP8, ATP6, COX3, ND3, ND4L, ND4, ND5, ND6, CYTB), taken from CDS features; records lacking any gene, or with
a gene shorter than 70% of the median length for that gene, are dropped. Subsample T = 1,500 genomes (seed 23),
stratified by NCBI class so that no class exceeds 300; the taxonomy lineage of every record is kept.

## Fixed design (scripts frozen and hashed in `run.log` before the verdict run)
1. **Alignment.** MAFFT 7.526 `--auto` per gene (nucleotide), genes concatenated in the standard order; columns
   that are gaps or ambiguous (`- ? N .`) in more than 50% of sequences dropped. Tape length L_max.
2. **Tree and model.** IQ-TREE 2.4.0, `-m GTR+F+R10` (free rates; if R10 does not converge, R8, then R6, in that
   order, recorded), default search, `-seed 23`, memory capped at 12 GB, under `nice`. From the final tree:
   branch lengths; the GTR exchangeabilities and base frequencies; the R-class rates and weights (the site-rate
   spectrum); `-wsr` posterior-mean site rates (the weighted reader's rates).
3. **Quartets and the truth set.** Internal edges with length τ in [0.02, 0.50]; at each endpoint the two
   subtrees (the complement at the parent side); up to four quartets per edge with distinct tip sets by the
   balanced-depth rule of PREREG23 amendment (iv) (targets at the 20/40/60/80% quantiles of the pooled depths);
   the four tip depths within a factor 1.5. **Truth set:** a quartet AB|CD is kept only if NCBI taxonomy implies
   the split: at some rank of order or above, A and B share a taxon containing neither C nor D, and C and D share
   a taxon containing neither A nor B. Depth t = mean of the four tip-to-endpoint lengths; eight log-spaced bins
   from 0.05 to 3.0; at most 400 quartets per bin (seed 23).
4. **Readers.** L in {64, 128, 256, 512, 1024, 2048, 4096, 8192} (truncated at L_max), 40 random column subsets per
   quartet (seed 23), gap-containing columns excluded per quartet. (U) unweighted four-point mismatch; (W)
   rate-weighted contrast with per-site weights s_i/v_i computed numerically from the fitted model for the
   quartet's own five branch lengths and the site's posterior-mean rate; (S) the same with rates permuted across
   sites. **RY arm:** the alignment recoded to purine/pyrimidine, readers U_RY and W_RY, where the two-state
   formula of the derivation is exact.
5. **Prediction, no free parameter.** For every quartet, L and reader, the predicted recovery probability is
   computed by parametric simulation from the fitted model on the quartet's own branches with the quartet's own
   site rates (sites drawn from the R-class spectrum), 200 replicate subsets per cell, through the identical
   reader. The predicted and observed recoveries then pass through the identical estimator (step 6). No κ.
6. **Estimator.** Per L and reader, recovery against depth smoothed by isotonic regression (monotone
   non-increasing in t, pooled over quartets, weighted by subsets); t*(L) is the depth at which the smoothed
   recovery equals 0.75 of that depth bin's full-length recovery (plateau normalisation, applied identically to
   the observed and the predicted curves). A cell with no interior crossing is UNRESOLVED.
7. **Exponents.** Predicted and observed log–log slopes over the top three resolved L. Gamma shape a fitted to the
   R-class spectrum by maximum likelihood on the (rate, weight) pairs; asymptotes 1/(2(a+1)) and 1/(a+2) reported.

## Verdicts (fixed here; both arms scored, the 4-letter arm decides)
- V1 form, unweighted: predicted t*(L) within ±20% of observed at every resolved L ≥ 128.
- V2 form, weighted: same rule.
- V3 ordering: observed W above U at every resolved L ≥ 128 and the ratio at the largest resolved L exceeds the
  ratio at L = 128; the prediction shows the same ordering.
- V4 exponent: for each reader, observed slope within ±0.06 of the predicted slope over the same L.
- V5 shuffle control: S within ±15% of U at every resolved L ≥ 256.
- V6 RY arm: V1–V3 at ±25% on the RY readers (reported beside; a failure here is reported, not decisive).
Overall: LAW SUPPORTED ON REAL DATA only if V1–V5 pass. No post-hoc change of grid, bins, truth-set rule,
normalisation level, tolerances or reader definitions; amendments dated and before the data they concern.

## Disclosed smoke test
100 taxonomy-concordant quartets, L in {128, 2048}, 10 subsets, 20 predicted replicates, same code paths; kept,
not interpreted.

## Readings (reported, not scored)
Recoverable fraction (full-length plateau) by depth bin; the R-class spectrum and its Gamma fit; the depth
3a/8 at which the asymptotic regime begins; L_max; the fraction of quartets rejected by the truth-set rule.

## Compute and data handling
biosphereatlas (ssh rohit@100.86.142.125), one scratch directory `/fast/scratch_h23b/` holding a Python venv
(numpy, biopython), IQ-TREE 2.4.0 Linux, MAFFT 7.526 Linux, the download, the alignment and the tree; everything
under `nice`; nothing outside the scratch directory touched; the scratch directory and any caches deleted after
the results (small JSON and logs) are copied here, after an audit that the copies match. The raw download is
public-domain NCBI data and is not kept.

## Amendments
- 2026-10-14, after the download and gene extraction and before alignment results, tree or any reader result were
  read (time in `run.log`): the NCBI lineage strings in GenBank records list taxon names without ranks, so the
  truth-set rule's clause "at some rank of order or above" cannot be applied as written. The rule is now: a
  quartet AB|CD is kept if some taxon in the lineage of both A and B is absent from the lineages of C and D, and
  some taxon in the lineage of both C and D is absent from the lineages of A and B, excluding the four named
  classes' superset names that every vertebrate shares. The class field recorded by `fetch_mito.py` is unchanged.
  Also recorded: the class list missed ray-finned fishes (NCBI uses "Actinopterygii"), which fell into "other"
  (229 chosen); this affects only the stratification label, not the data.
- 2026-10-14, during the tree search and before any reader result (time in `run.log`): the registered "default
  search" (stop after 100 iterations without improvement) is running at about 85 minutes per iteration on 1,500
  taxa × 11,422 columns under GTR+F+R10 (better trees at iterations 1 and 2, log-likelihoods −6,239,092 and
  −6,238,351), which would take days. The search is capped: IQ-TREE is resumed from its own checkpoint with
  `-n 3`, so the final tree is the best found after at most three iterations; branch lengths are then re-optimised
  under the fixed topology in the `-wsr` run as registered. The topology's only roles are the quartet depths and the
  taxonomy-checked truth set, neither of which the registration ties to search convergence.
- 2026-10-14 09:47:52 UTC (11:47 CEST), before any reader result: the capped-search amendment above is **withdrawn,
  not applied**. The 85-minute-per-iteration estimate was the NNI pass on the 20 best initial trees (the log's
  "iterations" 1 and 2); once the main search began, iterations took minutes (iteration 10 at 3 h 58 min, better
  trees at iterations 1, 2 and 8), and the checkpoint written at 06:21 UTC holds no search state (22 lines), so a
  resume with `-n 3` would have discarded four hours of search for no gain. The registered default search runs on
  unchanged (pid 1830572); `finish_tree2.sh` (hash in `run.log`) waits for it and then runs the `-wsr` site-rate step
  exactly as in `finish_tree.sh`. The design of step 2 is therefore as registered.
- 2026-10-14 18:18:06 UTC (20:18:06 CEST), **amendment (iv)**, after the registered quartet draw was summarised
  (986 edges in the τ band, 3,944 targets, 103 depth-balanced candidates, 3 kept) and before any reader result: the
  truth-set rule's second clause, "C and D share a taxon containing neither A nor B", is unsatisfiable by the
  sampling construction of step 3, which takes C from the sister subtree and D from the complement above the edge,
  so that the taxa C and D share always contain A and B; the three quartets it kept are tree–taxonomy conflicts. The
  first clause alone ("A and B share a taxon containing neither C nor D") certifies the split AB|CD and was the
  intended rule. The diagnostic `diag23b_quartets.py` (hash in `run.log`; it reads only the tree and the taxonomy)
  gives: registered rule 3 kept; one-sided rule 43 kept under the registered balance (factor 1.5, four targets);
  104 with factor 2.0; 112 with eight targets; 256 with factor 2.0 and eight targets; no taxonomy rule 103. Every
  balanced quartet on this tree lies at depth 0.39–1.08 (bins 4–5; tip depths from the root run 0.14–2.0), so the
  shallow bins are empty under any rule. Decision: the registered pipeline runs unchanged on the registered quartet
  file and gives the verdict of record; two labelled secondary analyses are reported as readings, not as the
  registered verdict: S1 = one-sided rule with the registered balance (43 quartets), S2 = one-sided rule, balance
  factor 2.0, eight targets (256 quartets; the only change to step 3 beyond the clause). Scripts
  `quartets23b_amended.py` and `pipeline23b.sh` (hashes in `run.log`); `run23b.py` unchanged
  (31d3e620…). The smoke test of the registration is run on S2 and kept, not interpreted.
