/-
  The balloon is proper and has packing entropy log 2 at resolution 1
  ===================================================================

  Closes the "true, not yet formalized" row of the September note. Closed
  balls of the balloon are finite (`ballFinset`), so the space is proper and
  packing numbers are finite; the `2^m` leaves of hub `m` are a 1-separated set
  in the ball of radius `m + 1`, and the ball of radius `ρ` has fewer than
  `2^(⌊ρ⌋₊ + 2)` points, so the packing rate is squeezed to `log 2`.

  With `ProperSpace Balloon` and the rate limit, the scalar capacity theorems of
  `Constrained.lean` apply to the balloon, and the separation of
  `BalloonCapacity.lean` becomes a statement about two numbers over the
  metric-ULF family at `ε = c = 1`:

      capacity_rel = 0  <  log 2 = capacity_block.
-/
import ActiveGeometry.BalloonCapacity

namespace ActiveGeometry.Constrained

open Filter
open scoped ENNReal NNReal Topology
open Balloon

/-! ### Closed balls are finite -/

/-- Hubs and leaves of index at most `n`. -/
def ballFinset (n : ℕ) : Finset Balloon :=
  (Finset.range (n + 1)).image hub ∪
    (Finset.range (n + 1)).biUnion
      (fun i => (Finset.univ : Finset (Fin (2 ^ i))).image (leaf i))

theorem mem_ballFinset_of_hubIndex_le {x : Balloon} {n : ℕ} (h : hubIndex x ≤ n) :
    x ∈ ballFinset n := by
  classical
  cases x with
  | hub i =>
      apply Finset.mem_union_left
      exact Finset.mem_image.mpr
        ⟨i, Finset.mem_range.mpr (Nat.lt_succ_of_le (by simpa [hubIndex] using h)), rfl⟩
  | leaf i a =>
      apply Finset.mem_union_right
      refine Finset.mem_biUnion.mpr
        ⟨i, Finset.mem_range.mpr (Nat.lt_succ_of_le (by simpa [hubIndex] using h)), ?_⟩
      exact Finset.mem_image.mpr ⟨a, Finset.mem_univ _, rfl⟩

theorem closedBall_subset_ballFinset {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Metric.closedBall (hub 0) ρ ⊆ (ballFinset ⌊ρ⌋₊ : Set Balloon) := by
  intro x hx
  have hle : (balloonNDist (hub 0) x : ℝ) ≤ ρ := by
    simpa [Metric.mem_closedBall, dist, balloonNDist_comm (hub 0) x] using hx
  have h1 : (hubIndex x : ℝ) ≤ ρ := (Nat.cast_le.mpr (hubIndex_le_dist_hub0 x)).trans hle
  have h2 : hubIndex x ≤ ⌊ρ⌋₊ := (Nat.le_floor_iff hρ).mpr h1
  exact Finset.mem_coe.mpr (mem_ballFinset_of_hubIndex_le h2)

theorem sum_two_pow_lt (n : ℕ) : ∑ i ∈ Finset.range n, 2 ^ i < 2 ^ n := by
  induction n with
  | zero => simp
  | succ n ih => rw [Finset.sum_range_succ, pow_succ]; omega

theorem succ_lt_two_pow_succ (n : ℕ) : n + 1 < 2 ^ (n + 1) := by
  induction n with
  | zero => norm_num
  | succ n ih => rw [pow_succ]; omega

theorem card_ballFinset_le (n : ℕ) : (ballFinset n).card ≤ 2 ^ (n + 2) := by
  classical
  have h1 : ((Finset.range (n + 1)).image hub).card ≤ n + 1 := by
    simpa using Finset.card_image_le (s := Finset.range (n + 1)) (f := hub)
  have h2 : ((Finset.range (n + 1)).biUnion
      (fun i => (Finset.univ : Finset (Fin (2 ^ i))).image (leaf i))).card ≤ 2 ^ (n + 1) := by
    refine le_trans Finset.card_biUnion_le ?_
    refine le_trans (Finset.sum_le_sum fun i _ => Finset.card_image_le) ?_
    simp only [Finset.card_univ, Fintype.card_fin]
    exact (sum_two_pow_lt (n + 1)).le
  calc (ballFinset n).card
      ≤ ((Finset.range (n + 1)).image hub).card +
        ((Finset.range (n + 1)).biUnion
          (fun i => (Finset.univ : Finset (Fin (2 ^ i))).image (leaf i))).card :=
        Finset.card_union_le _ _
    _ ≤ (n + 1) + 2 ^ (n + 1) := Nat.add_le_add h1 h2
    _ ≤ 2 ^ (n + 1) + 2 ^ (n + 1) := by have := succ_lt_two_pow_succ n; omega
    _ = 2 ^ (n + 2) := by ring

theorem closedBall_finite {ρ : ℝ} (hρ : 0 ≤ ρ) : (Metric.closedBall (hub 0) ρ).Finite :=
  (Finset.finite_toSet _).subset (closedBall_subset_ballFinset hρ)

/-! ### Proper, with finite packing numbers -/

instance : ProperSpace Balloon := ⟨fun x r => by
  have hsub : Metric.closedBall x r ⊆
      Metric.closedBall (hub 0) (max r 0 + dist x (hub 0)) :=
    (Metric.closedBall_subset_closedBall (le_max_left r 0)).trans
      (Metric.closedBall_subset_closedBall' le_rfl)
  exact ((closedBall_finite (add_nonneg (le_max_right r 0) dist_nonneg)).subset hsub).isCompact⟩

theorem balloon_hasFinitePacking (ε : ℝ≥0) : Packing.HasFinitePacking (hub 0) ε := by
  intro ρ hρ
  exact ne_top_of_le_ne_top (Set.encard_ne_top_iff.mpr (closedBall_finite hρ))
    (Metric.packingNumber_le_encard_self _)

/-! ### The leaves of one hub: a 1-separated set -/

def leavesOf (m : ℕ) : Finset Balloon := (Finset.univ : Finset (Fin (2 ^ m))).image (leaf m)

theorem leaf_injective (m : ℕ) : Function.Injective (leaf m) := fun a b h => by
  cases h; rfl

theorem card_leavesOf (m : ℕ) : (leavesOf m).card = 2 ^ m := by
  rw [leavesOf, Finset.card_image_of_injective _ (leaf_injective m)]
  simp

theorem leavesOf_separated (m : ℕ) :
    Metric.IsSeparated (1 : ℝ≥0) (leavesOf m : Set Balloon) := by
  intro x hx y hy hxy
  rcases Finset.mem_image.mp (Finset.mem_coe.mp hx) with ⟨a, _, rfl⟩
  rcases Finset.mem_image.mp (Finset.mem_coe.mp hy) with ⟨b, _, rfl⟩
  have hab : a.val ≠ b.val := fun h => hxy (congrArg (leaf m) (Fin.ext h))
  have hd : dist (leaf m a) (leaf m b) = 2 := by
    show (balloonNDist (leaf m a) (leaf m b) : ℝ) = 2
    simp [balloonNDist, hab]
  rw [edist_dist, hd]
  simp

theorem leavesOf_subset_closedBall (m : ℕ) :
    (leavesOf m : Set Balloon) ⊆ Metric.closedBall (hub 0) (m + 1) := by
  intro x hx
  rcases Finset.mem_image.mp (Finset.mem_coe.mp hx) with ⟨a, _, rfl⟩
  rw [Metric.mem_closedBall]
  show (balloonNDist (leaf m a) (hub 0) : ℝ) ≤ m + 1
  rw [balloonNDist_comm, balloonNDist_hub0_leaf]
  push_cast
  exact le_rfl

/-! ### Packing counts, squeezed -/

theorem two_pow_le_packingCount {ρ : ℝ} (hρ : 1 ≤ ρ) :
    2 ^ (⌊ρ⌋₊ - 1) ≤ Packing.packingCount (hub 0) 1 ρ := by
  have hfl : 1 ≤ ⌊ρ⌋₊ := (Nat.one_le_floor_iff ρ).mpr hρ
  have hsub : (leavesOf (⌊ρ⌋₊ - 1) : Set Balloon) ⊆ Metric.closedBall (hub 0) ρ := by
    refine (leavesOf_subset_closedBall _).trans (Metric.closedBall_subset_closedBall ?_)
    have h1 : ((⌊ρ⌋₊ - 1 : ℕ) : ℝ) + 1 = ⌊ρ⌋₊ := by
      rw [Nat.cast_sub hfl]; push_cast; ring
    rw [h1]; exact Nat.floor_le (by linarith)
  have := Packing.card_le_packingCount (hub 0) 1 ρ (leavesOf (⌊ρ⌋₊ - 1)) (by linarith)
    (balloon_hasFinitePacking 1) (leavesOf_separated _) hsub
  simpa [card_leavesOf] using this

theorem packingCount_le_two_pow {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount (hub 0) 1 ρ ≤ 2 ^ (⌊ρ⌋₊ + 2) := by
  have h1 : Metric.packingNumber (1 : ℝ≥0) (Metric.closedBall (hub 0) ρ) ≤
      ((ballFinset ⌊ρ⌋₊).card : ℕ∞) := by
    calc Metric.packingNumber (1 : ℝ≥0) (Metric.closedBall (hub 0) ρ)
        ≤ (Metric.closedBall (hub 0) ρ).encard := Metric.packingNumber_le_encard_self _
      _ ≤ ((ballFinset ⌊ρ⌋₊ : Set Balloon)).encard :=
          Set.encard_le_encard (closedBall_subset_ballFinset hρ)
      _ = ((ballFinset ⌊ρ⌋₊).card : ℕ∞) := Set.encard_coe_eq_coe_finsetCard _
  have h2 : Packing.packingCount (hub 0) 1 ρ ≤ (ballFinset ⌊ρ⌋₊).card := by
    unfold Packing.packingCount
    have := ENat.toNat_le_toNat h1 (ENat.natCast_ne_top _)
    simpa using this
  exact h2.trans (card_ballFinset_le _)

/-- **`h_pack(B, hub 0; 1) = log 2`.** -/
theorem balloon_packingRate_tendsto :
    Tendsto (Packing.packingRate (hub 0) 1) atTop (𝓝 (Real.log 2)) := by
  have hlow : ∀ᶠ ρ : ℝ in atTop,
      ((⌊ρ⌋₊ : ℝ) / ρ - ρ⁻¹) * Real.log 2 ≤ Packing.packingRate (hub 0) 1 ρ := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with ρ hρ
    have hρ0 : 0 < ρ := by linarith
    have hfl : 1 ≤ ⌊ρ⌋₊ := (Nat.one_le_floor_iff ρ).mpr hρ
    have hcR : ((2 : ℝ) ^ (⌊ρ⌋₊ - 1)) ≤ (Packing.packingCount (hub 0) 1 ρ : ℝ) := by
      exact_mod_cast two_pow_le_packingCount hρ
    have hpos : (0 : ℝ) < (2 : ℝ) ^ (⌊ρ⌋₊ - 1) := by positivity
    have hl := Real.log_le_log hpos hcR
    rw [Real.log_pow] at hl
    have hcast : ((⌊ρ⌋₊ - 1 : ℕ) : ℝ) = (⌊ρ⌋₊ : ℝ) - 1 := by rw [Nat.cast_sub hfl]; simp
    rw [hcast] at hl
    unfold Packing.packingRate
    calc ((⌊ρ⌋₊ : ℝ) / ρ - ρ⁻¹) * Real.log 2
        = (((⌊ρ⌋₊ : ℝ) - 1) * Real.log 2) / ρ := by ring
      _ ≤ Real.log (Packing.packingCount (hub 0) 1 ρ : ℝ) / ρ :=
          div_le_div_of_nonneg_right hl hρ0.le
  have hup : ∀ᶠ ρ : ℝ in atTop,
      Packing.packingRate (hub 0) 1 ρ ≤ ((⌊ρ⌋₊ : ℝ) / ρ + 2 * ρ⁻¹) * Real.log 2 := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with ρ hρ
    have hρ0 : 0 < ρ := by linarith
    have hcR : ((2 : ℝ) ^ (⌊ρ⌋₊ - 1)) ≤ (Packing.packingCount (hub 0) 1 ρ : ℝ) := by
      exact_mod_cast two_pow_le_packingCount hρ
    have hpos : (0 : ℝ) < (Packing.packingCount (hub 0) 1 ρ : ℝ) :=
      lt_of_lt_of_le (by positivity) hcR
    have hcU : (Packing.packingCount (hub 0) 1 ρ : ℝ) ≤ (2 : ℝ) ^ (⌊ρ⌋₊ + 2) := by
      exact_mod_cast packingCount_le_two_pow hρ0.le
    have hl := Real.log_le_log hpos hcU
    rw [Real.log_pow] at hl
    push_cast at hl
    unfold Packing.packingRate
    calc Real.log (Packing.packingCount (hub 0) 1 ρ : ℝ) / ρ
        ≤ (((⌊ρ⌋₊ : ℝ) + 2) * Real.log 2) / ρ := div_le_div_of_nonneg_right hl hρ0.le
      _ = ((⌊ρ⌋₊ : ℝ) / ρ + 2 * ρ⁻¹) * Real.log 2 := by ring
  have hg : Tendsto (fun ρ : ℝ => ((⌊ρ⌋₊ : ℝ) / ρ - ρ⁻¹) * Real.log 2) atTop
      (𝓝 (Real.log 2)) := by
    have := (tendsto_nat_floor_div_atTop.sub tendsto_inv_atTop_zero).mul_const (Real.log 2)
    simpa using this
  have hh : Tendsto (fun ρ : ℝ => ((⌊ρ⌋₊ : ℝ) / ρ + 2 * ρ⁻¹) * Real.log 2) atTop
      (𝓝 (Real.log 2)) := by
    have := (tendsto_nat_floor_div_atTop.add (tendsto_inv_atTop_zero.const_mul 2)).mul_const
      (Real.log 2)
    simpa using this
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le' hg hh hlow hup

/-! ### A metric-ULF source of growth zero that is relationally representable -/

/-- The one-history source. -/
def trivialSource : Source (List Bool) where
  census _ := {[]}
  census_nonempty _ := ⟨[], by simp⟩

theorem trivialSource_hasGrowth : trivialSource.HasGrowth 0 := by
  unfold Source.HasGrowth
  simp [trivialSource]

theorem trivialSource_metricULF : trivialSource.MetricULF :=
  ⟨fun _ => 1, fun R u _ t => by
    simpa [trivialSource] using Finset.card_filter_le ({[]} : Finset (List Bool))
      (fun v => dist u v ≤ (t : ℝ))⟩

/-- Put the single history at `hub R`, radius `R`. -/
def trivialCode : Code (List Bool) Balloon where
  addr R _ := hub R
  radius R := R

theorem trivialSource_represents (q : Distortion) :
    Represents (hub 0) 1 (Relational q) trivialSource 1 := by
  refine ⟨trivialCode, ⟨?_, ?_⟩, ?_, ?_, ?_⟩
  · intro R
    refine ⟨?_, ?_⟩
    · intro u hu v hv _
      simp [trivialSource] at hu hv
      rw [hu, hv]
    · have : book trivialSource trivialCode R = {hub R} := by
        ext x; simp [book, trivialSource, trivialCode]
      rw [this]
      exact Metric.IsSeparated.singleton
  · intro R x hx
    simp [book, trivialSource, trivialCode] at hx
    subst hx
    rw [Metric.mem_closedBall]
    show (balloonNDist (hub R) (hub 0) : ℝ) ≤ (trivialCode.radius R)
    rw [balloonNDist_comm, balloonNDist_hub0_hub]
    exact le_rfl
  · intro R u hu v hv
    simp [trivialSource] at hu hv
    subst hu; subst hv
    simp [trivialCode, q.additive_nonneg]
  · exact tendsto_natCast_atTop_atTop
  · have : ∀ᶠ R : ℕ in atTop, trivialCode.radius R / (R : ℝ) = 1 := by
      filter_upwards [eventually_gt_atTop 0] with R hR
      have : (R : ℝ) ≠ 0 := by exact_mod_cast hR.ne'
      simp [trivialCode, this]
    exact tendsto_const_nhds.congr' (this.mono fun R h => h.symm)

theorem zero_mem_rates_relational (q : Distortion) :
    (0 : ℝ) ∈ Rates (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) (Relational q) 1 :=
  ⟨trivialSource, trivialSource_metricULF, trivialSource_hasGrowth, trivialSource_represents q⟩

/-! ### The separation as two numbers -/

theorem balloon_capacity_block_eq :
    capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra 1 = Real.log 2 := by
  have hend : Achievable (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra
      (1 * Real.log 2) 1 := by
    rw [one_mul]
    exact (balloon_capacity_separation ⟨1, 0, le_rfl, le_rfl⟩).1
  have := capacity_eq_packing_of_endpoint_achievable (o := hub 0) (ε := 1) (by norm_num)
    balloon_packingRate_tendsto hend
  simpa using this

theorem balloon_capacity_relational_eq_zero (q : Distortion) :
    capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) (Relational q) 1 = 0 := by
  apply le_antisymm (balloon_capacity_relational_le_zero q 1 1)
  exact le_csSup (Rates_bddAbove (by norm_num) balloon_packingRate_tendsto)
    (zero_mem_rates_relational q)

/-- **Capacity-level separation, as numbers.** Over metric-ULF sources at
    `ε = c = 1`: `C_rel(B) = 0 < log 2 = C_block(B)`, for every lawful
    distortion. -/
theorem balloon_capacity_strict (q : Distortion) :
    capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) (Relational q) 1 <
      capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra 1 := by
  rw [balloon_capacity_block_eq, balloon_capacity_relational_eq_zero]
  exact Real.log_pos (by norm_num)

end ActiveGeometry.Constrained
