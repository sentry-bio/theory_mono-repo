# Evolution as Active Geometry, v4 — the experiments and mathematics sections, first full draft (2026-10-09)

Written against v3.5's structure ("Descent Occupies the Room; Genomes Encode It"). Every number below traces to a
registration in the worktree's RESULTS files or to the registered record in the Heredity-as-Memory doc. All twenty-one
registrations are scored. Author edits expected
throughout; the aim is that nothing here needs re-measuring. (Both pending results landed at 03:00 CEST on 9 October
and are filled in below; no [pending] marks remain.)

---

## §2 Descent occupies the room — rewritten

The governing figure keeps its two axes, growth class and tree defect, and its silent third coordinate: whether what
is plotted is the room or the tape. What changes is where the certified evidence sits.

The functional representation first. KEGG ortholog profiles over 1,935 genomes (the stratified sample, at most 120
genomes per phylum across 52 phyla, drawn from the 29,303-genome panel) give a four-point defect ratio of 0.32
against a dimension-matched Euclidean null — reproduced exactly (0.323) on the same sample on 9 October. That remains
a classifier-level fact: the functional arrangement is markedly more tree-like than a flat cloud of the same data.
The growth-class gate, pointed at this metric as v3.5 promised (PREREG18), returned the other verdict: from 25
centres, 21 read polynomial and 1 exponential, while the matched Gaussian null read polynomial from 24 — CERTIFIED
POLYNOMIAL on v3.5's own sample, INDETERMINATE on a random sample of the same size (18 polynomial, 5 exponential).
Ball occupancy in the pathway metric grows as a power of the radius, exponent 2–4. v3.5's kill line fired, and we
state the consequence plainly: the functional metric is hyperbolic at classifier strength and polynomial in growth,
so it cannot carry the Layer-I claim.

The Layer-I claim moves to the medium where it was certified: sequence. [Insert the base-map certification: the
Atlas base map v1.0 (186,527 genomes) and its taxon-edge certification of 28 September, with the certified growth
number.] A pathway profile is a reader's image of a genome — 868 coordinates, L1-normalised — and a coarse reader can
return a polynomial image of an exponential room. That is the audit's reading factor at work (§4), in the same
direction as the wedge (§3): composition-level readers lose genealogy first. We offer it as a reading, not a rescue;
the gate's verdict stands.

The governing figure's upper-left cell is therefore occupied by sequence, with the functional metric annotated as
"hyperbolic by four-point, polynomial by growth". Nothing about which exponential host, and nothing about
saturation, follows.

## §3 Identity is cheap; genealogy is expensive — the measured price law

v3.5 showed the two exits on ground truth. v4 adds the price law that sits under them, measured with nothing
fitted, and the control v3.5 asked for.

### The line
For a lineage branching at rate β on a four-letter tape forgetting at substitution rate ρ (ρ = 4μ/3 under
Jukes–Cantor), the Kesten–Stigum line 2ρ = β separates two regimes (Paper I's Window module proves the rate form;
exactness is the named hypothesis). Above the line the root of a clade is reconstructible from its leaves and the
sites a census reader needs to recover a split level off with the number of lineages; on the line they grow
polylogarithmically; below it they grow as a power of the number of lineages. PREREG15 (8 October) measured all three
on the synthetic harness and every prediction fell within 3% of the measured value with no parameter fitted. PREREG15b
found the other half of the line numerically for four letters on binary trees: below it, the optimal reader forgets
the root; above it, it reconstructs (registered verdict not reached only because one two-letter control cell stayed
indeterminate under an over-tight stability rule; the four-letter cells were unambiguous).

### The wedge: one tape, two prices
On the same tape, identity costs about log n sites and gets cheaper as substitution rises, while genealogy's cost
opens as a power of n below the line. PREREG16 (8 October) measured the ratio of the two prices across substitution
rates: within 7% of the closed-form prediction at every rate. This is the ladder seen as a number: block capacity
robust, relational capacity fragile, and the line as the hinge between them.

### What composition is worth
A reader that sees only letter or k-mer counts, not aligned sites, is worth a bounded number of sites. PREREG16's
closed form (reader modes j with lines x_j = 1, 1.41, 1.59, 1.68; the one-site worth of letter counts below the line)
predicted the 4-mer reader's worth at every rate, depth and genome length on new seeds (PREREG17, 9 October): 24 of
24 cells within 3 SE, decaying with depth toward the letter-count value, which is PREREG15's Var_site/P within 20% in
every cell. The registration's verdict was NOT PREDICTED because a secondary length-ratio rule, mis-sized against the
cells' sampling error, missed at the three smallest cells; the level, decay and limit all held. Composition is worth
1.0–1.3 aligned sites below the line and about 2 at 1.5× the line, falling toward one site with depth. This is the
price of reading composition instead of sequence, and it is why §2's functional metric cannot carry depth.

### The two exits, and the control v3.5 asked for
Poverty and mixing keep their v3.5 signatures (decided accuracy rising with alignment length versus flooring; the
misplaced block resolving to the donor's tree at 98.7%). Test B (PREREG19, 9 October) ran the wrong-model control:
gamma-distributed rates and a skewed base composition, with no transfer, recover at both depths (accuracy 0.97–1.00 by
800,000 sites). Heterotachy — two site classes four times faster inside two clades — gave a near-floor at the
shallower depth: 0.911 → 0.927 over a sixteen-fold range of sites, faster than Test C's floors (< 0.005), slower
than Test A's recoveries (≥ 0.04). The registered verdict is INCONCLUSIVE: a floor alone does not identify a second
history, because long-branch attraction can produce one.

What does identify it is block structure. A transferred segment sits in whole windows of the alignment; a wrong model
biases every site alike. For each quartet decided wrongly at full length, the per-site margin between the true and
the chosen split, summed over twenty windows, has an across-window variance whose null value under exchangeable sites
is exact (hypergeometric). PREREG19b (9 October): under mixing, 100% and 94% of wrong quartets exceed the null's 95th
percentile at the two depths (median variance ratio 880 and 208); under heterotachy, 4.5% and 6.4% (ratio 0.94 and
0.97 — the null itself). The window-vote statistic v3.5 proposed (fraction of windows agreeing with the majority) is
withdrawn: it measures a quartet's decision margin, not block structure, and reads 0.57 for heterotachy against 0.61
for mixing. The diagnostic for real data is two-part: a floor in the recovery curve, and block structure of the wrong
quartets against the site-permutation null, with the window length set from the expected segment length.

### The reading
Unchanged in substance from v3.5, with one sentence added: the price of genealogy changes class at the line, and
the line is where the tape's forgetting rate meets the lineage's branching rate.

## §4 The audit — new section (replaces "The encoding respects its alphabet", whose entropy-rate measurement moves
## here as the writing factor's ceiling)

Every real medium sits inside the envelope, and the audit says where. Paper I splits efficiency into availability and
utilization; the five-ratio form refines it:

η = (C_rel/C_block) · (β_written/C_rel) · (β_kept/β_written) · (β_distinct/β_kept) · (β_read/β_distinct),

each factor at most one under the lossy assumption (Lean: AuditFactors.efficiency_eq_product, factors_le_one). The
identity proves nothing by itself. Its content is the closure test: estimate each factor from its own mechanism,
multiply, and compare with the directly measured η; a residual names a further loss.

### One operational η
η(τ) = log₂ D_read(τ) / log₂ M(ε, r(τ)): the bits of lineage identity a reader distinguishes at depth τ, over the bits
the medium can hold at the distance the lineages have travelled by then. D_read is the ε-packing number of the read
lineage images; M the ε-packing number of the medium's ball of radius r(τ); r the mean displacement from the root
state. It is Paper I's β/(c·h_pack·ρ) with both rates integrated to depth τ, and it is a number in [0, 1] for every
medium (PREREG20 §One operational η).

### The closure test on the recorder (PREREG20, 9 October)
intMEMOIR: ten integrase sites, three states, irreversible edits, 107 colonies with imaged trees; the PREREG4
train/test split. Five stages, each from its own estimator on train data only: the room (analytic from the mean
number of edited sites), the independent-site writer fitted on train leaves (with every edit event labelled, so
collisions can be separated from inheritance), the finite-site tape, and the readout mixture fitted on short train
cherries. The five-factor chain over-predicts distinct lineages by a margin that grows with depth (+9% to +31% at
generations 1–5): FAIL, as predicted in advance. The sixth loss named in advance — correlated writing: edits clumped
on branches and heritable quiet in sub-lineages, carried by the empirical donor writer with colony activity classes —
closes the chain: |log error| ≤ 0.035 at generations 1–4 and 0.11 at generation 5 on the test colonies, and
≤ 0.09 on the swap split with the writer re-fitted on the other half. Verdict on both splits: CLOSURE LOCATED.

Two findings sit beside the verdict. Collisions on a ten-site, two-state tape are negligible (factor 0.98–1.03).
And the reader does not lose bits here; it fabricates them. The readout mixture (13.6% of cells read with 27%
per-site error) raises the distinct count by 3–16%: a noisy cell creates spurious fixed edits in small clades, so
lineages that share a tape are read as different. The audit's lossy assumption fails at the reading stage for a noisy
reader, and a closure test that only allowed losses would have mis-attributed the surplus to writing. The ordering of
losses at the deepest generation — writer speed, then correlated writing, then reading, then collisions — held on the
replication and narrowly failed on the main split (reading 0.150 against correlation 0.137 in log magnitude, eleven
colonies).

The recorder's η rises from 0.12 at generation 1 to 0.20 at generation 4; it is three-quarters of what the demand
asks (η/occupancy 0.78–0.89), in a room the lineages occupy to a quarter (about four edited sites of ten).

### The efficiency table, with one η
| Medium | η | Losses that bind | Provenance |
|---|---|---|---|
| Engineered recorder (intMEMOIR) | 0.12–0.20 by generation | writing, correlated writing, room; the readout adds spurious distinctness | PREREG20, measured on 47 and 60 held-out colonies |
| Genome sequence | 10⁻⁶–10⁻⁵ (10²–10⁵ lineages) | room unused; erasure and reading bind | analytic on the one η: D_read = N(τ), log₂ M ≈ L[H₂(p) + p log₂ 3] = 1.9·10⁶ bits at L = 3·10⁶, p = 0.1; the 25 Sep rate estimate gave 10⁻⁸ |
| Genome composition (Atlas) | 0.008–0.02 at genus depth | availability (half the family ellipsoid's axes thinner than ε: 0.62 → 0.46 in bacteria, 0.35 → 0.31 in archaea); then compaction beyond the Gaussian image, growing with ε (0.94 bacteria, 0.92 archaea at ε = 2); retention ≈ 1 at genus depth | PREREG20 Atlas arm: the audit chain on A-curve's confirmed family images, 262 bacterial and 35 archaeal genera |
| Natural CRISPR arrays | horizons 10–100× shorter than capacity allows | erasure | PREREG10, 56 species (not yet on the common η) |
| Hippocampal place code | ≈ 0.38 at the Fisher-optimal 0.41 | a reader-optimal interior | 25 Sep estimate; the bridge test was refuted (PREREG14) |

The entropy-rate measurement of v3.5 §4 (1.84/1.76/2.17 bits for fungi/archaea/bacteria against the two-bit
ceiling) is the writing factor's ceiling for the sequence medium and moves into this table's second row.

## The horizon section — theorem, instrument, contrast (new; replaces v3.5 §5.1)

**Theorem (rate form; Lean Window).** With b = e^{βτ} lineages per edge and λ = e^{−ρτ} the channel's second
eigenvalue, b·λ² > 1 ⇔ β > 2ρ. Above the line the signal e^{(β−2ρ)t} diverges; below it, it vanishes. Identity costs
O(log N) sites (N·p^L ≤ δ once L ≥ log(N/δ)/(−log p)). Exactness of the line — reconstruction possible exactly above it
— is a hypothesis: classical for two letters, claimed for three and four in October 2026 (family 229, supercritical
half formalized), found numerically for four letters on binary trees here (PREREG15b).

**Instrument.** The census reader of PREREG15: the number of sites a clade census needs to recover a split, as a
function of the number of lineages, measured at rates below, on and above the line. Three growth classes, each within
3% of prediction.

**Contrast.** Composition. Its room is bounded (a stationary cloud), its forgetting is the trait's mean reversion,
and its own line is β = 2θ with θ the mean-reversion rate. A pairwise reader pays a cost exponential in depth on either
side; an ancestor-aware reader (clade centroids) keeps a signal above it. Measured (PREREG21, 9 October): at the
deepest split among the test genera of each of 36 bacterial families, the pairwise reader recovers the split at
0.733 and the ancestor-aware reader at 0.897, both predicted from the frozen family kernels with nothing fitted
(0.726 and 0.892; median per-family errors 0.09 and 0.04); the ancestor-aware reader wins in 32 of 36 families, the
four exceptions at a ceiling. Every family sits far above its composition line (β − 2θ = +6 to +16: branching
9–23 against mean reversion 1–4), so the trait's window does not bind at family depth on the Atlas; what binds is
the pairwise reader's exponential cost, which averaging a clade's leaves halves. Verdict HORIZON READ in bacteria.
In archaea (9 families) the family image under-predicts both readers (the pairwise reader already at 0.92–1.00 in six
families) and the replication fails, in the same direction as A-arch: the archaeal image is too diffuse. The
ancestor-aware reader is the Atlas's next reader.

## §6 What stays open — revised list
1. No natural medium measured saturates: η ≤ 0.2 on the recorder, ≈ 0.38 in the hippocampus, 10⁻⁶–10⁻⁵ on sequence.
   Saturation is a design regime (Paper I, Remark on four rigidities). Open question 2 of v3.5 is answered in the
   negative for every medium measured.
2. Direction and the operating point are open: whether the room a lineage uses is isotropic, and where inside the
   envelope natural media settle, remain unmeasured (PREREG11–13 closed the Atlas derivation of the genus-rate rung).
3. The polytomy retrospective (soft versus hard polytomies by the two-part diagnostic) decides whether the horizon
   predicts rather than describes.
4. The matched-capacity host comparison (hyperbolic versus other exponential hosts) stays unrun and is not
   load-bearing.

## §8 Instrument certifications — additions
The growth-class gate re-certified 13 of 13 on the machine that ran PREREG18 before touching a genome; its refusal
rule never triggered (every centre had 39–40 radii and an occupancy span above 30). The Test A/C instrument (256-tip
Yule tree, seed 42; 3,000 quartets, seed 7; JC-corrected four-point with saturated pairs excluded) ran Test B and
PREREG19b unchanged, with a disclosed smoke test on a 32-tip tree before any registered cell. The block-structure
statistic's null is exact: under heterotachy 4–6% of wrong quartets exceed the 95th percentile, the nominal rate. The
recorder closure's simulators reproduce PREREG4's and PREREG9's statistics on the seen aggregates before any new
quantity is read.

## Appendix: the registered record (one line each; the full ledger is the repository's registrations directory)
PREREG (25 Sep) Atlas round 1 — D3 failed, D4 partial. PREREG2 (26 Sep) Atlas round 2 — clade subspaces sufficient;
window rules failed; the encoder reads composition. PREREG3 synthetic harness — H1, H2, H4–H6 passed. PREREG4 recorder
law — R1, R2 failed; R3 passed. PREREG5/6 fusion and path entropy — refuted. PREREG7 tree-aware writer — supported.
PREREG8 packing law — passed at ε = 1 only. PREREG9 (28 Sep) confirmation suite — Atlas bacteria confirmed, archaea
failed, recorder readout model failed out of sample. PREREG10 CRISPR arrays — erasure-limited. PREREG11–13 (30 Sep)
genus-rate rung — not derived; partial in archaea; the Atlas derivation closed. PREREG14 (4 Oct) hippocampal bridge —
refuted; the fine-resolution sign law held in 18 of 19 tracks. PREREG15 (8 Oct) harness horizon — sequence arm within
3%; composition arm failed as registered. PREREG15b four-letter tightness — on the line for four letters; verdict
not reached on a control cell. PREREG16 the wedge — identity–genealogy rules within 7%; composition-level rules
failed on level and were explained exactly post hoc. PREREG17 (9 Oct) composition's worth — NOT PREDICTED on the
length band; level, decay and limit held. PREREG18 growth-class gate — CERTIFIED POLYNOMIAL. PREREG19 Test B —
INCONCLUSIVE; PREREG19b block discriminator — WORKS. PREREG20 closure — recorder CLOSURE LOCATED on both splits;
Atlas arm reported (η ≈ 0.01; availability binds; retention one at genus depth; the residual is compaction beyond
the image, larger in archaea). PREREG21 composition's horizon — HORIZON READ in bacteria; FAIL in archaea.

---

# The mathematics section (for both manuscripts' reference; Paper I's Lean inventory paragraph is in
# paper1/PAPER_I_ADDITIONS.tex)

One object, three statements, each with its status.

**I. The envelope.** β ≤ C_𝒜 ≤ C_block = c·h_pack, in every proper metric space, with no curvature, tree or
stationarity hypothesis (Paper I; Lean Packing.convergent_rate_addressability_limit,
Constrained.structured_addressability_limit). Equality is rigid four ways (Remark on four rigidities; Lean Rigidity
for the net statement). The room has five classical names; the bound uses only the one that exists everywhere.

**II. The window.** Random writing keeps genealogy only inside 2ρ < β < λ₀. The erasure side is the Kesten–Stigum line,
proved in rate form (Lean Window.kestenStigum_iff_rate) with exactness a named hypothesis
(Window.ReconstructionThreshold, in the shape of openai/math family 229's Reconstructs); the collision side is
hyperbolic branching Brownian motion, with the quarter-envelope constant (n−1)²/8 our derivation; readers shrink the
window (edit-distance distortion, family 099). Measured: the three growth classes of the price of genealogy (PREREG15),
four-letter tightness (PREREG15b), the wedge (PREREG16), composition's worth (PREREG17).

**III. The audit.** η = availability · writing · retention · collisions · reading, an identity with bounds (Lean
AuditFactors), given content by the closure test: on the recorder it closes once a sixth loss, correlated writing, is
included, and the reader fabricates distinctness (PREREG20). One operational η is defined for every medium.

Named hypotheses, never derived: Manning (topological entropy = volume entropy), Gromov's invariance, exactness of the
Kesten–Stigum line for q ≥ 3, the isotropy assumption A3. Named conjecture: one theorem covering both sides of the
window.
