# PREREG15 — the genealogy horizon in the harness (registered 2026-10-08, before any registered simulation ran)

## Claim
Evolution as Active Geometry v4 will claim two lines and the wedge between them: an envelope for addresses
(Paper I's β ≤ c·h_pack) and a horizon for genealogy, which for a four-state symmetric substitution process
on a branching lineage sits at the Kesten–Stigum line x = 2λ² = 1, λ = e^{−4t/3}. The claim this test can
move is precise and narrower than "relations are lost below the line": **the horizon is where the price of
genealogy changes class.** Above it, the sequence needed to resolve deep relationships is bounded in tree
size; at it, it grows polylogarithmically; below it, it grows as a power of the number of lineages.
And a composition reader has a horizon of its own that **no amount of sequence moves**, while the
sequence reader's horizon recedes as the tape lengthens. That second contrast is the wedge the paper needs.

## What kind of test this is (stated before the result)
Arm S is a **calibration of a known theorem in our own instrument**, not a discovery: the census (linear)
reader's threshold at x = 1 is Kesten–Stigum (1966) / Mossel–Peres (2003). If S fails, the harness is wrong,
not the theorem. Arm C extends PREREG3's H3 (composition horizons flat in length, quartets) to deep trees
with a census, and is the part only this frame predicts as a *contrast* with S. Neither arm tests whether
better-than-linear readers (belief propagation, ML) share the threshold — that is family 229's four-state
claim, and finite h ≤ 10 cannot settle it; it is deliberately out.

## Design
- Process: JC69 (uniform root, every site independent); each edge keeps its letter with prob λ, else redraws
  uniformly. Every edge has length t; x = 2λ².
- Tree: four complete binary clades A, B, C, D of height h (2^h leaves each, n = 4·2^h), joined as ((A,B),(C,D)),
  every joining edge of length t (internal edge split at its midpoint, half on each side). Topology known.
- Reader (both arms' sequence reader): clade census s = per-letter counts among the clade's leaves − 2^h/4;
  per-site margin M = s_A·s_B + s_C·s_D − s_A·s_C − s_B·s_D; correct topology iff ΣM > 0.
- Composition reader (arm C): each leaf's overlapping 4-mer counts, centred at (L−3)/256 and scaled by its
  square root (R2 std4 of PREREG3, non-canonical); clade census = sum over leaves; same margin with dot
  products in R^256.

## Arm S — sequence census across the line
- x ∈ {0.6, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5}; h ∈ {2, …, 10} (n = 16 … 4096 leaves).
- 200,000 sites per (x, h) for h ≤ 8; 100,000 for h = 9, 10. Seeds fixed in horizon_sim.py.
- E[M] is exact: 2·(3/4)·4^h·λ^{2h+2}·(1−λ). Sites are independent, so the margin over L sites has
  mean/sd = r√L with r = E[M]/sd(M); L* = 4/r² is the number of sites needed for mean/sd = 2.
  sd(M) is estimated; E[M] is taken from the closed form (checked by K1), because below the line E[M]/sd is
  too small to estimate directly at h = 10 within any feasible budget.
- Leading-order prediction (horizon_predictions.json): L* ∝ (S_h/x^h)², S_h = 1 + ½Σ_{j≤h} x^j.

| x | t | L*(10)/L*(6) | L*(10)/L*(7) | slope of log₂L* on h, h = 6–10 |
|---|---|---|---|---|
| 0.6 | 0.452 | 61.7 | 21.8 | 1.486 |
| 0.8 | 0.344 | 7.54 | 4.44 | 0.728 |
| 0.9 | 0.299 | 3.72 | 2.60 | 0.473 |
| 1.0 | 0.260 | 2.25 | 1.78 | 0.292 |
| 1.1 | 0.224 | 1.62 | 1.39 | 0.173 |
| 1.25 | 0.176 | 1.23 | 1.15 | 0.075 |
| 1.5 | 0.108 | 1.05 | 1.03 | 0.017 |

### Rules (arm S)
- K1 mean calibration: |mean_emp − E[M]| ≤ 3 SE in ≥ 90% of the 63 cells.
- K2 supercritical, bounded: L*(10)/L*(7) ≤ 1.5 for x = 1.25 and 1.5.
- K3 subcritical, power law in n: OLS slope of log₂L* on h over h = 6–10 within ±25% of the table for
  x = 0.6 and 0.8 (slope s means L* ∝ n^s).
- K4 critical, polylog: L*(10)/L*(6) ∈ [1.5, 3.4] at x = 1.0.
- K5 (reported) ordering: Spearman of L*(10)/L*(6) against x ≤ −0.9.
- Verdict: HORIZON REPRODUCED if K1–K4 hold; otherwise NOT REPRODUCED, and the harness is repaired before
  any claim in EAG v4 cites it.

## Arm C — the reader's horizon does not recede with tape
- h ∈ {2, 4, 6}; x ∈ {0.8, 1.0, 1.25}; L ∈ {20,000, 160,000}; 150 independent replicate trees per cell, both
  readers on the same replicates. z = mean/sd of the total margin across replicates.
- C1 length does not rescue composition: z_comp(160k)/z_comp(20k) ∈ [0.75, 1.33] in ≥ 7 of 9 (h, x) cells,
  while the sequence census on the same trees rises by √8 = 2.83 (ratio within [0.75, 1.33] × 2.83) in ≥ 7 of 9.
- C2 reader tax: z_comp < z_seq at L = 160,000 in all 9 cells.
- C3 (reported, no verdict): z_comp(h = 6)/z_comp(h = 2) at each x. Expectation, stated not scored: the
  composition census inherits the same x = 1 line through its slowest (single-letter) mode, so this ratio
  should be smallest at x = 0.8.
- Verdict: WEDGE SHOWN if C1 and C2 hold; else WEDGE NOT SHOWN.

## Ceiling map, stated now
Both verdicts positive → the horizon section of EAG v4 is written as "theorem + instrument + contrast", and
the open-question list keeps only family 229's tightness. S positive, C negative → the horizon section stands
but the composition-reader paragraph is rewritten from the data. S negative → no horizon claim is made
from the harness.

## Frozen files (sha256)
- horizon_theory.py 67b0d0ea58516b8bf1d97de8265727cd96eb9e6df281ebb15191d2daee789434
- horizon_sim.py beb9bd4029b6d296a40d3970ffc112c3a11bee186f42d8fc48ff8f1d485bc566
- horizon_score.py 65ac2d2ae7d3bb3e5314ab8fe5603cb7700b5252c584ce9ca069e323defb8b5a
- horizon_predictions.json 9cf2d491a0c904a3d518ab868ba0ca30d2b85724a13689410429d3bedfa93a4d

## Disclosed before registration
A smoke test on a throwaway seed (7), not the registered seeds: runtime at h = 2 and 10; one mean check at
x = 1.0, h = 2 over 100,000 sites (0.842 ± 0.020 vs closed form 0.879, 1.8 SE); 4-mer reader and h = 6
simulation timing at L = 160,000. No margin sd, no L*, no composition z was looked at.

## Caveats stated in advance
- K2–K4 tolerances rest on a leading-order variance (inter-clade correlation neglected); it is h-independent
  asymptotically, so it should shift levels more than ratios, but a K2/K4 miss of under 20% beyond tolerance
  will be reported as "prediction constant, not class" and examined, not re-scored.
- JC on an iid uniform root is the theory's exact domain; real genomes (rate heterogeneity, composition
  drift, indels) move the line, which is the next registration, not this one.
- Complete balanced trees with equal edges are the cleanest case; Yule trees are a follow-up.

## Result as registered — 2026-10-08: arm S HORIZON REPRODUCED; arm C WEDGE NOT SHOWN
Arm S (all rules pass): K1 mean calibration 62/63 cells within 3 SE. K2 L*(10)/L*(7) = 1.16 (x = 1.25), 1.03 (x = 1.5).
K3 slopes 1.487 (x = 0.6; predicted 1.486) and 0.735 (x = 0.8; predicted 0.728). K4 L*(10)/L*(6) = 2.30 at x = 1
(predicted 2.25). K5 Spearman −1.0. L* at h = 10 (4,096 leaves): 153 sites at x = 1.5, 2,070 at x = 1, 6.0 × 10⁶ at
x = 0.6, against 104 / 210 / 1,210 at h = 2. The leading-order variance predicted the ratios to within 3% everywhere.
Arm C: C2 holds (z_comp < z_seq in 9/9 cells; z_seq 11–69 at 160 kb against z_comp ≤ 0.49). C1 FAILS (2/9 composition
cells in band; sequence 9/9 in the √8 band, 2.6–3.1×). Reading, verdict first: composition sat at z ≈ 0 (fraction
correct 0.40–0.69) in every cell, i.e. beyond its horizon everywhere — every design point has total depth ≥ (h+1)t ≥ 0.5,
past PREREG3's ~0.2 composition quartet horizon, which was knowable at design time and was flagged after the first cell
was seen, before scoring. C1's ratios are therefore ratios of noise and test nothing about length; C3 likewise. What arm C
does show is that the composition census resolves no deep quartet at depths where 100–2,000 sites of sequence suffice.
The L-independence contrast at depth needs a redesign with composition inside its horizon (t ≈ 0.02–0.08, x near 2,
where the line itself is out of reach) — a separate registration, not a re-score.

## Record note — 2026-10-09: this file was overwritten and restored on 2026-10-08; its content is unchanged
At 12:59:44Z on 2026-10-08, a parallel session (transcript a73dbe6e…, which ran PREREG15b) picked the same dated folder name
and wrote its own registration to this path, replacing this file. At 12:59:54Z it also put a script, horizon_A.py, here.
At 13:00:42Z it restored this file from this session's original Write (12:55:23Z; 6,704 bytes, sha256 d42e94c68df928f5…)
and moved horizon_A.py to ~/Documents/addressability-theory-2026-10-08/horizon-A/. That session's message reporting this
was held and never delivered. This note is written from both transcripts and from the following check, made on 2026-10-09:
- The first 6,704 bytes of this file are byte-identical to the original Write. Everything after them was appended by this
  session: the result section at 13:12:19Z, after the restore, and this note.
- All four frozen hashes above still match.
- That session wrote nothing else into this folder; its other commands here were listings and reads.
- No registered result depends on the 58 seconds the file was wrong. horizon_sim.py and horizon_score.py never read this
  file, and this session neither read nor edited it between 12:55:23Z and 13:12:19Z.
