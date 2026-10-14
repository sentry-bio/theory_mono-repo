# PREREG23 — The rate-class test on a public phylogenomic alignment (GTDB bac120)

Registered 2026-10-14, clock time at freeze in `run.log` (the `date` line precedes the file hashes). Written before
any data file was downloaded or read. This is Paper II's frontier item (1): the first real-data test of the
rate-tail law (`paper2/RATE_TAIL_DERIVATION.md`, confirmed in simulation by PREREG22).

## Claim under test
On a real concatenated alignment with an inferred reference tree, the depth to which a four-point (distance)
reader recovers a split from L subsampled sites follows the exact Fisher curves of the derivation, with the
site-rate Gamma shape a estimated independently on the same alignment, and with the reader-dependence of the
exponent: the rate-weighted reader reads deeper than the unweighted one and its advantage grows with L. The
exponents 1/(2(a+1)) and 1/(a+2) are the asymptotes of those curves; the alphabet (here amino acids) changes the
curves' constants, not the exponents, because the exponents are set by the density of slow sites near zero rate.

## Data (public; CC BY-SA 4.0; downloaded after this file is frozen)
- GTDB release `latest` (VERSION.txt recorded in `run.log`): `genomic_files_reps/bac120_msa_reps.faa.gz`
  (the 120-marker concatenated amino-acid alignment of the bacterial representative genomes, masked) and
  `bac120.tree.gz` (the bacterial reference tree of the same representatives, branch lengths in expected
  substitutions per site). `MD5SUM.txt` is downloaded first and both files are checked against it before use.
- Honest circularity: the tree was inferred from this alignment. The test asks how much of that tree a bounded
  reader recovers from L of its sites; depths are measured on the reference tree.

## Fixed design (scripts frozen and hashed in `run.log` before the verdict run)
1. **Subsample taxa.** T = 1,500 representatives chosen uniformly at random (seed 23) among those present in both
   files. The tree is pruned to them (unary nodes collapsed, branch lengths summed). Columns that are gaps or
   ambiguous in more than 50% of the subsample are dropped; the remaining columns are the tape, of length L_max.
2. **Site rates and shape.** IQ-TREE 2 (v2.4.0 binary, hash recorded), fixed pruned tree (`-te`), model
   `LG+G4`, `-n 0`, `-wsr`: the Gamma shape α and the posterior-mean rate per site. α is the registered shape
   parameter a; the per-site rates (normalised to mean 1) are the weighted reader's rates. Branch lengths are
   re-optimised on the fixed topology by the same run and the re-optimised lengths are used for depths.
3. **Quartets.** Every internal edge of the pruned tree with length τ in [0.02, 0.20] substitutions per site defines
   candidate quartets: one tip from each of the two subtrees at each endpoint, each chosen as the tip whose
   path length to that endpoint is closest to the edge's median tip depth. Depth t of a quartet is the mean of the
   four tip-to-endpoint path lengths; quartets whose four tip depths differ by more than a factor 1.5 are dropped.
   Up to 3,000 quartets are kept, stratified in eight log-spaced depth bins from t = 0.05 to 4.0 (at most 400 per
   bin, seed 23).
4. **Readers.** For each quartet and each L in {64, 128, 256, 512, 1024, 2048, 4096} (L ≤ L_max; if L_max < 4096
   the grid stops at the largest power of two ≤ L_max), 40 random column subsets (seed 23). Columns with a gap
   in any of the four sequences are excluded from that quartet's subset counts. (U) unweighted four-point mismatch
   reader; (W) rate-weighted contrast reader with per-site weights s_i/v_i computed from the IQ-TREE rate r_i and
   the quartet's (t, τ) under the 20-letter symmetric channel at the quartet's own depth. Success = the true split
   is the strict minimum of the three four-point sums.
5. **Readable depth.** For each (L, reader), success is modelled as a logistic function of ln t over all quartets
   (weighted by subsets); t*(L) is the depth at which the fitted success equals 0.90. If the fit never crosses
   0.90 at the shallow end or never falls below it at the deep end for some L, that cell is UNRESOLVED and the
   verdicts that need it fail.
6. **Prediction.** The exact curves of the derivation with the 20-letter constants (p = 1/20 + 19/20·e^{−20rℓ/19}),
   Gamma(a = α) integrated by 400,000 fixed-seed draws, κ fitted once per reader on the L = 64 cell; every other
   cell predicted with no free parameter.

## Verdicts (one per claim; rules fixed here)
- V1 form, unweighted: predicted t*(L) within ±25% of observed at every L ≥ 256.
- V2 form, weighted: same rule, weighted reader.
- V3 ordering: weighted t* > unweighted t* at every L ≥ 128, and the ratio at the largest L exceeds the ratio at
  L = 128.
- V4 exponent: for each reader, the observed log–log slope over the top three L values is within ±0.08 of the
  exact-curve slope over the same values (both exponents predicted from α in advance).
- V5 shuffle control: with the per-site rates permuted across sites (seed 23), the weighted reader's t*(L) falls
  within ±15% of the unweighted reader's at every L ≥ 256 (the advantage comes from the rates, not the weights'
  form).
Overall: LAW SUPPORTED ON REAL DATA only if V1–V5 all pass; any failure is reported as such with its cells.
No post-hoc change of tolerances, grid, bins, κ-fit cell, taxon count or reader definition. Amendments must be
dated and precede the data they concern.

## Disclosed smoke test
Before the verdict run: 100 quartets, L ∈ {64, 512}, 10 subsets, on the same subsample, to validate the code
paths (`smoke23.json` kept; no verdict read from it).

## Readings (reported, not scored)
- α and the fitted κ per reader; the depth distribution of quartets; the fraction of UNRESOLVED cells if any.
- Local slopes against the asymptotes 1/(2(α+1)) and 1/(α+2).
- A free fit of the shape parameter to the observed curves, compared with α.

## Data handling
Downloads go to `horizon23/data/` (untrusted-data directory, never executed from, excluded from any commit);
intermediate files (pruned tree, sub-alignment, IQ-TREE outputs) are kept under `horizon23/work/`; results are
small JSON files beside this registration. The raw downloads are deleted after the results are recorded and
their hashes logged.

## Amendments
- 2026-10-14, before the alignment download finished and before any alignment column was read (time in
  `run.log`): two design details the registration left implicit are fixed. (i) The prediction curves use, for
  the internal branch, the median τ of the kept quartets (τ enters the constants, which κ absorbs, and weakly the
  shape). (ii) "Gap or ambiguous" means any of `- ? X . *`. (iii) The quartet depth bins and the logistic fit use
  the IQ-TREE re-optimised branch lengths, as step 2 states.
- 2026-10-14, after the tree-only diagnostic `diag23.py` on the pruned tree and before any reader result was
  computed (IQ-TREE was running; no reader had read a column; time in `run.log`): (iv) the tip-pick rule of step 3
  is replaced. On this tree the "closest to the median depth" rule leaves only 2% of edges with the four tip
  depths within a factor 1.5 (21 quartets in total). The rule is now: among candidate target depths taken from
  the four pools (25 quantile points per pool), choose the target that minimises the max/min ratio of the four
  closest-depth picks; the factor-1.5 balance rule is unchanged. (v) The tree's tip depths span about 0.05–1.3
  substitutions per site, so the registered depth bins 0.05–4.0 have empty top bins; the eight log-spaced bins now
  run from 0.03 to 1.5. (vi) If the L = 64 cell is UNRESOLVED for a reader, κ for that reader is fitted on the
  smallest resolved L instead (stated here as the only fallback); V1/V2 then evaluate cells with L ≥ 4 × (fit L),
  V3 cells with L ≥ 2 × (fit L), V5 cells with L ≥ 4 × (fit L). Tolerances and all other rules unchanged.
- 2026-10-14, at the disclosed smoke read, before any reader result existed: (vii) a code bug in `run23.py read`
  (sequence byte arrays were built from the taxon names instead of the sequences; the smoke run crashed on the
  shape mismatch) is fixed with no change of design; re-hashed in `run.log`.
