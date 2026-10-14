# Path-entropy test (recorders) — pre-registration

Written 2026-09-28 before any of this code ran. Same data and split (60 train / 47 test colonies).

Conjecture (corrected form): distinguishable lineages cannot outgrow the entropy written along lineages. In the
bound's form, log D_g ≈ min(g·ln 2, H_path(g)), with D_g the number of distinct lineage signatures at generation g
and H_path(g) the joint entropy of the signature written along a lineage root→g, at the reader's resolution.

## Resolution
Two signatures are the same if they differ at <= 1 site (misread ε = 3.5% makes single-site differences unreliable).
D_g = number of clusters under single-linkage at Hamming distance <= 1 over the signatures of a colony's
generation-g lineages (clade signatures as in PREREG4), summed over test colonies.

## Diagnostic (train only, before predictions)
Parent→child correlation of placed events per branch (tolerant placement as in PREREG5): Spearman ρ and the
ratio of joint to marginal-sum entropy of (parent count, child count). Reported; if ρ <= 0.05 the corrected test
has no leverage over the per-branch form and this is stated.

## Estimating H_path(g) on train, at the resolution above
For each generation g and train colony, each generation-g lineage's signature (10 sites, 3 states); the joint
entropy H_path(g) is estimated over all train lineages at g by Miller–Madow on the cluster labels (single-linkage,
Hamming <= 1) after pooling lineages across colonies with their signatures aligned by site. Lineage counts at
each g are recorded; g with < 40 train lineages are not used.

## Prediction and rules (test colonies)
- Predicted log D_g^pred = log N_g − max(0, log N_g − H_path(g)) i.e. D_g^pred = min(N_g, e^{H_path(g)}) applied
  colony by colony with N the colony's lineage count, then summed. Observed D_g from test signatures.
- P1 (collision curve): |log D_g^obs − log D_g^pred| <= 0.15 in every generation with >= 50 test lineages.
- P2 (regime): the first generation where H_path(g) < g·ln 2 (from train) is the first generation where the test
  collision fraction 1 − D_g/N_g exceeds 0.2, ±1 generation.
- Baseline: the same rules with H replaced by the marginal sum of per-branch entropies (PREREG5's W accumulated
  along the path). Path entropy is supported if P1 passes and the baseline fails P1; partial if P1 passes for
  both; refuted if P1 fails for path entropy.

## Result (2026-09-28)
Diagnostic (train): parent→child Spearman ρ = −0.117 (691 pairs), joint/marginal entropy 0.993 → "no leverage" as
registered; the negative sign is consistent with site exhaustion (irreversible edits consume sites), not heritable
quiet. Test: H_path(g) at resolution = 2.01/1.84/1.36/1.45/2.19 nats (g = 1..5), below g·ln2 from g = 2; predicted
crossover g = 3, observed first collision fraction > 0.2 at g = 2 → P2 PASS. D_obs vs D_path (log-error):
g1 −0.21, g2 −0.31, g3 +0.14, g4 −0.02, g5 −0.77 → P1 FAIL (tolerance 0.15). Marginal baseline predicts zero
collisions at every generation (log-error −0.21 to −1.13) → fails. Verdict as registered: REFUTED.
Reading: two regimes. Deep collisions (g 3–4) are predicted by packing entropy at the reader's resolution; shallow
collisions (g 1–2, 19–31%) are write-limited (the writer is nearly off before frame 60), which a static
per-generation entropy cannot see; g5 is sparse (108 lineages). This is the bound's own structure, c (write rate)
limiting early and h_pack limiting late, but the combined prediction was not registered and is post hoc.
