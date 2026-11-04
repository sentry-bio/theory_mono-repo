/-
  The coarse packing converse
  ===========================

  Block capacity sees packing entropy at the reader's scale `ε`. Relational
  capacity over metric-ULF sources (bounded `d_S`-balls) sees it at EVERY
  scale: for each `ε' > 0`,

      β ≤ c · h_pack(M, o; ε').

  Proof. Under a lawful relational code, histories whose addresses lie within
  `2ε'` of each other have source distance at most `D (2ε' + K)`, so at most
  `f(⌈D(2ε'+K)⌉)` of them share a cell of an `ε'`-cover; a maximal
  `ε'`-separated subset of the budget ball is such a cover and has exactly the
  ball's packing number of cells (Mathlib). Hence
  `|σ(R)| ≤ f · P(B(o, r(R)), ε')`, and the rate follows.

  Consequences. The infimum over scales of packing entropy, the coarse growth
  rate, is a quasi-isometry invariant; relational capacity is bounded by it,
  block capacity is not. The balloon packs only linearly above the diameter of
  its stars (`h_pack(B; ε') = 0` for `ε' ≥ 2`), so its relational capacity over
  metric-ULF sources vanishes — the separation of `BalloonCapacity.lean` is
  the instance of this theorem at scale `ε' > 2`. Hyperbolic space has the same
  packing entropy at every scale, which is why it CAN have zero relational tax
  (the equality itself is Skenderi's, not this theorem's).
-/
import ActiveGeometry.BalloonPacking

namespace Challenges.CoarseConverse

open Filter
open scoped ENNReal NNReal Topology
open ActiveGeometry
open ActiveGeometry.Constrained
open ActiveGeometry.Constrained.Balloon

variable {M : Type*} [MetricSpace M] {S : Type*} [PseudoMetricSpace S]

/-! ### The counting step -/

/-- Under a lawful relational code into a proper host, the depth-`R` census of
    a source with `d_S`-balls bounded by `f` has at most
    `f ⌈D (2ε' + K)⌉₊ · P(B(o, r(R)), ε')` histories, for every `ε' ≠ 0`. -/
theorem census_card_le_coarse_packing [ProperSpace M] {o : M} {σ : Source S} {f : ℕ → ℕ}
    (hf : ∀ R, ∀ u ∈ σ.census R, ∀ t : ℕ,
      ((σ.census R).filter (fun v => dist u v ≤ (t : ℝ))).card ≤ f t)
    (q : Distortion) {κ : Code S M} {ε : ℝ≥0}
    (hb : Base o ε σ κ) (hrel : Relational q σ κ)
    (ε' : ℝ≥0) (hε' : ε' ≠ 0) (R : ℕ) (hρ : 0 ≤ κ.radius R) :
    (σ.census R).card ≤
      f ⌈q.multiplicative * (2 * ε' + q.additive)⌉₊ * Packing.packingCount o ε' (κ.radius R) := by
  sorry

/-! ### The rate form -/

/-- **Coarse packing converse.** Over metric-ULF sources, a relational rate is
    bounded by `c` times the packing entropy at EVERY scale `ε' > 0`. -/
theorem coarse_packing_converse [ProperSpace M] {o : M} {ε ε' : ℝ≥0} (hε' : ε' ≠ 0) {h' : ℝ}
    (hpacking : Tendsto (Packing.packingRate o ε') atTop (𝓝 h')) (q : Distortion)
    {σ : Source S} (hσ : σ.MetricULF) {β : ℝ} (hg : σ.HasGrowth β) {c : ℝ}
    (hr : Represents o ε (Relational q) σ c) : β ≤ c * h' := by
  sorry

/-! ### The balloon above the diameter of its stars -/

/-- At any scale `ε' ≥ 2` the balloon's ball of radius `ρ` packs at most
    `⌊ρ⌋₊ + 1` points: one per star. -/
theorem balloon_packingCount_le {ε' : ℝ≥0} (hε' : 2 ≤ (ε' : ℝ)) {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount (hub 0) ε' ρ ≤ ⌊ρ⌋₊ + 1 := by
  sorry

/-- **The balloon's coarse packing entropy is zero**: at every scale `ε' ≥ 2`
    the packing rate tends to `0`. -/
theorem balloon_coarse_entropy_zero {ε' : ℝ≥0} (hε' : 2 ≤ (ε' : ℝ)) :
    Tendsto (Packing.packingRate (hub 0) ε') atTop (𝓝 0) := by
  sorry

/-! ### Bounded geometry closes the scale gap

If every `ε'`-ball packs at most `Mb` points at resolution `ε` (uniformly in
the centre: bounded geometry at the pair of scales), then the packing counts
at the two scales differ by the factor `Mb`, so the packing rates have the
same limit. The scale gap of the coarse converse is therefore a phenomenon
of hosts WITHOUT bounded geometry — the balloon's hubs of unbounded degree. -/

/-- A coarser packing is a finer packing. -/
theorem packingCount_anti [ProperSpace M] {o : M} {ε ε' : ℝ≥0} (hε : ε ≠ 0) (hε' : ε' ≠ 0)
    (hle : ε ≤ ε') {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount o ε' ρ ≤ Packing.packingCount o ε ρ := by
  sorry

/-- Under bounded geometry at scales `ε ≤ ε'`, the fine count is at most `Mb`
    times the coarse count. -/
theorem packingCount_le_mul_packingCount [ProperSpace M] {o : M} {ε ε' : ℝ≥0}
    (hε : ε ≠ 0) (hε' : ε' ≠ 0) {Mb : ℕ}
    (hMb : ∀ x : M, Metric.packingNumber ε (Metric.closedBall x ε') ≤ Mb)
    {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount o ε ρ ≤ Mb * Packing.packingCount o ε' ρ := by
  sorry

/-- **Bounded geometry closes the scale gap.** If `ε'`-balls pack boundedly
    many points at resolution `ε`, the packing rate at `ε` has the same limit
    as the packing rate at `ε'`. -/
theorem packingRate_scale_invariant [ProperSpace M] {o : M} {ε ε' : ℝ≥0}
    (hε : ε ≠ 0) (hε' : ε' ≠ 0) (hle : ε ≤ ε') {Mb : ℕ}
    (hMb : ∀ x : M, Metric.packingNumber ε (Metric.closedBall x ε') ≤ Mb)
    {h : ℝ} (hpacking : Tendsto (Packing.packingRate o ε') atTop (𝓝 h)) :
    Tendsto (Packing.packingRate o ε) atTop (𝓝 h) := by
  sorry

/-- The balloon separation as a corollary of the coarse converse: no
    metric-ULF source has a positive relational rate in `B`. -/
theorem balloon_relational_rate_nonpos (q : Distortion) {σ : Source S} (hσ : σ.MetricULF)
    {β : ℝ} (hg : σ.HasGrowth β) {ε : ℝ≥0} {c : ℝ}
    (hr : Represents (hub 0) ε (Relational q) σ c) : β ≤ 0 := by
  sorry

end Challenges.CoarseConverse
