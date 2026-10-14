/-
  The balloon at the level of capacities
  ======================================

  `Balloon.lean` separates the block and relational rungs for ONE source, the
  binary tree. This module lifts the separation to a family: over sources whose
  own metric is uniformly locally finite — bounded balls in `d_S`, the standard
  meaning of "uniformly locally finite metric space" — no lawful quasi-isometric
  coding into the balloon has positive growth, at any radial rate `c` and any
  resolution `ε`. The binary tree is such a source and is block-codable at
  `log 2`, so the two rate sets differ over the whole family.

  Two notions of ULF. `Source.ULF` (Constrained.lean) bounds the census ratio
  `|σ(R+1)| ≤ K |σ(R)|`: a clock condition. `Source.MetricULF` (here) bounds
  the cardinality of `d_S`-balls uniformly over the census. The balloon's own
  star source is clock-ULF with `K = 2` and is not metric-ULF (a hub's `2^i`
  leaves lie in one `d_S`-ball of radius 2); that is exactly the gap in which
  the capacity-level question of the September note lived.

  Mechanism, unchanged from `Balloon.lean`: two addresses in the same star are
  at host distance ≤ 2, so the lower relational bound confines their histories
  to one `d_S`-ball of radius `D (2 + K)`; a radial budget `r(R)` meets only
  `⌊r(R)⌋ + 1` stars; so the census is at most linear in `R` times a constant,
  and no positive exponential growth survives. Only the LOWER side of the
  relational sandwich is used.
-/
import ActiveGeometry.Balloon

namespace Challenges.BalloonCapacity

open Filter
open scoped ENNReal NNReal Topology
open ActiveGeometry.Constrained
open ActiveGeometry.Constrained.Balloon

variable {S : Type*} [PseudoMetricSpace S]

/-! ### Metric uniform local finiteness of a source -/

/-- Bounded balls in the source metric, uniformly over the census: a bound
    `f t` on the number of census histories within source distance `t` of any
    census history, at every depth. -/
def Source.MetricULF (σ : Source S) : Prop :=
  ∃ f : ℕ → ℕ, ∀ R, ∀ u ∈ σ.census R, ∀ t : ℕ,
    ((σ.census R).filter (fun v => dist u v ≤ (t : ℝ))).card ≤ f t

def metricUlfSources : Set (Source S) := {σ | Source.MetricULF σ}

/-! ### The counting step -/

/-- Under a lawful relational code into the balloon, the depth-`R` census has
    at most `f t₀ · (⌊r(R)⌋₊ + 1)` histories, with `t₀ = ⌈D (2 + K)⌉₊`. -/
theorem census_card_le_of_relational {σ : Source S} {f : ℕ → ℕ}
    (hf : ∀ R, ∀ u ∈ σ.census R, ∀ t : ℕ,
      ((σ.census R).filter (fun v => dist u v ≤ (t : ℝ))).card ≤ f t)
    (q : Distortion) {κ : Code S Balloon} {ε : ℝ≥0}
    (hb : Base (hub 0) ε σ κ) (hrel : Relational q σ κ) (R : ℕ)
    (hρ : 0 ≤ κ.radius R) :
    (σ.census R).card ≤
      f ⌈q.multiplicative * (2 + q.additive)⌉₊ * (⌊κ.radius R⌋₊ + 1) := by
  sorry

/-! ### No positive relational rate -/

/-- **Metric-ULF sources have no positive relational rate in the balloon**, at
    any radial rate and any resolution. -/
theorem metricULF_not_relational_pos (q : Distortion) {σ : Source S}
    (hσ : Source.MetricULF σ) {β : ℝ} (hβ : 0 < β) (hg : σ.HasGrowth β)
    (ε : ℝ≥0) (c : ℝ) :
    ¬ Represents (hub 0) ε (Relational q) σ c := by
  sorry

/-- Over metric-ULF sources, the balloon's relational rate set lies in `{0}`,
    for every lawful distortion, resolution and radial rate. -/
theorem balloon_rates_relational_subset (q : Distortion) (ε : ℝ≥0) (c : ℝ) :
    Rates (hub 0) ε (metricUlfSources : Set (Source S)) (Relational q) c ⊆ {0} := by
  sorry

/-- Scalar form: the balloon's relational capacity over metric-ULF sources is
    at most zero. -/
theorem balloon_capacity_relational_le_zero (q : Distortion) (ε : ℝ≥0) (c : ℝ) :
    capacity (hub 0) ε (metricUlfSources : Set (Source S)) (Relational q) c ≤ 0 := by
  sorry

/-! ### The binary tree is metric-ULF -/

theorem take_eq_of_le_lcp : ∀ (p : ℕ) (u v : List Bool), p ≤ lcp u v → u.take p = v.take p := by
  sorry

/-- A ball of radius `t` in the generation-`R` binary tree has at most `2^t`
    vertices: its members share a prefix of length `R − t`. -/
theorem card_ball_le_of_wordsOfLength {R t : ℕ} {u : List Bool}
    (hu : u ∈ wordsOfLength R) :
    ((wordsOfLength R).filter (fun v => dist u v ≤ (t : ℝ))).card ≤ 2 ^ t := by
  sorry

theorem binaryTreeSource_metricULF : Source.MetricULF binaryTreeSource := by
  sorry

theorem binaryTreeSource_mem_metricUlf :
    binaryTreeSource ∈ (metricUlfSources : Set (Source (List Bool))) := by
  sorry

/-! ### Separation at the level of the family -/

/-- **Capacity-level separation over metric-ULF sources.** The balloon's block
    rate set over the family contains `log 2`; its relational rate set does not
    (it lies in `{0}`), for every lawful distortion. -/
theorem balloon_capacity_separation (q : Distortion) :
    Real.log 2 ∈ Rates (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra 1 ∧
    Real.log 2 ∉ Rates (hub 0) 1 (metricUlfSources : Set (Source (List Bool)))
      (Relational q) 1 := by
  sorry

/-- The two rate sets differ over the metric-ULF family (`Separates`). -/
theorem balloon_separates_metricUlf (q : Distortion) :
    Separates (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra
      (Relational q) 1 := by
  sorry

end Challenges.BalloonCapacity
