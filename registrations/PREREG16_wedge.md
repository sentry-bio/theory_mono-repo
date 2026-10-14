# PREREG16 — one tape, two prices: the wedge (registered 2026-10-08, before any registered simulation ran)

## The sharpest version of the claim
On one tape written by one substitution process, the price of **identity** (every lineage distinguishable) and
the price of **genealogy** (the branching order recoverable) are different functions of the same rate, and the
Kesten–Stigum line x = 2λ² = 1 is where they part in class:

1. **Identity costs O(log n) sites on both sides of the line, and gets cheaper as substitution rises.** Writing
   is what makes addresses.
2. **Genealogy costs O(1) sites per deep split above the line, polylog on it, and n^{2·log₂(1/x)} below.** Writing
   is also what erases relations. (Measured in PREREG15; cited, not rerun.)
3. **So the wedge — genealogy price over identity price — is bounded above the line and opens as a power of n
   below it.** At 4,096 lineages the predicted identity price is 15 sites at x = 0.6 and 52 at x = 1.5; genealogy
   is ~6 × 10⁶ and ~150. The same rate moves them in opposite directions.
4. **The reader tax is a cap on effective tape.** A composition reader keeps identity (every leaf's composition
   is distinct) but is worth a bounded number of aligned sites however long the genome: letter counts are worth
   exactly **one** site (Gaussian pairing makes the off-diagonal L² variance equal one site's variance), and
   standardized 4-mers a handful (their higher-order modes decay as λ^j per edge and die first). This is
   Paper I's balloon realised by a reader: addresses intact, relations at one site's worth.

Nothing here is a new theorem. (1) is a birthday bound; (2) is Kesten–Stigum / Mossel–Peres for linear readers;
(4) is a second-moment identity. The claim is the *conjunction measured on one instrument*, which is what
EAG v4's "identity is cheap; genealogy is expensive" needs in place of the qualitative v3.5 statement.

## Design (same process and tree as PREREG15)
JC69, uniform iid root; deep quartet ((A,B),(C,D)) of complete binary clades of height h, every edge length t,
x = 2λ², λ = e^{−4t/3}.

**Arm I — identity price.** h = 2…10, x ∈ {0.6, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5}; 200 replicate trees of 160 sites;
per replicate the smallest site prefix at which all 4·2^h leaves are pairwise distinct (binary search; distinctness
is monotone in prefix length); L_id = 95th percentile. Prediction (wedge_predictions.json): Poisson approximation
over all leaf pairs by path length, Σ_pairs (1/4 + 3/4·λ^d)^L ≤ −ln 0.95.

| x | L_id, h = 2 … 10 | L_id(10)/L_id(6) | genealogy L*(10)/L*(6) (PREREG15 pred.) | Λ = ratio of ratios |
|---|---|---|---|---|
| 0.6 | 8 9 9 10 11 12 13 14 15 | 1.36 | 61.7 | 45.2 |
| 0.8 | 9 10 11 12 14 15 16 17 18 | 1.29 | 7.54 | 5.87 |
| 0.9 | 10 11 13 14 15 17 18 19 20 | 1.33 | 3.71 | 2.79 |
| 1.0 | 11 13 14 16 17 19 20 22 23 | 1.35 | 2.25 | 1.66 |
| 1.1 | 13 15 16 18 20 21 23 25 26 | 1.30 | 1.62 | 1.24 |
| 1.25 | 16 18 20 22 24 26 28 30 33 | 1.38 | 1.23 | 0.90 |
| 1.5 | 25 28 32 35 38 42 45 48 52 | 1.37 | 1.05 | 0.77 |

**Arm C — composition as effective sites.** x ∈ {0.8, 1.0, 1.5}; h ∈ {1, 2, 4}; L ∈ {5,000, 40,000}; 1,500 replicate
trees per cell, all readers on the same trees. Per cell: per-site census margin sd (pooled over all sites, exact
mean from PREREG15's closed form) → per-site SNR r; letter-count reader margin M₁ (census of per-leaf letter counts);
standardized 4-mer reader margin M₄ (PREREG3's R2 std4). Effective sites:
- L_eff,1 = (L · sd_site / sd(M₁))² (the exact mean of M₁ is L·E[M], so only the sd is estimated);
- L_eff,4 = (z₄ / r)², z₄ = mean(M₄)/sd(M₄) across replicates.
These cells are placed where composition is inside or near its horizon (PREREG15's arm-C design flaw).

## Rules
- W1a identity closed form: L_id within max(2 sites, 15%) of the table in ≥ 90% of the 63 cells.
- W1b identity grows as log n at every x: L_id(10)/L_id(6) ≤ 1.6 for all seven x, *including below the line*.
- W1c identity is cheaper below the line: L_id(x = 0.6) ≤ L_id(x = 1.5) at every h.
- W3 the wedge: Λ(x) = [L*_gen(10)/L*_gen(6)] / [L_id(10)/L_id(6)], with L*_gen the PREREG15 measurements and L_id
  arm I's: Λ ≤ 1.3 at x = 1.25 and 1.5; Λ ∈ [1.2, 2.6] at x = 1.0; Λ ≥ 4 at x = 0.8; Λ ≥ 25 at x = 0.6.
- W4 letter counts are worth one site: L_eff,1 ∈ [0.75, 1.33] in ≥ 90% of the 18 cells, at both L.
- W5 4-mers are worth a bounded number of sites, independent of genome length. Power gate (fixes PREREG15's flaw):
  a cell is eligible only if r ≥ 0.05 and z₄ ≥ 4/√R. Requires ≥ 4 eligible cells; every eligible L_eff,4 ∈ [2/3, 24];
  and for (x, h) eligible at both L, L_eff,4(40k)/L_eff,4(5k) ∈ [0.6, 1.6] in all such pairs (one miss allowed if > 3
  pairs). Under the same rule the aligned reader's effective sites are L itself — an 8× step.
- W6 (reported) composition keeps identity: fraction of replicates with all leaves' 4-mer vectors distinct.
- Verdict: WEDGE SHOWN if W1a, W1b, W1c, W3, W4, W5 all hold; otherwise WEDGE NOT SHOWN, with the failing rule named.

## What a pass licenses in EAG v4
§3's "identity is cheap; genealogy is expensive" becomes a measured price law with the KS line as its hinge, and
the Atlas paragraph says what composition is worth in sites. It does **not** license any claim about real
genomes, about non-linear readers (BP/ML, family 229's tightness), or about trees other than balanced ones.

## Frozen files (sha256)
- wedge_theory.py 2b34ad5249c5e86fa988a96b5ce4b22d7b70f6d5753024b3595821021e058417
- wedge_sim.py e53d88041a7d02d1225cb32789d4af2cb6e801d95281dfa58f1fb2254fd1a1ca
- wedge_score.py 691f8d4f4ea49aff0d55e8f31971145ab8b3e2b04e81be0e5da06ab3c2b16d23
- wedge_predictions.json 07839bb89778d94b2a570d2d30a86b864a1ec7027dbe9eac69f882be93d100f1
- ../addressability-horizon-2026-10-08/horizon_score.json b91553b9b9cb03d145a206f8ac83e277604f381bce0f4daa69b03e4ec5cd10ce

## Disclosed before registration
Written with PREREG15's results in hand, including its 18 composition cells (z_comp 0.01–0.49 at h = 2–6), which
suggested the one-site reading; the prediction in (4) was derived afterwards from the second-moment identity and is
tested here on new seeds and new cells. Timing smoke test on seed 3 (h = 4, L = 40k; one h = 10 distinctness call);
no statistic inspected.

## Caveats stated in advance
- L_gen is a per-split price (one deep quartet) and L_id an all-leaves price; full-tree genealogy carries an extra
  log n union factor. W3 compares growth classes, not levels, and that factor would strengthen, not weaken, it.
- The one-site identity for letter counts is exact only under Gaussian pairing; at h = 1 (two leaves per clade) the
  census is far from Gaussian, which is the likeliest W4 miss and will be reported as such.

## Result as registered — 2026-10-08: WEDGE NOT SHOWN (W4, W5 fail; W1a–c and W3 pass)
- W1a 63/63 identity cells within tolerance. W1b L_id(10)/L_id(6) = 1.35–1.46 at every x. W1c holds at every h.
  At 4,096 leaves: identity 16 sites (x = 0.6) … 50 (x = 1.5).
- W3 Λ = 42.5 (0.6; pred 45.2), 5.25 (0.8; 5.87), 2.72 (0.9; 2.79), 1.63 (1.0; 1.66), 1.20 (1.1; 1.24),
  0.93 (1.25; 0.90), 0.78 (1.5; 0.77). The wedge between identity and genealogy behaves exactly as predicted.
- W4 FAIL (10/18 in [0.75, 1.33]): letter counts are worth 1.03–1.38 sites at x ≤ 1.0 but 1.7–2.4 at x = 1.5.
  Reading: the "exactly one site" identity assumed Gaussian pairing; with short edges the single-site census is
  near-discrete (most leaves share the clade root's letter), its variance exceeds the pairing term, and the reader is
  worth Var_site/σ²_pair > 1 sites. Right in kind (bounded, L-independent, → ~1 with depth), wrong in level where the
  census is non-Gaussian — the caveat named h = 1; the miss is wider (x = 1.5 at every h).
- W5 FAIL on range only: 12 eligible cells; length-independence holds in 6/6 pairs (40k/5k ratios 0.89–1.21); but
  x = 1.5, h = 1 is worth 33–37 sites, above the registered cap of 24. 4-mers are worth ~35 → 21 → 9.4 sites as h goes
  1 → 2 → 4 at x = 1.5, and ~3 → 0.8 at x = 1.0: higher-order modes die with depth, as stated; the cap was a guess.
- W6 composition kept identity in every replicate of every cell (fraction 1.0).
Not re-scored. A follow-up registration may state the composition claim as "bounded and length-independent, decaying
toward the letter-count value with depth", with the letter-count level predicted from the measured site kurtosis.

## Post-hoc analysis — 2026-10-08 (after scoring; the verdict above is unchanged)
Files: posthoc_closed_form.py/.json, posthoc_gaussianity_P15.json, posthoc_lcheck.py/.json. Zero fitted parameters.
1. Verdict scoping. The registered verdict conjoined two claims under one name. The identity–genealogy wedge rules
   (W1a–c, W3) all passed; the composition-level rules (W4, W5) failed. Cite as such; future registrations get one
   verdict per claim. Evidential weight: W3's genealogy half was PREREG15's (known at registration); the new evidence
   in W3 is W1, a birthday bound. The wedge is known mathematics shown combining as the frame says on one instrument.
2. W4 explained exactly. Var(M₁) = L·Var_site + L(L−1)·P holds identically for iid sites, P = the Isserlis (Gaussian)
   value, closed form from second moments. So L_eff,1 = Var_site/P, which is 1 only for a Gaussian single-site census.
   Predicted vs measured in all 18 cells within sampling error (e.g. 2.26 vs 2.38/1.97; 1.13 vs 1.26/1.05). The 5k/40k
   gap is noise: rerun of (x 1.5, h 1) with 10,000 replicates, new seeds: 2.31 ± 0.05 (5k), 2.26 ± 0.05 (40k), predicted
   2.26; M₁ excess kurtosis ≈ 2.3 inflates the R = 1,500 variance SE to ~±0.12.
3. The W4 miss is the horizon. Var_site/P across PREREG15's 63 cells → 1.00 below the line (x = 0.6: 1.001 at h = 10),
   decays slowly at x = 1 (1.041), and plateaus above it (x = 1.25: ~1.22; x = 1.5: ~1.62). This is the census CLT
   below Kesten–Stigum vs a root-dependent non-Gaussian limit above it (Janson–Mossel): above the line the census still
   remembers the root, and that memory is why letter counts are worth more than one site there.
4. W5 explained. The 4-mer covariance is exact: 4^-8[∏_aligned(1 + λ^d K) − 1] per window offset, expanding into modes j
   (j aligned positions) with eigenvalue λ^j per edge, each with its own line 2(x/2)^j = 1 → x_j = 1, 1.41, 1.59, 1.68.
   Predicted z₄ matches measured within ~2.3 SE in all 18 cells; predicted worth at (1.5, 1) = 37.2 sites (measured
   36.9/32.9) — the registered cap of 24 was a guess where the closed form was available. 94% of that cell's signal is
   in modes j ≥ 2. For the unweighted standardized reader, the j = 1 mode grows fastest and dominates with depth, so the
   reader's worth falls toward the letter-count value at every x (projection, Gaussian-site units, x = 1.5: 16.5 at
   h = 1 → 1.74 at h = 10). Bounded and length-independent throughout. No composition cell reached z = 2 (max 1.33).
