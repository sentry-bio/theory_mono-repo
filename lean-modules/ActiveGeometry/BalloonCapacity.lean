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

namespace ActiveGeometry.Constrained

open Filter
open scoped ENNReal NNReal Topology
open Balloon

variable {S : Type*} [PseudoMetricSpace S]

/-! ### Metric uniform local finiteness of a source -/

/-- Bounded balls in the source metric, uniformly over the census: a bound
    `f t` on the number of census histories within source distance `t` of any
    census history, at every depth. -/
def Source.MetricULF (σ : Source S) : Prop :=
  ∃ f : ℕ → ℕ, ∀ R, ∀ u ∈ σ.census R, ∀ t : ℕ,
    ((σ.census R).filter (fun v => dist u v ≤ (t : ℝ))).card ≤ f t

def metricUlfSources : Set (Source S) := {σ | σ.MetricULF}

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
  classical
  have hDpos : 0 < q.multiplicative :=
    lt_of_lt_of_le (by norm_num : (0 : ℝ) < 1) q.one_le_multiplicative
  -- fibres of the hub index are small: same star ⇒ host distance ≤ 2 ⇒
  -- source distance ≤ D (2 + K)
  have hfib : ∀ b ∈ (σ.census R).image (fun u => hubIndex (κ.addr R u)),
      ((σ.census R).filter (fun u => hubIndex (κ.addr R u) = b)).card ≤
        f ⌈q.multiplicative * (2 + q.additive)⌉₊ := by
    intro b hb'
    rcases Finset.mem_image.mp hb' with ⟨u, hu, rfl⟩
    refine le_trans (Finset.card_le_card ?_) (hf R u hu _)
    intro v hv
    rcases Finset.mem_filter.mp hv with ⟨hv, hidx⟩
    refine Finset.mem_filter.mpr ⟨hv, ?_⟩
    have h2 : dist (κ.addr R u) (κ.addr R v) ≤ 2 := by
      have hn : balloonNDist (κ.addr R u) (κ.addr R v) ≤ 2 :=
        balloonNDist_le_two_of_hubIndex_eq hidx.symm
      have : (balloonNDist (κ.addr R u) (κ.addr R v) : ℝ) ≤ 2 := by exact_mod_cast hn
      simpa [dist] using this
    have hlow := (hrel R u hu v hv).1
    have hmul : q.multiplicative⁻¹ * dist u v ≤ 2 + q.additive := by linarith
    have hdist : dist u v ≤ q.multiplicative * (2 + q.additive) := by
      have := mul_le_mul_of_nonneg_left hmul hDpos.le
      rwa [← mul_assoc, mul_inv_cancel₀ hDpos.ne', one_mul] at this
    exact hdist.trans (Nat.le_ceil _)
  -- the hub index of a radial address is at most ⌊r(R)⌋₊
  have himg : (σ.census R).image (fun u => hubIndex (κ.addr R u)) ⊆
      Finset.range (⌊κ.radius R⌋₊ + 1) := by
    intro n hn
    rcases Finset.mem_image.mp hn with ⟨u, hu, rfl⟩
    have hmem : κ.addr R u ∈ Metric.closedBall (hub 0) (κ.radius R) :=
      hb.2 R (Set.mem_image_of_mem _ (by exact_mod_cast hu))
    have hle : (balloonNDist (hub 0) (κ.addr R u) : ℝ) ≤ κ.radius R := by
      simpa [Metric.mem_closedBall, dist, balloonNDist_comm (hub 0)] using hmem
    have : (hubIndex (κ.addr R u) : ℝ) ≤ κ.radius R :=
      (Nat.cast_le.mpr (hubIndex_le_dist_hub0 _)).trans hle
    exact Finset.mem_range.mpr (Nat.lt_succ_of_le ((Nat.le_floor_iff hρ).mpr this))
  calc (σ.census R).card
      ≤ f ⌈q.multiplicative * (2 + q.additive)⌉₊ *
          ((σ.census R).image (fun u => hubIndex (κ.addr R u))).card :=
        Finset.card_le_mul_card_image _ _ hfib
    _ ≤ f ⌈q.multiplicative * (2 + q.additive)⌉₊ * (⌊κ.radius R⌋₊ + 1) := by
        have := Finset.card_le_card himg
        simpa [Finset.card_range] using Nat.mul_le_mul_left _ this

/-! ### No positive relational rate -/

/-- **Metric-ULF sources have no positive relational rate in the balloon**, at
    any radial rate and any resolution. -/
theorem metricULF_not_relational_pos (q : Distortion) {σ : Source S}
    (hσ : σ.MetricULF) {β : ℝ} (hβ : 0 < β) (hg : σ.HasGrowth β)
    (ε : ℝ≥0) (c : ℝ) :
    ¬ Represents (hub 0) ε (Relational q) σ c := by
  rintro ⟨κ, hb, hrel, hdiv, hc⟩
  obtain ⟨f, hf⟩ := hσ
  obtain ⟨N, hN⟩ : ∃ N : ℕ, f ⌈q.multiplicative * (2 + q.additive)⌉₊ = N := ⟨_, rfl⟩
  have hEv : ∀ᶠ R : ℕ in atTop,
      κ.radius R < (c + 1) * R ∧ 0 ≤ κ.radius R ∧
      β / 2 * R < Real.log ((σ.census R).card : ℝ) ∧ 0 < R := by
    have h1 := hc.eventually (gt_mem_nhds (by linarith : c < c + 1))
    have h2 := hdiv.eventually (eventually_ge_atTop (0 : ℝ))
    have h3 := hg.eventually (lt_mem_nhds (by linarith : β / 2 < β))
    filter_upwards [h1, h2, h3, eventually_gt_atTop 0] with R hr hρ hl hR
    have hRpos : (0 : ℝ) < R := by exact_mod_cast hR
    exact ⟨(div_lt_iff₀ hRpos).mp hr, hρ, (lt_div_iff₀ hRpos).mp hl, hR⟩
  obtain ⟨n0, hn0⟩ := eventually_atTop.mp hEv
  -- a depth beyond `n0` at which the quadratic lower bound beats the linear
  -- upper bound
  obtain ⟨R, hR⟩ : ∃ R : ℕ, R = n0 + ⌈16 * (N : ℝ) * (|c| + 2) / β ^ 2⌉₊ + 1 := ⟨_, rfl⟩
  have hRn0 : n0 ≤ R := by omega
  obtain ⟨hrad, hρ, hlog, hRpos⟩ := hn0 R hRn0
  have hRr : (0 : ℝ) < R := by exact_mod_cast hRpos
  have hR1 : (1 : ℝ) ≤ R := by exact_mod_cast hRpos
  have hbig : 16 * (N : ℝ) * (|c| + 2) / β ^ 2 < R := by
    have hcast : (R : ℝ) = n0 + ⌈16 * (N : ℝ) * (|c| + 2) / β ^ 2⌉₊ + 1 := by
      rw [hR]; push_cast; ring
    have := Nat.le_ceil (16 * (N : ℝ) * (|c| + 2) / β ^ 2)
    have hn0' : (0 : ℝ) ≤ n0 := Nat.cast_nonneg n0
    linarith
  -- counting bound, as reals
  have hcount := census_card_le_of_relational hf q hb hrel R hρ
  rw [hN] at hcount
  have hcountR : ((σ.census R).card : ℝ) ≤ (N : ℝ) * (κ.radius R + 1) := by
    have h1 : ((σ.census R).card : ℝ) ≤ (N : ℝ) * ((⌊κ.radius R⌋₊ : ℝ) + 1) := by
      exact_mod_cast hcount
    have h2 : (⌊κ.radius R⌋₊ : ℝ) ≤ κ.radius R := Nat.floor_le hρ
    nlinarith [Nat.cast_nonneg (α := ℝ) N]
  have hlin : (N : ℝ) * (κ.radius R + 1) ≤ (N : ℝ) * ((|c| + 2) * R) := by
    have hc' : c ≤ |c| := le_abs_self c
    have : κ.radius R + 1 ≤ (|c| + 2) * R := by nlinarith [hrad, hR1, hc']
    exact mul_le_mul_of_nonneg_left this (Nat.cast_nonneg N)
  -- exponential lower bound on the census
  have hcardpos : (0 : ℝ) < (σ.census R).card := by
    exact_mod_cast Finset.card_pos.mpr (σ.census_nonempty R)
  have hexp : Real.exp (β / 2 * R) ≤ (σ.census R).card :=
    (Real.le_log_iff_exp_le hcardpos).mp hlog.le
  have hsq : (β * R / 4) ^ 2 ≤ Real.exp (β / 2 * R) := by
    have h := Real.add_one_le_exp (β * R / 4)
    have hpos : 0 ≤ β * R / 4 := by positivity
    have hsplit : Real.exp (β / 2 * R) = Real.exp (β * R / 4) * Real.exp (β * R / 4) := by
      rw [← Real.exp_add]; congr 1; ring
    rw [hsplit]
    nlinarith [h, hpos]
  -- the quadratic beats the linear bound
  have hquad : (N : ℝ) * ((|c| + 2) * R) < (β * R / 4) ^ 2 := by
    have hβ2 : 0 < β ^ 2 := by positivity
    have h := (div_lt_iff₀ hβ2).mp hbig
    have h' := mul_lt_mul_of_pos_right h hRr
    have e : (β * R / 4) ^ 2 = β ^ 2 * R * R / 16 := by ring
    rw [e]; nlinarith [h']
  linarith [hcountR, hlin, hexp, hsq, hquad]

/-- Over metric-ULF sources, the balloon's relational rate set lies in `{0}`,
    for every lawful distortion, resolution and radial rate. -/
theorem balloon_rates_relational_subset (q : Distortion) (ε : ℝ≥0) (c : ℝ) :
    Rates (hub 0) ε (metricUlfSources : Set (Source S)) (Relational q) c ⊆ {0} := by
  rintro β ⟨σ, hσ, hg, hr⟩
  by_contra hne
  have hne' : β ≠ 0 := fun h => hne (Set.mem_singleton_iff.mpr h)
  have hpos : 0 < β := lt_of_le_of_ne hg.nonneg hne'.symm
  exact metricULF_not_relational_pos q hσ hpos hg ε c hr

/-- Scalar form: the balloon's relational capacity over metric-ULF sources is
    at most zero. -/
theorem balloon_capacity_relational_le_zero (q : Distortion) (ε : ℝ≥0) (c : ℝ) :
    capacity (hub 0) ε (metricUlfSources : Set (Source S)) (Relational q) c ≤ 0 :=
  Real.sSup_le
    (fun _ hβ => le_of_eq (Set.mem_singleton_iff.mp (balloon_rates_relational_subset q ε c hβ)))
    le_rfl

/-! ### The binary tree is metric-ULF -/

theorem take_eq_of_le_lcp : ∀ (p : ℕ) (u v : List Bool), p ≤ lcp u v → u.take p = v.take p
  | 0, _, _, _ => by simp
  | p + 1, [], v, h => by simp [lcp] at h
  | p + 1, x :: xs, [], h => by simp [lcp] at h
  | p + 1, x :: xs, y :: ys, h => by
      by_cases hxy : x = y
      · subst hxy
        simp only [lcp, ite_true] at h
        simp [List.take_succ_cons, take_eq_of_le_lcp p xs ys (by omega)]
      · simp [lcp, hxy] at h

/-- A ball of radius `t` in the generation-`R` binary tree has at most `2^t`
    vertices: its members share a prefix of length `R − t`. -/
theorem card_ball_le_of_wordsOfLength {R t : ℕ} {u : List Bool}
    (hu : u ∈ wordsOfLength R) :
    ((wordsOfLength R).filter (fun v => dist u v ≤ (t : ℝ))).card ≤ 2 ^ t := by
  classical
  have hulen : u.length = R := mem_wordsOfLength.mp hu
  obtain ⟨p, hp⟩ : ∃ p : ℕ, p = R - t := ⟨_, rfl⟩
  have hpre : ∀ v ∈ (wordsOfLength R).filter (fun v => dist u v ≤ (t : ℝ)),
      v.take p = u.take p := by
    intro v hv
    rcases Finset.mem_filter.mp hv with ⟨hv, hd⟩
    have hvlen : v.length = R := mem_wordsOfLength.mp hv
    have hd' : treeNDist u v ≤ t := by
      have : (treeNDist u v : ℝ) ≤ t := by simpa [dist] using hd
      exact_mod_cast this
    have hl : lcp u v ≤ R := hulen ▸ lcp_le_length_left u v
    have hlcp : p ≤ lcp u v := by
      simp only [treeNDist, hulen, hvlen] at hd'
      omega
    exact (take_eq_of_le_lcp p u v hlcp).symm
  have hmaps : ∀ v ∈ (wordsOfLength R).filter (fun v => dist u v ≤ (t : ℝ)),
      v.drop p ∈ wordsOfLength (R - p) := by
    intro v hv
    have hvlen : v.length = R := mem_wordsOfLength.mp (Finset.mem_filter.mp hv).1
    exact mem_wordsOfLength.mpr (by simp [hvlen])
  have hinj : Set.InjOn (fun v : List Bool => v.drop p)
      ((wordsOfLength R).filter (fun v => dist u v ≤ (t : ℝ)) : Set (List Bool)) := by
    intro v hv w hw hvw
    have hv' := hpre v (by exact_mod_cast hv)
    have hw' := hpre w (by exact_mod_cast hw)
    have hvw' : v.drop p = w.drop p := by simpa using hvw
    calc v = v.take p ++ v.drop p := (List.take_append_drop p v).symm
      _ = w.take p ++ w.drop p := by rw [hv', hw', hvw']
      _ = w := List.take_append_drop p w
  calc ((wordsOfLength R).filter (fun v => dist u v ≤ (t : ℝ))).card
      ≤ (wordsOfLength (R - p)).card := Finset.card_le_card_of_injOn _ hmaps hinj
    _ = 2 ^ (R - p) := card_wordsOfLength _
    _ ≤ 2 ^ t := Nat.pow_le_pow_right (by norm_num) (by omega)

theorem binaryTreeSource_metricULF : binaryTreeSource.MetricULF :=
  ⟨fun t => 2 ^ t, fun R u hu t => by
    have hu' : u ∈ wordsOfLength R := by simpa [binaryTreeSource] using hu
    simpa [binaryTreeSource] using card_ball_le_of_wordsOfLength (t := t) hu'⟩

theorem binaryTreeSource_mem_metricUlf :
    binaryTreeSource ∈ (metricUlfSources : Set (Source (List Bool))) :=
  binaryTreeSource_metricULF

/-! ### Separation at the level of the family -/

/-- **Capacity-level separation over metric-ULF sources.** The balloon's block
    rate set over the family contains `log 2`; its relational rate set does not
    (it lies in `{0}`), for every lawful distortion. -/
theorem balloon_capacity_separation (q : Distortion) :
    Real.log 2 ∈ Rates (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra 1 ∧
    Real.log 2 ∉ Rates (hub 0) 1 (metricUlfSources : Set (Source (List Bool)))
      (Relational q) 1 := by
  refine ⟨?_, ?_⟩
  · obtain ⟨σ, hσ, hg, hr⟩ := binaryTree_block_achievable
    have hσ' : σ = binaryTreeSource := by simpa using hσ
    subst hσ'
    exact ⟨_, binaryTreeSource_mem_metricUlf, hg, hr⟩
  · intro h
    have h0 := Set.mem_singleton_iff.mp (balloon_rates_relational_subset q 1 1 h)
    have : (0 : ℝ) < Real.log 2 := Real.log_pos (by norm_num)
    linarith

/-- The two rate sets differ over the metric-ULF family (`Separates`). -/
theorem balloon_separates_metricUlf (q : Distortion) :
    Separates (hub 0) 1 (metricUlfSources : Set (Source (List Bool))) noExtra
      (Relational q) 1 := by
  intro heq
  obtain ⟨hin, hout⟩ := balloon_capacity_separation q
  exact hout (heq ▸ hin)

end ActiveGeometry.Constrained
