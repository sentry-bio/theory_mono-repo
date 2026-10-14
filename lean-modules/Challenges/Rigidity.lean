/-
  Rigidity of the equality case
  =============================

  A codebook that is an `ε`-net of a region `A` of the host, and that preserves
  the source metric to lawful distortion `(D, K)` (`Constrained.Relational`),
  makes `A` quasi-isometric to the source: every point of `A` is within `ε` of
  a codeword, and codeword distances track source distances. Concretely, for
  `a b ∈ A` with nearest codewords `s t`,

      D⁻¹ · dist s t − K − 2ε  ≤  dist a b  ≤  D · dist s t + K + 2ε.

  Read with the source a tree: a lineage whose image fills its room at the
  reader's resolution, with bounded relational tax, forces the room to carry
  the tree's geometry at that resolution. The Gromov-hyperbolicity corollary
  (quasi-isometry invariance of hyperbolicity for geodesic spaces) is not in
  Mathlib and is cited, not proved, in the manuscript.

  The net hypothesis is where saturation enters: `maximal_separated_isNet`
  shows a codebook that is maximal among `ε`-separated subsets of `A` is an
  `ε`-net of `A`. Maximality is exactly "no further address fits", the finite
  form of attaining the packing number (`Packing.exists_optimal_blockCode`).

  STATUS. LEAN-CHECKED once built. Elementary; no new hypotheses beyond the
  kernel's `Relational` obligation and an explicit net.
-/

import ActiveGeometry.Constrained

namespace ActiveGeometry.Rigidity

open ActiveGeometry.Constrained
open scoped NNReal ENNReal

variable {M : Type*} [MetricSpace M] {S : Type*}

/-- `C` is an `ε`-net of `A`: every point of `A` lies within `ε` of `C`. -/
def IsNet (ε : ℝ) (C A : Set M) : Prop :=
  ∀ a ∈ A, ∃ c ∈ C, dist a c ≤ ε

/-- A real gap `ε < dist u v` is an extended gap `ε < edist u v`. -/
theorem edist_gt_of_dist_gt {ε : ℝ≥0} {u v : M} (h : (ε : ℝ) < dist u v) :
    (ε : ℝ≥0∞) < edist u v := by
  sorry

/-- Maximal `ε`-separated subsets are `ε`-nets: if some point of `A` were
    farther than `ε` from every codeword, it could be added without breaking
    separation. Separation is Mathlib's `Metric.IsSeparated` (`ε < edist`
    pairwise). -/
theorem maximal_separated_isNet {ε : ℝ≥0} {C A : Set M}
    (hsep : Metric.IsSeparated ε C)
    (hmax : ∀ a ∈ A, a ∉ C → ¬ Metric.IsSeparated ε (insert a C)) :
    IsNet (ε : ℝ) C A := by
  sorry

/-- The two-sided estimate behind the quasi-isometry: a point within `ε` of a
    codeword and another within `ε` of a second codeword are at a distance
    within `2ε` of the codeword distance. -/
theorem dist_within_two_eps {ε : ℝ} {a b c d : M}
    (hac : dist a c ≤ ε) (hbd : dist b d ≤ ε) :
    dist c d - 2 * ε ≤ dist a b ∧ dist a b ≤ dist c d + 2 * ε := by
  sorry

/-- **Rigidity.** If the depth-`R` codebook of `(σ, κ)` is an `ε`-net of `A` and
    the code is relational with distortion `q`, then every two points of `A`
    have source histories whose source distance controls their host distance,
    with the additive constant inflated by `2ε`. -/
theorem quasiIsometric_of_net [PseudoMetricSpace S]
    (σ : Source S) (κ : Code S M) (q : Distortion)
    (hrel : Relational q σ κ) (R : ℕ) {ε : ℝ} {A : Set M}
    (hnet : IsNet ε (book σ κ R) A) :
    ∀ a ∈ A, ∀ b ∈ A, ∃ s ∈ σ.census R, ∃ t ∈ σ.census R,
      dist a (κ.addr R s) ≤ ε ∧ dist b (κ.addr R t) ≤ ε ∧
      q.multiplicative⁻¹ * dist s t - q.additive - 2 * ε ≤ dist a b ∧
      dist a b ≤ q.multiplicative * dist s t + q.additive + 2 * ε := by
  sorry

/-- Every codeword is its own nearest codeword: the correspondence of
    `quasiIsometric_of_net` is onto the census. -/
theorem codeword_self_net (σ : Source S) (κ : Code S M) (R : ℕ) {ε : ℝ} (hε : 0 ≤ ε) :
    ∀ s ∈ σ.census R, ∃ c ∈ book σ κ R, dist (κ.addr R s) c ≤ ε := by
  sorry

end ActiveGeometry.Rigidity
