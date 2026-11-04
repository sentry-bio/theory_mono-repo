/-
  Challenge module for `ActiveGeometry.Persistent` (the persistent rung): the same definitions and theorem
  statements, every proof replaced by `sorry`. Namespace `Challenges.Persistent`; opens `ActiveGeometry.Constrained`
  so the statements refer to the repository's `Source`, `Code`, `Stable`, `retentiveSources`, `capacity`,
  `recodingCode` and to `packingRate_scale_invariant` of `CoarseConverse`.
-/
import ActiveGeometry.Structured
import CoarseConverse

namespace Challenges.Persistent

open ActiveGeometry
open ActiveGeometry.Constrained

open Filter
open scoped ENNReal NNReal Topology

variable {M : Type*} [MetricSpace M]

/-! ### Packing numbers are monotone in the set -/

theorem packingNumber_mono_set {ε : ℝ≥0} {A B : Set M} (h : A ⊆ B) :
    Metric.packingNumber ε A ≤ Metric.packingNumber ε B := by
  sorry

theorem packingCount_mono_radius [ProperSpace M] (o : M) {ε : ℝ≥0} (hε : ε ≠ 0)
    {ρ ρ' : ℝ} (hρ : 0 ≤ ρ) (h : ρ ≤ ρ') :
    Packing.packingCount o ε ρ ≤ Packing.packingCount o ε ρ' := by
  sorry

theorem two_mul_ne_zero_of_ne_zero {ε : ℝ≥0} (hε : ε ≠ 0) : (2 * ε : ℝ≥0) ≠ 0 := by
  sorry

/-- The identity code never moves an address. -/
theorem recodingCode_stable (σ : Source M) (c : ℝ) (m : ℝ≥0) :
    Stable m σ (recodingCode c) := by
  sorry

/-! ### Extending a separated set to a covering one -/

/-- The points of `B` farther than `ε` from every point of `A`. -/
def farSet (ε : ℝ≥0) (A B : Set M) : Set M :=
  {x | x ∈ B ∧ ∀ a ∈ A, (ε : ℝ≥0∞) < edist x a}

theorem farSet_subset (ε : ℝ≥0) (A B : Set M) : farSet ε A B ⊆ B := by
  sorry

/-- Extend a separated set `A ⊆ B` to a separated subset of `B` that covers
    `B`: adjoin a maximal separated subset of the far points. -/
noncomputable def extendSeparated (ε : ℝ≥0) (A B : Set M) : Set M :=
  A ∪ Metric.maximalSeparatedSet ε (farSet ε A B)

theorem subset_extendSeparated (ε : ℝ≥0) (A B : Set M) :
    A ⊆ extendSeparated ε A B := by
  sorry

theorem extendSeparated_subset {ε : ℝ≥0} {A B : Set M} (hA : A ⊆ B) :
    extendSeparated ε A B ⊆ B := by
  sorry

theorem isSeparated_extendSeparated {ε : ℝ≥0} {A : Set M} (B : Set M)
    (hA : Metric.IsSeparated ε A) :
    Metric.IsSeparated ε (extendSeparated ε A B) := by
  sorry

theorem packingNumber_farSet_ne_top {ε : ℝ≥0} {A B : Set M}
    (hfin : Metric.packingNumber ε B ≠ ⊤) :
    Metric.packingNumber ε (farSet ε A B) ≠ ⊤ := by
  sorry

theorem extendSeparated_isCover {ε : ℝ≥0} {A B : Set M}
    (hfin : Metric.packingNumber ε B ≠ ⊤) :
    Metric.IsCover ε B (extendSeparated ε A B) := by
  sorry

theorem extendSeparated_finite {ε : ℝ≥0} {A B : Set M} (hA : A.Finite)
    (hfin : Metric.packingNumber ε B ≠ ⊤) :
    (extendSeparated ε A B).Finite := by
  sorry

/-! ### The nested family -/

/-- Nested separated covering sets at the radii `c R`. -/
noncomputable def nestedSet (o : M) (ε : ℝ≥0) (c : ℝ) : ℕ → Set M
  | 0 => extendSeparated ε ∅ (Metric.closedBall o (c * ((0 : ℕ) : ℝ)))
  | R + 1 =>
      extendSeparated ε (nestedSet o ε c R)
        (Metric.closedBall o (c * ((R + 1 : ℕ) : ℝ)))

/-- The target census size at depth `R`: the packing count at twice the
    resolution. -/
noncomputable def persistentCount (o : M) (ε : ℝ≥0) (c : ℝ) (R : ℕ) : ℕ :=
  Packing.packingCount o (2 * ε) (c * (R : ℝ))

theorem nestedSet_zero (o : M) (ε : ℝ≥0) (c : ℝ) :
    nestedSet o ε c 0 = extendSeparated ε ∅ (Metric.closedBall o (c * ((0 : ℕ) : ℝ))) := by
  sorry

theorem nestedSet_succ (o : M) (ε : ℝ≥0) (c : ℝ) (R : ℕ) :
    nestedSet o ε c (R + 1) =
      extendSeparated ε (nestedSet o ε c R)
        (Metric.closedBall o (c * ((R + 1 : ℕ) : ℝ))) := by
  sorry

section Nested

variable [ProperSpace M]
variable (o : M) {ε : ℝ≥0} (hε : ε ≠ 0) {c : ℝ} (hc : 0 ≤ c)
include hε hc

theorem ball_packingNumber_ne_top (R : ℕ) :
    Metric.packingNumber ε (Metric.closedBall o (c * (R : ℝ))) ≠ ⊤ := by
  sorry

omit [ProperSpace M] hε in
theorem nestedSet_subset_closedBall (R : ℕ) :
    nestedSet o ε c R ⊆ Metric.closedBall o (c * (R : ℝ)) := by
  sorry

omit [ProperSpace M] hε hc in
theorem nestedSet_isSeparated (R : ℕ) : Metric.IsSeparated ε (nestedSet o ε c R) := by
  sorry

theorem nestedSet_finite (R : ℕ) : (nestedSet o ε c R).Finite := by
  sorry

omit [ProperSpace M] hε hc in
theorem nestedSet_mono (R : ℕ) : nestedSet o ε c R ⊆ nestedSet o ε c (R + 1) := by
  sorry

theorem nestedSet_isCover (R : ℕ) :
    Metric.IsCover ε (Metric.closedBall o (c * (R : ℝ))) (nestedSet o ε c R) := by
  sorry

/-- The nested sets as finsets. -/
noncomputable def nestedFinset (R : ℕ) : Finset M :=
  (nestedSet_finite o hε hc R).toFinset

theorem coe_nestedFinset (R : ℕ) : (nestedFinset o hε hc R : Set M) = nestedSet o ε c R := by
  sorry

theorem nestedFinset_mono (R : ℕ) : nestedFinset o hε hc R ⊆ nestedFinset o hε hc (R + 1) := by
  sorry

/-- A covering separated set is at least as large as the packing number at
    twice the resolution. -/
theorem packingCount_two_mul_le_nestedFinset_card (R : ℕ) :
    Packing.packingCount o (2 * ε) (c * (R : ℝ)) ≤ (nestedFinset o hε hc R).card := by
  sorry

/-! ### The thinned nested census -/

theorem persistentCount_mono (R : ℕ) :
    persistentCount o ε c R ≤ persistentCount o ε c (R + 1) := by
  sorry

theorem one_le_persistentCount (R : ℕ) : 1 ≤ persistentCount o ε c R := by
  sorry

/-- A nested census of the right size inside the nested finsets. -/
abbrev PersistentCell (R : ℕ) : Type _ :=
  {s : Finset M // s ⊆ nestedFinset o hε hc R ∧ s.card = persistentCount o ε c R}

theorem persistentBase_exists :
    ∃ u : Finset M, (∅ : Finset M) ⊆ u ∧ u ⊆ nestedFinset o hε hc 0 ∧
      u.card = persistentCount o ε c 0 := by
  sorry

theorem persistentStep_exists (R : ℕ) (prev : PersistentCell o hε hc R) :
    ∃ u : Finset M, prev.1 ⊆ u ∧ u ⊆ nestedFinset o hε hc (R + 1) ∧
      u.card = persistentCount o ε c (R + 1) := by
  sorry

noncomputable def persistentStep (R : ℕ) (prev : PersistentCell o hε hc R) :
    PersistentCell o hε hc (R + 1) :=
  ⟨Classical.choose (persistentStep_exists o hε hc R prev),
    (Classical.choose_spec (persistentStep_exists o hε hc R prev)).2.1,
    (Classical.choose_spec (persistentStep_exists o hε hc R prev)).2.2⟩

theorem persistentStep_subset (R : ℕ) (prev : PersistentCell o hε hc R) :
    prev.1 ⊆ (persistentStep o hε hc R prev).1 := by
  sorry

noncomputable def persistentCell : (R : ℕ) → PersistentCell o hε hc R
  | 0 =>
      ⟨Classical.choose (persistentBase_exists o hε hc),
        (Classical.choose_spec (persistentBase_exists o hε hc)).2.1,
        (Classical.choose_spec (persistentBase_exists o hε hc)).2.2⟩
  | R + 1 => persistentStep o hε hc R (persistentCell R)

theorem persistentCell_succ (R : ℕ) :
    persistentCell o hε hc (R + 1) = persistentStep o hε hc R (persistentCell o hε hc R) := by
  sorry

theorem persistentCell_mono (R : ℕ) :
    (persistentCell o hε hc R).1 ⊆ (persistentCell o hε hc (R + 1)).1 := by
  sorry

theorem persistentCell_card (R : ℕ) :
    (persistentCell o hε hc R).1.card = persistentCount o ε c R := by
  sorry

theorem persistentCell_subset_nestedSet (R : ℕ) :
    ((persistentCell o hε hc R).1 : Set M) ⊆ nestedSet o ε c R := by
  sorry

theorem persistentCell_nonempty (R : ℕ) : (persistentCell o hε hc R).1.Nonempty := by
  sorry

/-- The persistent source: a retentive census that is a nested family of
    `ε`-separated points inside the balls of radius `c R`. -/
noncomputable def persistentSource : Source M where
  census R := (persistentCell o hε hc R).1
  census_nonempty R := persistentCell_nonempty o hε hc R

theorem persistentSource_census (R : ℕ) :
    (persistentSource o hε hc).census R = (persistentCell o hε hc R).1 := by
  sorry

theorem persistentSource_retentive : (persistentSource o hε hc).Retentive := by
  sorry

theorem persistentSource_mem_retentive :
    persistentSource o hε hc ∈ (retentiveSources : Set (Source M)) := by
  sorry

theorem persistentSource_card (R : ℕ) :
    ((persistentSource o hε hc).census R).card =
      Packing.packingCount o (2 * ε) (c * (R : ℝ)) := by
  sorry

/-! ### The identity code never moves an address -/

theorem book_persistent (R : ℕ) :
    book (persistentSource o hε hc) (recodingCode c) R =
      ((persistentCell o hε hc R).1 : Set M) := by
  sorry

theorem recodingCode_base_persistent :
    Base o ε (persistentSource o hε hc) (recodingCode c) := by
  sorry

end Nested

/-! ### Achievability and capacity at the persistent rung -/

section Capacity

variable [ProperSpace M]

theorem persistentSource_hasGrowth (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c h : ℝ} (hc : 0 < c)
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h)) :
    (persistentSource o hε.ne' hc.le).HasGrowth (c * h) := by
  sorry

theorem recodingCode_represents_persistent (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c : ℝ}
    (hc : 0 < c) (m : ℝ≥0) :
    Represents o ε (Stable m) (persistentSource o hε.ne' hc.le) c := by
  sorry

/-- **The persistent rung is achievable at the packing rate of twice the
    resolution.** Over retentive sources, with addresses that never move, the
    rate `c · h_pack(2ε)` is achieved; the only price of nesting is the
    resolution shift `ε → 2ε`. -/
theorem achievable_stable_persistent (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c h : ℝ}
    (hc : 0 < c) (m : ℝ≥0)
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h)) :
    Achievable o ε (retentiveSources : Set (Source M)) (Stable m) (c * h) c := by
  sorry

/-- Over retentive sources the persistent capacity sits between the packing
    rates at `2ε` and at `ε`:

        c · h_pack(2ε) ≤ C_persistent(ε) ≤ c · h_pack(ε). -/
theorem capacity_stable_between (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c h₁ h₂ : ℝ}
    (hc : 0 < c) (m : ℝ≥0)
    (hup : Tendsto (Packing.packingRate o ε) atTop (𝓝 h₁))
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h₂)) :
    c * h₂ ≤ capacity o ε (retentiveSources : Set (Source M)) (Stable m) c ∧
      capacity o ε (retentiveSources : Set (Source M)) (Stable m) c ≤ c * h₁ := by
  sorry

/-- **The persistent rung is free under bounded geometry.** If the packing
    numbers of the balls of radius `2ε` at resolution `ε` are uniformly
    bounded, the persistent capacity over retentive sources equals the block
    capacity, `c · h_pack`, and the block rate is itself achieved with
    addresses that never move. -/
theorem capacity_stable_eq_packing_of_boundedGeometry (o : M) {ε : ℝ≥0} (hε : 0 < ε)
    {c h : ℝ} (hc : 0 < c) (m : ℝ≥0) {Mb : ℕ}
    (hMb : ∀ x : M, Metric.packingNumber ε (Metric.closedBall x ((2 * ε : ℝ≥0) : ℝ)) ≤ Mb)
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h)) :
    capacity o ε (retentiveSources : Set (Source M)) (Stable m) c = c * h ∧
      capacity o ε (retentiveSources : Set (Source M)) (noExtra : Obligation M M) c =
        c * h ∧
      Tendsto (Packing.packingRate o ε) atTop (𝓝 h) := by
  sorry

/-- The structured chain at the persistent rung over retentive sources, with
    an exact block endpoint, under bounded geometry:

        β ≤ C_persistent ≤ C_block = c · h_pack. -/
theorem persistent_chain (o : M) {ε : ℝ≥0} (hε : 0 < ε) {β c h : ℝ} (hc : 0 < c) (m : ℝ≥0)
    {Mb : ℕ}
    (hMb : ∀ x : M, Metric.packingNumber ε (Metric.closedBall x ((2 * ε : ℝ≥0) : ℝ)) ≤ Mb)
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h))
    (hβ : Achievable o ε (retentiveSources : Set (Source M)) (Stable m) β c) :
    β ≤ capacity o ε (retentiveSources : Set (Source M)) (Stable m) c ∧
      capacity o ε (retentiveSources : Set (Source M)) (Stable m) c ≤
        capacity o ε (retentiveSources : Set (Source M)) (noExtra : Obligation M M) c ∧
      capacity o ε (retentiveSources : Set (Source M)) (noExtra : Obligation M M) c =
        c * h := by
  sorry

end Capacity

end Challenges.Persistent
