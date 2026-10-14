# PREREG20 — the closure test of the audit (registered 2026-10-09, ≈01:58 CEST — before the disclosed smoke test of
# 02:02:56 and the registered run of 02:05:14 in run_recorder_main.log; the clock time first written in this header,
# 02:20, was mis-stated and is corrected to the logs — before any stage count, factor or η was computed on any medium)

## What this decides
The audit identity η = availability · writing · retention · collisions · reading proves nothing by itself. Its
content is that each factor can be estimated from its own mechanism, and that the product then matches the directly
measured efficiency; if it does not, the residual names a further loss. This registration (i) defines one operational
η, once, for every medium; (ii) runs the closure on the medium where every stage is simulable against ground truth
(the intMEMOIR recorder, imaged trees); (iii) reports the same decomposition on the bacterial Atlas, where the
A-curve prediction already closes within 0.15 in bacteria and misses in archaea, so that the Atlas residual is
located at a stage rather than left as a number.

## One operational η (all media)
At depth τ (recorder: generation g; Atlas: the genus or family depth on the reference tree),

    η(τ) = log₂ D_read(τ) / log₂ M(ε, r(τ)),

D_read(τ) = the number of depth-τ lineages the reader distinguishes at resolution ε (the ε-packing number of their
read images in the reader's metric); M(ε, r) = the ε-packing number of the medium's ball of radius r in that metric;
r(τ) = the distance a lineage has travelled by depth τ (the mean displacement of the read images from the root
state). This is Paper I's β/(c·h_pack·ρ) with both rates integrated to depth τ: the bits of lineage identity read,
over the bits the medium can hold at the distance the process has gone. It is a number in [0, 1] for every medium.
- Recorder (ε = 0): D_read = distinct strict-consensus signatures among depth-g lineages (PREREG4's statistic);
  r = mean edited sites per signature; M(0, r) = Σ_{k ≤ r} C(10, k)·2^k (tape states with at most r edited sites;
  log-linear interpolation between integers). At ε = 1 (reported): D by greedy packing of signatures at Hamming
  distance > 1; M divided by 3 (the single-parity bound for distance 2).
- Atlas (recipe metric, 136 dimensions): D_read = AC1's greedy ε-packing of a genus's genomes (ε ∈ EPS); r = RMS
  distance of the genus's genomes from the family centroid; M(ε, r) = the ε-packing number of the Euclidean ball of
  radius r in 136 dimensions, computed by the same greedy packing on uniform draws (so reader and room use one
  instrument).
- Genome sequence (analytic, reported): D_read = tips distinguishable = N(τ) for any L above the identity price;
  M = the Hamming ball of radius L·p(τ) in 4^L, log₂ M ≈ L·[H₂(p) + p·log₂ 3]; at L = 3·10⁶ and p = 0.1 the room is
  1.9·10⁶ bits, so for 10²–10⁵ lineages η is of order 10⁻⁶–10⁻⁵. (Correction 02:28 CEST, 9 Oct: the first draft of
  this line said "order 10⁻⁸", which does not follow from the formula beside it; the efficiency table's 10⁻⁸ was the
  25 Sep rate estimate, and the one operational η gives 10⁻⁶–10⁻⁵. Reported, not scored.)
- Natural CRISPR arrays and the hippocampal code: the same definition with depth = array age and track distance
  respectively; not computed here (their rows keep their provenance notes).

## Recorder arm — the registered closure
Data: 107 intMEMOIR colonies with imaged trees (closure/intmemoir, re-fetched 9 Oct; analysed in place, not
redistributed); the PREREG4 split (60 train / 47 test by md5("E-R:" + name)); generations gated at ≥ 50 test
lineages, as RM1. Disclosed: the aggregate statistics D_obs(g) at ε = 0, 1, 2 and the recorded fractions were seen on
both splits in PREREG4/9; the stage counts, the factors, the sixth-loss size and η are new.

Stage counts, all per colony and averaged over test colonies (D̄ = Σ_c D_c / n_c, the R2/RM1 convention), each from
its own estimator, train only where estimated:
0. Room: M(0, r̄(g)) from the observed r̄(g). Availability = 1 at ε = 0 by construction: every tape state inside the
   ball is reachable (10 independent integrase cassettes, each 0 → {1, 2}).
1. Demand: N̄(g), from the imaged trees.
2. Written, independent writer, infinite sites: D̄_2∞(g) — the PREREG4 writer (hazards κ_s·λ(t), q_s, p0_s fitted on
   train leaf likelihoods) simulated on the true test trees with every edit event labelled uniquely, so two
   lineages collide only by inheritance. Writer-speed factor = log D̄_2∞ / log N̄; the writing factor of the Lean chain
   is log D̄_2∞ / log M (demand × writer speed).
3. Kept: = written. Retention = 1 by the chemistry (excision and inversion are terminal in intMEMOIR); the parsimony
   placement's count of edited → unedited steps is reported as the check.
4. Distinct, finite sites: D̄_2(g) — the same simulation with the ten real sites (homoplasy on the hot sites).
   Collision factor = log D̄_2 / log D̄_2∞; its independent basis is the site-usage distribution (κ_s, q_s) alone.
5. Read: D̄_5(g) — stage-4 leaves passed through the readout mixture (π, ε_clean, ε_noisy fitted on short train
   cherries, PREREG9's amendment of 28 Sep). Reading factor = log D̄_5 / log D̄_2.
Five-factor prediction: D̄_5(g). Direct measurement: D̄_obs(g) (observed distinct signatures on the test colonies).
The sixth loss, named in advance — correlated writing: the empirical writer with branch-level donors and colony
activity classes (R-mix's build_writer, internal donors, train only), which carries the observed clumping of edits
on branches (variance/mean 1.98 against 1.18 for independent sites) and the heritable quiet of sub-lineages.
2′. D̄_2′(g): that writer, finite sites, no readout. Correlation factor = log D̄_2′ / log D̄_2.
5′. D̄_5′(g): 2′ through the readout mixture. Six-factor prediction.

Rules (err_k(g) = log(D̄_k(g) / D̄_obs(g)), gated g):
- CL1 five-factor closure: PASS if |err_5(g)| ≤ 0.15 at every gated g. Prediction: FAIL, with err_5 > +0.15 at g ≥ 3
  (the independent writer over-predicts distinctness, PREREG4's R2).
- CL2 six-factor closure: PASS if |err_5′(g)| ≤ 0.15 at every gated g. Prediction: PASS. Disclosed: this is RM1 at
  ε = 0 for the readout-mixture writer, seen on both splits (main −0.03/0.00/+0.04/+0.02/−0.10; swap −0.002/+0.09/
  +0.05/+0.003/−0.05); it is restated as the closure, not as a new verdict.
- CL3 the residual is a loss at the writing stage: the correlation factor's log is negative at every gated g ≥ 2,
  and |err_5′(g)| < |err_5(g)| at every gated g ≥ 3.
- CL4 ordering at the deepest gated generation: |log writer-speed| ≥ |log correlation| ≥ |log reading| ≥
  |log collision|. Prediction stated now: writing is the largest loss, then correlation, then reading; collisions
  are small (ten sites, two edited states, fifteen-fold site heterogeneity).
- CL5 reported: η(g) at ε = 0 and 1 for g = 1…5; every stage count with its simulation SD (400 replicates, seed
  20000 + g); the demand/room ratio log N̄ / log M separately from writer speed; the swap split (writer re-estimated
  on the 47) as replication.
Verdict: CLOSURE LOCATED if CL1 fails as predicted, CL2 passes, CL3 holds (the audit closes once the named sixth
loss is included, and the residual sits where predicted); CLOSED if CL1 passes (five factors suffice); NOT CLOSED
if CL2 fails; PARTIAL otherwise. CL4 is scored separately as the ordering claim.

## Atlas arm — reported decomposition (no verdict; A-curve's verdict stands)
Frozen family images from A-curve (bacteria, 36 families; archaea as in A-arch), the E-D full-matrix process and the
k2 joint draw, unchanged. Per family and ε ∈ EPS, the chain of mean per-genus packing numbers:
room M(ε, r) (uniform ball) → available (the ellipsoid of the family covariance Σ_f, same radius) → written (joint
draw with the linear kernel Γ′(0)·τ, no saturation) → kept (the fitted saturating Γ_f(τ): A-curve's prediction
itself) → read (ε; the ratio to the ε → 0 count, which is the genome count). Collisions between genera are not in
AC1 and are reported as 1. The residual err(ε) = log(Σ_obs / Σ_kept) is A-curve's known log error; its growth with
ε (bacteria −0.04 → −0.12, archaea −0.05 → −0.18) is reported against the stage factors so that the sixth loss on
the Atlas (compaction beyond the Gaussian image, the deep collision remainder of PREREG11–13) is located relative to
retention and reading. η(τ) per family at ε = 0.79 (K2's ε) and 1.25 is reported.

## Amendment to the Atlas arm — 2026-10-09 02:08 CEST (closure_atlas.py modified 02:08:19; the full run launched
## 02:11:12 per closure_atlas_bac.log; the time first written here, 03:05, was mis-stated), after a disclosed smoke
## test on one family (two genera, 02:05:18), before the full run
The "written" stage's unsaturated kernel was specified as the family's first variogram bin extended linearly,
Γ_lin(τ) = (τ/c₀)·Γ(c₀). In the smoke test that gave Σ_lin < Σ_fam (the shallowest bin is convex: near-clonal pairs
change composition slower than their patristic distance), which would make retention > 1. The unsaturated rate is
now the maximal secant over the family's bins, Γ_lin(τ) = τ·Γ(c_k*)/c_k* with k* = argmax_k tr Γ(c_k)/c_k, the
fastest linear growth any bin shows; k* and c_k* are recorded per genus. The room is analytic (d·log₂(r/ε), the
volume-ratio convention) because a greedy packing cannot count a 135-dimensional ball; the registration's "same
instrument" clause is withdrawn for the room and kept for the observed, written and kept counts. The Atlas arm
remains reported, not scored.

## Frozen files (sha256 in closure/run.log at launch)
closure_recorder.py (this registration's recorder script), rec_test.py and rmix.py from
~/Documents/addressability-recorders-2026-09-26 (unchanged; imported), rec_fit.json (PREREG4 fit), the 107
true_tree.nwk and characters.txt files (manifest hash). Atlas: acurve.py, k2_packing.py, exp_D_family.py,
atlas_predict2.py (unchanged), the Atlas inputs by CHECKSUMS.sha256.

## Caveats stated in advance
The closure's independence is of estimators, not of data: the writer is fitted on train leaves, the readout mixture
on train cherries, the correlated writer on train event placements, and the closure is scored on test lineages.
Stage 2′ is a simulation switch, not a parameter, so the six-factor chain has nothing fitted to D̄_obs. Any further
residual after the sixth loss is reported as such and not named.
