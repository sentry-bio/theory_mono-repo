/-
  The persistent rung
  ===================

  Rung 2 of the admissibility ladder asks for one nested address family: the
  census accretes (`Source.Retentive`) and an address, once assigned, never
  moves (`Stable 0`). Depthwise recoding (`Structured.lean`) chooses a fresh
  optimal packing at every radius and so says nothing about this rung.

  This file closes the rung by an explicit construction with no choice beyond
  Mathlib's maximal separated sets:

  * `extendSeparated ε A B` enlarges a separated set `A ⊆ B` to a separated
    subset of `B` that `ε`-covers `B`, by adjoining a maximal separated subset
    of the points of `B` farther than `ε` from `A`. No Zorn argument: the
    extension is `A ∪ maximalSeparatedSet ε (farSet ε A B)`.
  * `nestedSet o ε c R` iterates this at the radii `c R`. The sets are nested,
    `ε`-separated, finite, inside the ball of radius `c R`, and cover it; so
    their cardinality is at least the packing number of the ball at
    resolution `2 ε` (`packingNumber_two_mul_le_externalCoveringNumber`).
  * `persistentSource` thins the nested sets to a nested census of cardinality
    exactly `packingCount o (2 ε) (c R)` (`Finset.exists_subsuperset_card_eq`),
    so that its growth is exactly `c · h_pack(2ε)`.
  * The identity code is `Base`, `Stable m` for every `m`, and has radial rate
    `c`. Hence, over retentive sources,

        c · h_pack(2ε)  ≤  C_persistent(ε)  ≤  C_block(ε)  =  c · h_pack(ε)

    (`capacity_stable_between`), and under bounded geometry at the scales
    `(ε, 2ε)` the scale-invariance theorem of `CoarseConverse.lean` closes the
    gap: the persistent rung costs nothing
    (`capacity_stable_eq_packing_of_boundedGeometry`).

  Everything here is unconditional on the host beyond properness; the
  resolution shift `ε → 2ε` is the only price of nesting, and bounded
  geometry removes it.
-/

import ActiveGeometry.Structured
import ActiveGeometry.CoarseConverse

namespace ActiveGeometry.Constrained

open Filter
open scoped ENNReal NNReal Topology

variable {M : Type*} [MetricSpace M]

/-! ### Packing numbers are monotone in the set -/

theorem packingNumber_mono_set {ε : ℝ≥0} {A B : Set M} (h : A ⊆ B) :
    Metric.packingNumber ε A ≤ Metric.packingNumber ε B := by
  simp only [Metric.packingNumber, iSup_le_iff]
  intro C hCA hC
  exact hC.encard_le_packingNumber (hCA.trans h)

theorem packingCount_mono_radius [ProperSpace M] (o : M) {ε : ℝ≥0} (hε : ε ≠ 0)
    {ρ ρ' : ℝ} (hρ : 0 ≤ ρ) (h : ρ ≤ ρ') :
    Packing.packingCount o ε ρ ≤ Packing.packingCount o ε ρ' := by
  unfold Packing.packingCount
  exact ENat.toNat_le_toNat
    (packingNumber_mono_set (Metric.closedBall_subset_closedBall h))
    (Packing.hasFinitePacking_of_properSpace o hε (hρ.trans h))

theorem two_mul_ne_zero_of_ne_zero {ε : ℝ≥0} (hε : ε ≠ 0) : (2 * ε : ℝ≥0) ≠ 0 :=
  mul_ne_zero two_ne_zero hε

/-- The identity code never moves an address. -/
theorem recodingCode_stable (σ : Source M) (c : ℝ) (m : ℝ≥0) :
    Stable m σ (recodingCode c) := by
  intro R s _
  simp [recodingCode]

/-! ### Extending a separated set to a covering one -/

/-- The points of `B` farther than `ε` from every point of `A`. -/
def farSet (ε : ℝ≥0) (A B : Set M) : Set M :=
  {x | x ∈ B ∧ ∀ a ∈ A, (ε : ℝ≥0∞) < edist x a}

theorem farSet_subset (ε : ℝ≥0) (A B : Set M) : farSet ε A B ⊆ B :=
  fun _ hx => hx.1

/-- Extend a separated set `A ⊆ B` to a separated subset of `B` that covers
    `B`: adjoin a maximal separated subset of the far points. -/
noncomputable def extendSeparated (ε : ℝ≥0) (A B : Set M) : Set M :=
  A ∪ Metric.maximalSeparatedSet ε (farSet ε A B)

theorem subset_extendSeparated (ε : ℝ≥0) (A B : Set M) :
    A ⊆ extendSeparated ε A B :=
  Set.subset_union_left

theorem extendSeparated_subset {ε : ℝ≥0} {A B : Set M} (hA : A ⊆ B) :
    extendSeparated ε A B ⊆ B :=
  Set.union_subset hA (Metric.maximalSeparatedSet_subset.trans (farSet_subset ε A B))

theorem isSeparated_extendSeparated {ε : ℝ≥0} {A : Set M} (B : Set M)
    (hA : Metric.IsSeparated ε A) :
    Metric.IsSeparated ε (extendSeparated ε A B) := by
  unfold extendSeparated
  rw [Metric.IsSeparated, Set.pairwise_union]
  refine ⟨hA, Metric.isSeparated_maximalSeparatedSet, ?_⟩
  intro a ha d hd _
  have hfar : d ∈ farSet ε A B := Metric.maximalSeparatedSet_subset hd
  have h1 : (ε : ℝ≥0∞) < edist d a := hfar.2 a ha
  exact ⟨by simpa [edist_comm] using h1, h1⟩

theorem packingNumber_farSet_ne_top {ε : ℝ≥0} {A B : Set M}
    (hfin : Metric.packingNumber ε B ≠ ⊤) :
    Metric.packingNumber ε (farSet ε A B) ≠ ⊤ :=
  ne_top_of_le_ne_top hfin (packingNumber_mono_set (farSet_subset ε A B))

theorem extendSeparated_isCover {ε : ℝ≥0} {A B : Set M}
    (hfin : Metric.packingNumber ε B ≠ ⊤) :
    Metric.IsCover ε B (extendSeparated ε A B) := by
  intro x hx
  by_cases hnear : ∃ a ∈ A, edist x a ≤ (ε : ℝ≥0∞)
  · obtain ⟨a, ha, hxa⟩ := hnear
    exact ⟨a, Set.subset_union_left ha, hxa⟩
  · push Not at hnear
    have hxfar : x ∈ farSet ε A B := ⟨hx, hnear⟩
    obtain ⟨d, hd, hxd⟩ :=
      Metric.isCover_maximalSeparatedSet (packingNumber_farSet_ne_top hfin) hxfar
    exact ⟨d, Set.subset_union_right hd, hxd⟩

theorem extendSeparated_finite {ε : ℝ≥0} {A B : Set M} (hA : A.Finite)
    (hfin : Metric.packingNumber ε B ≠ ⊤) :
    (extendSeparated ε A B).Finite := by
  refine hA.union ?_
  have hfin' := packingNumber_farSet_ne_top (A := A) hfin
  refine Set.encard_ne_top_iff.mp ?_
  rw [Metric.encard_maximalSeparatedSet hfin']
  exact hfin'

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
    nestedSet o ε c 0 = extendSeparated ε ∅ (Metric.closedBall o (c * ((0 : ℕ) : ℝ))) :=
  rfl

theorem nestedSet_succ (o : M) (ε : ℝ≥0) (c : ℝ) (R : ℕ) :
    nestedSet o ε c (R + 1) =
      extendSeparated ε (nestedSet o ε c R)
        (Metric.closedBall o (c * ((R + 1 : ℕ) : ℝ))) :=
  rfl

section Nested

variable [ProperSpace M]
variable (o : M) {ε : ℝ≥0} (hε : ε ≠ 0) {c : ℝ} (hc : 0 ≤ c)
include hε hc

theorem ball_packingNumber_ne_top (R : ℕ) :
    Metric.packingNumber ε (Metric.closedBall o (c * (R : ℝ))) ≠ ⊤ :=
  Packing.hasFinitePacking_of_properSpace o hε (mul_nonneg hc (Nat.cast_nonneg _))

omit [ProperSpace M] hε in
theorem nestedSet_subset_closedBall (R : ℕ) :
    nestedSet o ε c R ⊆ Metric.closedBall o (c * (R : ℝ)) := by
  induction R with
  | zero => exact extendSeparated_subset (Set.empty_subset _)
  | succ R ih =>
    rw [nestedSet_succ]
    refine extendSeparated_subset (ih.trans (Metric.closedBall_subset_closedBall ?_))
    exact mul_le_mul_of_nonneg_left (by exact_mod_cast Nat.le_succ R) hc

omit [ProperSpace M] hε hc in
theorem nestedSet_isSeparated (R : ℕ) : Metric.IsSeparated ε (nestedSet o ε c R) := by
  induction R with
  | zero => exact isSeparated_extendSeparated _ Metric.IsSeparated.empty
  | succ R ih =>
    rw [nestedSet_succ]
    exact isSeparated_extendSeparated _ ih

theorem nestedSet_finite (R : ℕ) : (nestedSet o ε c R).Finite := by
  induction R with
  | zero => exact extendSeparated_finite Set.finite_empty (ball_packingNumber_ne_top o hε hc 0)
  | succ R ih =>
    rw [nestedSet_succ]
    exact extendSeparated_finite ih (ball_packingNumber_ne_top o hε hc (R + 1))

omit [ProperSpace M] hε hc in
theorem nestedSet_mono (R : ℕ) : nestedSet o ε c R ⊆ nestedSet o ε c (R + 1) := by
  rw [nestedSet_succ]
  exact subset_extendSeparated ε _ _

theorem nestedSet_isCover (R : ℕ) :
    Metric.IsCover ε (Metric.closedBall o (c * (R : ℝ))) (nestedSet o ε c R) := by
  cases R with
  | zero => exact extendSeparated_isCover (ball_packingNumber_ne_top o hε hc 0)
  | succ R => exact extendSeparated_isCover (ball_packingNumber_ne_top o hε hc (R + 1))

/-- The nested sets as finsets. -/
noncomputable def nestedFinset (R : ℕ) : Finset M :=
  (nestedSet_finite o hε hc R).toFinset

theorem coe_nestedFinset (R : ℕ) : (nestedFinset o hε hc R : Set M) = nestedSet o ε c R :=
  (nestedSet_finite o hε hc R).coe_toFinset

theorem nestedFinset_mono (R : ℕ) : nestedFinset o hε hc R ⊆ nestedFinset o hε hc (R + 1) :=
  Set.Finite.toFinset_subset_toFinset.mpr (nestedSet_mono o R)

/-- A covering separated set is at least as large as the packing number at
    twice the resolution. -/
theorem packingCount_two_mul_le_nestedFinset_card (R : ℕ) :
    Packing.packingCount o (2 * ε) (c * (R : ℝ)) ≤ (nestedFinset o hε hc R).card := by
  have h1 :
      Metric.packingNumber (2 * ε) (Metric.closedBall o (c * (R : ℝ))) ≤
        (nestedSet o ε c R).encard :=
    (Metric.packingNumber_two_mul_le_externalCoveringNumber ε _).trans
      (nestedSet_isCover o hε hc R).externalCoveringNumber_le_encard
  have hfinN : (nestedSet o ε c R).encard ≠ ⊤ :=
    (nestedSet_finite o hε hc R).encard_lt_top.ne
  have h2 := ENat.toNat_le_toNat h1 hfinN
  unfold Packing.packingCount
  rw [(nestedSet_finite o hε hc R).encard_eq_coe_toFinset_card, ENat.toNat_natCast] at h2
  exact h2

/-! ### The thinned nested census -/

theorem persistentCount_mono (R : ℕ) :
    persistentCount o ε c R ≤ persistentCount o ε c (R + 1) :=
  packingCount_mono_radius o (two_mul_ne_zero_of_ne_zero hε)
    (mul_nonneg hc (Nat.cast_nonneg _))
    (mul_le_mul_of_nonneg_left (by exact_mod_cast Nat.le_succ R) hc)

theorem one_le_persistentCount (R : ℕ) : 1 ≤ persistentCount o ε c R :=
  Packing.one_le_packingCount o (2 * ε) (c * (R : ℝ)) (mul_nonneg hc (Nat.cast_nonneg _))
    (Packing.hasFinitePacking_of_properSpace o (two_mul_ne_zero_of_ne_zero hε))

/-- A nested census of the right size inside the nested finsets. -/
abbrev PersistentCell (R : ℕ) : Type _ :=
  {s : Finset M // s ⊆ nestedFinset o hε hc R ∧ s.card = persistentCount o ε c R}

theorem persistentBase_exists :
    ∃ u : Finset M, (∅ : Finset M) ⊆ u ∧ u ⊆ nestedFinset o hε hc 0 ∧
      u.card = persistentCount o ε c 0 :=
  Finset.exists_subsuperset_card_eq (Finset.empty_subset _) (by simp)
    (packingCount_two_mul_le_nestedFinset_card o hε hc 0)

theorem persistentStep_exists (R : ℕ) (prev : PersistentCell o hε hc R) :
    ∃ u : Finset M, prev.1 ⊆ u ∧ u ⊆ nestedFinset o hε hc (R + 1) ∧
      u.card = persistentCount o ε c (R + 1) :=
  Finset.exists_subsuperset_card_eq (prev.2.1.trans (nestedFinset_mono o hε hc R))
    (by rw [prev.2.2]; exact persistentCount_mono o hε hc R)
    (packingCount_two_mul_le_nestedFinset_card o hε hc (R + 1))

noncomputable def persistentStep (R : ℕ) (prev : PersistentCell o hε hc R) :
    PersistentCell o hε hc (R + 1) :=
  ⟨Classical.choose (persistentStep_exists o hε hc R prev),
    (Classical.choose_spec (persistentStep_exists o hε hc R prev)).2.1,
    (Classical.choose_spec (persistentStep_exists o hε hc R prev)).2.2⟩

theorem persistentStep_subset (R : ℕ) (prev : PersistentCell o hε hc R) :
    prev.1 ⊆ (persistentStep o hε hc R prev).1 :=
  (Classical.choose_spec (persistentStep_exists o hε hc R prev)).1

noncomputable def persistentCell : (R : ℕ) → PersistentCell o hε hc R
  | 0 =>
      ⟨Classical.choose (persistentBase_exists o hε hc),
        (Classical.choose_spec (persistentBase_exists o hε hc)).2.1,
        (Classical.choose_spec (persistentBase_exists o hε hc)).2.2⟩
  | R + 1 => persistentStep o hε hc R (persistentCell R)

theorem persistentCell_succ (R : ℕ) :
    persistentCell o hε hc (R + 1) = persistentStep o hε hc R (persistentCell o hε hc R) :=
  rfl

theorem persistentCell_mono (R : ℕ) :
    (persistentCell o hε hc R).1 ⊆ (persistentCell o hε hc (R + 1)).1 := by
  rw [persistentCell_succ]
  exact persistentStep_subset o hε hc R _

theorem persistentCell_card (R : ℕ) :
    (persistentCell o hε hc R).1.card = persistentCount o ε c R :=
  (persistentCell o hε hc R).2.2

theorem persistentCell_subset_nestedSet (R : ℕ) :
    ((persistentCell o hε hc R).1 : Set M) ⊆ nestedSet o ε c R := by
  rw [← coe_nestedFinset o hε hc R]
  exact Finset.coe_subset.mpr (persistentCell o hε hc R).2.1

theorem persistentCell_nonempty (R : ℕ) : (persistentCell o hε hc R).1.Nonempty :=
  Finset.card_pos.mp (by rw [persistentCell_card]; exact one_le_persistentCount o hε hc R)

/-- The persistent source: a retentive census that is a nested family of
    `ε`-separated points inside the balls of radius `c R`. -/
noncomputable def persistentSource : Source M where
  census R := (persistentCell o hε hc R).1
  census_nonempty R := persistentCell_nonempty o hε hc R

theorem persistentSource_census (R : ℕ) :
    (persistentSource o hε hc).census R = (persistentCell o hε hc R).1 :=
  rfl

theorem persistentSource_retentive : (persistentSource o hε hc).Retentive :=
  fun R => persistentCell_mono o hε hc R

theorem persistentSource_mem_retentive :
    persistentSource o hε hc ∈ (retentiveSources : Set (Source M)) :=
  persistentSource_retentive o hε hc

theorem persistentSource_card (R : ℕ) :
    ((persistentSource o hε hc).census R).card =
      Packing.packingCount o (2 * ε) (c * (R : ℝ)) :=
  persistentCell_card o hε hc R

/-! ### The identity code never moves an address -/

theorem book_persistent (R : ℕ) :
    book (persistentSource o hε hc) (recodingCode c) R =
      ((persistentCell o hε hc R).1 : Set M) := by
  simp [book, recodingCode, persistentSource]

theorem recodingCode_base_persistent :
    Base o ε (persistentSource o hε hc) (recodingCode c) := by
  constructor
  · intro R
    constructor
    · exact Set.injOn_id _
    · rw [book_persistent]
      exact (nestedSet_isSeparated o R).subset (persistentCell_subset_nestedSet o hε hc R)
  · intro R
    rw [book_persistent]
    have hr : ((recodingCode c : Code M M).radius R) = c * (R : ℝ) := rfl
    rw [hr]
    exact (persistentCell_subset_nestedSet o hε hc R).trans (nestedSet_subset_closedBall o hc R)

end Nested

/-! ### Achievability and capacity at the persistent rung -/

section Capacity

variable [ProperSpace M]

theorem persistentSource_hasGrowth (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c h : ℝ} (hc : 0 < c)
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h)) :
    (persistentSource o hε.ne' hc.le).HasGrowth (c * h) := by
  have hρ : Tendsto (fun R : ℕ => c * (R : ℝ)) atTop atTop :=
    tendsto_natCast_atTop_atTop.const_mul_atTop hc
  have hsampled :
      Tendsto (fun R : ℕ => Packing.packingRate o (2 * ε) (c * (R : ℝ))) atTop (𝓝 h) :=
    hlow.comp hρ
  have hmul :
      Tendsto (fun R : ℕ => c * Packing.packingRate o (2 * ε) (c * (R : ℝ))) atTop
        (𝓝 (c * h)) :=
    hsampled.const_mul c
  refine hmul.congr' ?_
  filter_upwards [eventually_gt_atTop 0] with R hR
  rw [persistentSource_card, Packing.packingRate, ← mul_div_assoc,
    mul_div_mul_left _ _ hc.ne']

theorem recodingCode_represents_persistent (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c : ℝ}
    (hc : 0 < c) (m : ℝ≥0) :
    Represents o ε (Stable m) (persistentSource o hε.ne' hc.le) c := by
  refine ⟨(recodingCode c : Code M M), recodingCode_base_persistent o hε.ne' hc.le,
    recodingCode_stable _ c m, ?_, ?_⟩
  · exact tendsto_natCast_atTop_atTop.const_mul_atTop hc
  · refine tendsto_const_nhds.congr' ?_
    filter_upwards [eventually_gt_atTop 0] with R hR
    have hR' : (R : ℝ) ≠ 0 := by exact_mod_cast (Nat.ne_of_gt hR)
    simp [recodingCode, hR']

/-- **The persistent rung is achievable at the packing rate of twice the
    resolution.** Over retentive sources, with addresses that never move, the
    rate `c · h_pack(2ε)` is achieved; the only price of nesting is the
    resolution shift `ε → 2ε`. -/
theorem achievable_stable_persistent (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c h : ℝ}
    (hc : 0 < c) (m : ℝ≥0)
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h)) :
    Achievable o ε (retentiveSources : Set (Source M)) (Stable m) (c * h) c :=
  ⟨persistentSource o hε.ne' hc.le, persistentSource_mem_retentive o hε.ne' hc.le,
    persistentSource_hasGrowth o hε hc hlow,
    recodingCode_represents_persistent o hε hc m⟩

/-- Over retentive sources the persistent capacity sits between the packing
    rates at `2ε` and at `ε`:

        c · h_pack(2ε) ≤ C_persistent(ε) ≤ c · h_pack(ε). -/
theorem capacity_stable_between (o : M) {ε : ℝ≥0} (hε : 0 < ε) {c h₁ h₂ : ℝ}
    (hc : 0 < c) (m : ℝ≥0)
    (hup : Tendsto (Packing.packingRate o ε) atTop (𝓝 h₁))
    (hlow : Tendsto (Packing.packingRate o (2 * ε)) atTop (𝓝 h₂)) :
    c * h₂ ≤ capacity o ε (retentiveSources : Set (Source M)) (Stable m) c ∧
      capacity o ε (retentiveSources : Set (Source M)) (Stable m) c ≤ c * h₁ := by
  have hach := achievable_stable_persistent o hε hc m hlow
  constructor
  · unfold capacity
    exact le_csSup (Rates_bddAbove hε hup) hach
  · exact capacity_le_packing hε hup ⟨c * h₂, hach⟩

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
  have hle : ε ≤ 2 * ε := le_mul_of_one_le_left (by simp) one_le_two
  have hup : Tendsto (Packing.packingRate o ε) atTop (𝓝 h) :=
    packingRate_scale_invariant hε.ne' (two_mul_ne_zero_of_ne_zero hε.ne') hle hMb hlow
  have hach := achievable_stable_persistent o hε hc m hlow
  refine ⟨capacity_eq_packing_of_endpoint_achievable hε hup hach, ?_, hup⟩
  exact capacity_eq_packing_of_endpoint_achievable hε hup
    (hach.mono_obligation (fun _ _ _ => trivial))

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
  obtain ⟨_, _, hup⟩ := capacity_stable_eq_packing_of_boundedGeometry o hε hc m hMb hlow
  exact structured_addressability_limit hε hup hβ
    ((achievable_stable_persistent o hε hc m hlow).mono_obligation (fun _ _ _ => trivial))

end Capacity

end ActiveGeometry.Constrained
