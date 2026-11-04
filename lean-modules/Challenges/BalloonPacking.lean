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

namespace Challenges.BalloonPacking

open Filter
open scoped ENNReal NNReal Topology
open ActiveGeometry
open ActiveGeometry.Constrained
open ActiveGeometry.Constrained.Balloon

/-! ### Closed balls are finite -/

/-- Hubs and leaves of index at most `n`. -/
def ballFinset (n : ℕ) : Finset Balloon :=
  (Finset.range (n + 1)).image hub ∪
    (Finset.range (n + 1)).biUnion
      (fun i => (Finset.univ : Finset (Fin (2 ^ i))).image (leaf i))

theorem mem_ballFinset_of_hubIndex_le {x : Balloon} {n : ℕ} (h : hubIndex x ≤ n) :
    x ∈ ballFinset n := by
  sorry

theorem closedBall_subset_ballFinset {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Metric.closedBall (hub 0) ρ ⊆ (ballFinset ⌊ρ⌋₊ : Set Balloon) := by
  sorry

theorem sum_two_pow_lt (n : ℕ) : ∑ i ∈ Finset.range n, 2 ^ i < 2 ^ n := by
  sorry

theorem succ_lt_two_pow_succ (n : ℕ) : n + 1 < 2 ^ (n + 1) := by
  sorry

theorem card_ballFinset_le (n : ℕ) : (ballFinset n).card ≤ 2 ^ (n + 2) := by
  sorry

theorem closedBall_finite {ρ : ℝ} (hρ : 0 ≤ ρ) : (Metric.closedBall (hub 0) ρ).Finite := by
  sorry

/-! ### Proper, with finite packing numbers -/

instance : ProperSpace Balloon := ⟨fun x r => by
  have hsub : Metric.closedBall x r ⊆
      Metric.closedBall (hub 0) (max r 0 + dist x (hub 0)) :=
    (Metric.closedBall_subset_closedBall (le_max_left r 0)).trans
      (Metric.closedBall_subset_closedBall' le_rfl)
  exact ((closedBall_finite (add_nonneg (le_max_right r 0) dist_nonneg)).subset hsub).isCompact⟩

theorem balloon_hasFinitePacking (ε : ℝ≥0) : Packing.HasFinitePacking (hub 0) ε := by
  sorry

/-! ### The leaves of one hub: a 1-separated set -/

def leavesOf (m : ℕ) : Finset Balloon := (Finset.univ : Finset (Fin (2 ^ m))).image (leaf m)

theorem leaf_injective (m : ℕ) : Function.Injective (leaf m) := by
  sorry

theorem card_leavesOf (m : ℕ) : (leavesOf m).card = 2 ^ m := by
  sorry

theorem leavesOf_separated (m : ℕ) :
    Metric.IsSeparated (1 : ℝ≥0) (leavesOf m : Set Balloon) := by
  sorry

theorem leavesOf_subset_closedBall (m : ℕ) :
    (leavesOf m : Set Balloon) ⊆ Metric.closedBall (hub 0) (m + 1) := by
  sorry

/-! ### Packing counts, squeezed -/

theorem two_pow_le_packingCount {ρ : ℝ} (hρ : 1 ≤ ρ) :
    2 ^ (⌊ρ⌋₊ - 1) ≤ Packing.packingCount (hub 0) 1 ρ := by
  sorry

theorem packingCount_le_two_pow {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount (hub 0) 1 ρ ≤ 2 ^ (⌊ρ⌋₊ + 2) := by
  sorry

/-- **`h_pack(B, hub 0; 1) = log 2`.** -/
theorem balloon_packingRate_tendsto :
    Tendsto (Packing.packingRate (hub 0) 1) atTop (𝓝 (Real.log 2)) := by
  sorry

/-! ### A metric-ULF source of growth zero that is relationally representable -/

/-- The one-history source. -/
def trivialSource : Source (List Bool) where
  census _ := {[]}
  census_nonempty _ := ⟨[], by simp⟩

theorem trivialSource_hasGrowth : trivialSource.HasGrowth 0 := by
  sorry

theorem trivialSource_metricULF : trivialSource.MetricULF := by
  sorry

/-- Put the single history at `hub R`, radius `R`. -/
def trivialCode : Code (List Bool) Balloon where
  addr R _ := hub R
  radius R := R

theorem trivialSource_represents (q : Distortion) :
    Represents (hub 0) 1 (Relational q) trivialSource 1 := by
  sorry

theorem zero_mem_rates_relational (q : Distortion) :
    (0 : ℝ) ∈ Rates (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) (Relational q) 1 := by
  sorry

/-! ### The separation as two numbers -/

theorem balloon_capacity_block_eq :
    capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra 1 = Real.log 2 := by
  sorry

theorem balloon_capacity_relational_eq_zero (q : Distortion) :
    capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) (Relational q) 1 = 0 := by
  sorry

/-- **Capacity-level separation, as numbers.** Over metric-ULF sources at
    `ε = c = 1`: `C_rel(B) = 0 < log 2 = C_block(B)`, for every lawful
    distortion. -/
theorem balloon_capacity_strict (q : Distortion) :
    capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) (Relational q) 1 <
      capacity (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra 1 := by
  sorry

end Challenges.BalloonPacking
