# Atlas round 2 — robust experiments (pre-registration)

Written 2026-09-26 before any round-2 code ran. Roles: base map v1.0 is the ruler (transparent, frozen reader);
the v10.9 encoder is the specimen (a learned reader to be characterised). Round-1 verdicts stand as scored.

## E-D: kernels within one family (nature, trait layer)

- Families: GTDB r220 families with >= 300 catalogue genomes on the bac120 tree (one genome per leaf).
- Split inside each family: genera to train/test by md5("E-D:" + genus) parity. Families need >= 100 train genomes
  and >= 4 test genera with genomes.
- Kernel per family: variogram Γ_f(τ) from train-genus pairs (same genus and same family, up to 20,000 each), τ bins
  geomspace(0.003, 1.5, 19) with >= 150 pairs; Σ_f = covariance of the family's train genomes. Prediction by the
  full-matrix Gaussian tree model with the bivariate-normal accuracy formula (validated in round 1 to within 0.005).
- Quartets from test genera only: type G (two genera, two genomes each) and type F4 (four genera, one genome each),
  up to 300 of each per family. Baseline: the round-1 pooled kernel applied to the same quartets. (The pooled kernel
  saw some of these families' pairs, which favours the baseline.)
- D-a calibration, pooled over families, t bins with >= 150 quartets: PASS if every bin |obs − pred| <= 0.05 and
  mean |error| <= 0.03; PARTIAL if mean |error| <= 0.05; FAIL otherwise.
- D-b across families, families with >= 50 F4 quartets: PASS if Spearman(predicted, observed family accuracy) >= 0.6
  and the family-kernel mean |error| across families is <= 0.75 × the pooled-kernel mean |error|.
- Reported, not gated: per-family excess kurtosis; per-family τ_half (τ where tr Γ_f / tr Σ_f = 0.5).

## E-B′: re-enact round 1 in silico on the real tree

- Trait: isotropic 135-d OU on the GTDB r220 bac120 tree, stationary variance 1 per axis, started at stationarity.
  α from the round-1 pooled variogram: e^(−α τ½) = 0.5 where tr Γ/tr Σ = 0.5. Nugget per leaf =
  max(0, tr Γ(τ_min)/tr Σ − (1 − e^(−α τ_min))).
- Homogeneous run: all branches rate 1. Heterogeneous run: every branch below a family's MRCA has its rate multiplied
  by m_f, log m_f ~ Normal(0, s²), with s = SD of log τ_half across the E-D families (measured before this run).
- Pipeline identical to round 1: same order split, same pair sampling, same saved test quartets, full-matrix
  predictions, observed accuracy of the Euclidean reader, same t bins.
- Homogeneous: PASS if every bin |obs − pred| <= 0.03 (validates the method end to end).
- Heterogeneous: "heterogeneity sufficient" if the largest overprediction among bins with t in [0.1, 0.4] is
  >= 0.05 while the shallowest and deepest bins stay within 0.03; "insufficient" if it is < 0.03; else "partial".

## E-A: homologous windows (real genomes, record layer)

- Pairs: genomes on the bac120 tree with local FASTA on biosphereatlas, within families, stratified by marker τ into
  8 bins over 0.005–0.5 (about 40 pairs each), preferring assemblies with <= 200 contigs.
- Alignment: minimap2 (mappy, preset asm20); primary hits >= 5 kb. Homologous windows: 5 kb segments of genome 1
  along each hit and their CIGAR-mapped counterparts in genome 2 (reverse-complemented for reverse hits). Window
  divergence d: JC-corrected mismatch fraction over aligned columns; windows with gap fraction > 5% dropped.
- Deviation of a window: 4-mer counts standardised against its own genome's whole-genome 4-mer frequencies,
  (n − E)/√E. This removes the genome's composition, i.e. the trait layer. Order decomposition: π-orthonormal tensor
  transform (site basis from the pair's mean base frequencies); coefficients grouped by pattern order j = 1..4.
- Control: each genome-1 window paired with a random genome-2 window that is not its homolog.
- Corr_j in window-d bins [0, .02, .05, .1, .15, .2, .3]: Σ a1·a2 / sqrt(Σ a1² Σ a2²) over order-j coefficients.
- A1 control: PASS if non-homologous |Corr_j| <= 0.02 for every j and bin.
- A2 ordering: PASS if in every bin with >= 200 window pairs Corr_1 > Corr_2 > Corr_3 > Corr_4, and every Corr_j
  falls with d (Spearman <= −0.8 across bins).
- A3 order law (clock-free): slope s_j of log Corr_j on log Corr_1 across bins with Corr_4 > 0.02; PASS if s_j / j
  lies in [0.7, 1.15] for j = 2, 3, 4. (Independent site rates give s_j = j exactly.)
- Reported: plateau of Corr_j at the largest d (functionally maintained regional composition); aligned fraction.

## E-C: encoder spectroscopy

Conditions, predictions and rules will be appended here after reading the encoder's loading code and before any
encoder output is computed.

## Amendment A — 2026-09-26 13:27, after a two-pair smoke test, before the full E-A run

The smoke test (pairs 60 and 200 of expA_pairs.json) showed: (1) non-homologous order-1 correlation of 0.09-0.27,
because aligned (core) windows share an offset from each genome's whole-genome composition; (2) order-1 correlation
above the neutral value (0.98 vs 0.92 at d ≈ 0.06) while order 4 matched it (0.716 vs 0.726), consistent with
functionally maintained regional composition inflating low orders. A1-A3 are still scored exactly as registered.
Added, and scored alongside:
- A1' control after centring: each genome's window deviations are centred on their mean over that pair's analysed
  windows. PASS if non-homologous |Corr_j| <= 0.02 for every j and bin.
- A4 native-unit decay (record part): with d from the alignment, fit −ln Corr_j = k_j d + b_j over bins with
  d <= 0.15 (centred deviations). To first order in d the record part gives k_j = 4j/3 regardless of site-rate
  heterogeneity; maintained regional composition lowers k_j most at low order. PASS if k_4 and k_3 lie within ±25%
  of 16/3 and 4; reported for all j, with the implied maintained share.

## E-C: encoder spectroscopy — registered 2026-09-26 13:30, before any encoder output

- Genomes: 30 GTDB genera with two local, <= 200-contig genomes each (60 genomes). For each genome, W = a 20 kb
  all-ACGT window from its largest contig. Encoder: v10.9 exactly as served (v9_best.pt + v10_9_encoder.pt overlay,
  BPE 4096, ntok 4096), run on CPU in a separate process. The base map recipe reads the same sequences (control).
- Conditions per genome, each a 20 kb sequence: C_self (another real window of the same genome, >= 100 kb away);
  C_sib (a window of its genus-mate); C_rc (reverse complement of W); C_M(m), m = 0, 1, 2, 3, 5, 7 (an order-m Markov
  chain fitted on the whole genome: same genome-wide (m+1)-mer statistics, no shared sequence); C_B(b),
  b = 10, 100, 1000, 5000 (W cut into b-bp blocks and shuffled: same DNA, order destroyed beyond b).
- Displacement D(cond) = cosine distance to W (encoder) or Euclidean distance to W (base map); medians over genomes.
- Effective word length m* = smallest m with D(C_M(m)) <= D(C_self). Scope: D(C_B(b)) / D(C_self).
- Verdict for the encoder, with the base map as the positive control (expected: m* <= 3, D(C_B(b >= 10)) ≈ 0,
  D(C_rc) = 0):
  - COMPOSITION READER if m* <= 3 and D(C_B(100)) <= 0.25 D(C_self);
  - BEYOND COMPOSITION if m* >= 5 or D(C_B(1000)) >= 0.5 D(C_self);
  - INTERMEDIATE otherwise.
- Stated consequence: a composition reader cannot beat the optimal composition reader at genealogy (consistent with
  0.920 vs 0.951); a beyond-composition reader has channels composition lacks, and the next test is whether they
  carry genealogical signal.
- Also reported: D(C_self)/D(C_sib) (trait vs genome identity) and D(C_rc)/D(C_self) (strand).

## E-B″ — 2026-09-26 13:33, post hoc mechanism check, rule registered before running

Found after E-B′: single families change along ~14 effective channels (participation ratio, median 13.6), pooled
families along 56, with nearly unrelated directions (top-10 subspace overlap 0.13; random 0.07). Mechanism check:
simulate OU on the real tree where branches inside each family use that family's own random subspace (exponential
spectrum with participation ratio ~14, random orientation) and branches above families are isotropic; run the round-1
pooled pipeline over 4 realizations. "Clade-specific channels sufficient" if the mean overprediction in the
t 0.105-0.41 bins is >= 0.05 (vs ~0 for isotropic and rate-only heterogeneity).
