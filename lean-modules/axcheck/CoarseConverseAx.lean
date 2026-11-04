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
import BalloonPacking

namespace ActiveGeometry.Constrained

open Filter
open scoped ENNReal NNReal Topology
open Balloon

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
  classical
  have hDpos : 0 < q.multiplicative :=
    lt_of_lt_of_le (by norm_num : (0 : ℝ) < 1) q.one_le_multiplicative
  have hfin : Metric.packingNumber ε' (Metric.closedBall o (κ.radius R)) ≠ ⊤ :=
    Packing.hasFinitePacking_of_properSpace o hε' hρ
  have hYfin : (Metric.maximalSeparatedSet ε' (Metric.closedBall o (κ.radius R))).Finite :=
    Set.encard_ne_top_iff.mp (by rw [Metric.encard_maximalSeparatedSet hfin]; exact hfin)
  have hmem : ∀ u ∈ σ.census R, κ.addr R u ∈ Metric.closedBall o (κ.radius R) :=
    fun u hu => hb.2 R (Set.mem_image_of_mem _ (by exact_mod_cast hu))
  -- every address is within ε' of a point of the maximal separated set
  have hcov : ∀ x ∈ Metric.closedBall o (κ.radius R),
      ∃ y ∈ Metric.maximalSeparatedSet ε' (Metric.closedBall o (κ.radius R)), dist x y ≤ (ε' : ℝ) := by
    intro x hx
    obtain ⟨y, hy, hd0⟩ := Metric.isCover_maximalSeparatedSet hfin hx
    refine ⟨y, hy, ?_⟩
    have hd : edist x y ≤ (ε' : ℝ≥0∞) := hd0
    rw [edist_dist] at hd
    have := (ENNReal.ofReal_le_iff_le_toReal ENNReal.coe_ne_top).mp hd
    simpa using this
  let G : S → M := fun u =>
    if h : u ∈ σ.census R then (hcov _ (hmem u h)).choose else o
  have hG : ∀ u ∈ σ.census R,
      G u ∈ Metric.maximalSeparatedSet ε' (Metric.closedBall o (κ.radius R)) ∧
        dist (κ.addr R u) (G u) ≤ (ε' : ℝ) := by
    intro u hu
    simp only [G, dif_pos hu]
    exact (hcov _ (hmem u hu)).choose_spec
  -- fibres of G are small: shared cell ⇒ host distance ≤ 2ε' ⇒ source distance ≤ D(2ε'+K)
  have hfib : ∀ y ∈ (σ.census R).image G,
      ((σ.census R).filter (fun u => G u = y)).card ≤
        f ⌈q.multiplicative * (2 * ε' + q.additive)⌉₊ := by
    intro y hy
    rcases Finset.mem_image.mp hy with ⟨u, hu, rfl⟩
    refine le_trans (Finset.card_le_card ?_) (hf R u hu _)
    intro v hv
    rcases Finset.mem_filter.mp hv with ⟨hv, hGv⟩
    refine Finset.mem_filter.mpr ⟨hv, ?_⟩
    have h1 := (hG u hu).2
    have h2 := (hG v hv).2
    have hd : dist (κ.addr R u) (κ.addr R v) ≤ 2 * ε' := by
      calc dist (κ.addr R u) (κ.addr R v)
          ≤ dist (κ.addr R u) (G u) + dist (G u) (κ.addr R v) := dist_triangle _ _ _
        _ ≤ ε' + ε' := add_le_add h1 (by rw [← hGv, dist_comm]; exact h2)
        _ = 2 * ε' := by ring
    have hlow := (hrel R u hu v hv).1
    have hmul : q.multiplicative⁻¹ * dist u v ≤ 2 * ε' + q.additive := by linarith
    have hdist : dist u v ≤ q.multiplicative * (2 * ε' + q.additive) := by
      have := mul_le_mul_of_nonneg_left hmul hDpos.le
      rwa [← mul_assoc, mul_inv_cancel₀ hDpos.ne', one_mul] at this
    exact hdist.trans (Nat.le_ceil _)
  -- the image lies in the maximal separated set, whose size is the packing count
  have himg : (σ.census R).image G ⊆ hYfin.toFinset := by
    intro y hy
    rcases Finset.mem_image.mp hy with ⟨u, hu, rfl⟩
    exact hYfin.mem_toFinset.mpr (hG u hu).1
  have hYcard : hYfin.toFinset.card = Packing.packingCount o ε' (κ.radius R) := by
    unfold Packing.packingCount
    have h1 : (hYfin.toFinset.card : ℕ∞) =
        (Metric.maximalSeparatedSet ε' (Metric.closedBall o (κ.radius R))).encard := by
      rw [← Set.encard_coe_eq_coe_finsetCard, hYfin.coe_toFinset]
    rw [← Metric.encard_maximalSeparatedSet hfin, ← h1]
    simp
  calc (σ.census R).card
      ≤ f ⌈q.multiplicative * (2 * ε' + q.additive)⌉₊ * ((σ.census R).image G).card :=
        Finset.card_le_mul_card_image _ _ hfib
    _ ≤ f ⌈q.multiplicative * (2 * ε' + q.additive)⌉₊ * hYfin.toFinset.card :=
        Nat.mul_le_mul_left _ (Finset.card_le_card himg)
    _ = _ := by rw [hYcard]

/-! ### The rate form -/

/-- **Coarse packing converse.** Over metric-ULF sources, a relational rate is
    bounded by `c` times the packing entropy at EVERY scale `ε' > 0`. -/
theorem coarse_packing_converse [ProperSpace M] {o : M} {ε ε' : ℝ≥0} (hε' : ε' ≠ 0) {h' : ℝ}
    (hpacking : Tendsto (Packing.packingRate o ε') atTop (𝓝 h')) (q : Distortion)
    {σ : Source S} (hσ : σ.MetricULF) {β : ℝ} (hg : σ.HasGrowth β) {c : ℝ}
    (hr : Represents o ε (Relational q) σ c) : β ≤ c * h' := by
  obtain ⟨κ, hb, hrel, hdiv, hc⟩ := hr
  obtain ⟨f, hf⟩ := hσ
  obtain ⟨N, hN⟩ : ∃ N : ℕ, f ⌈q.multiplicative * (2 * ε' + q.additive)⌉₊ = N := ⟨_, rfl⟩
  have hev : ∀ᶠ R : ℕ in atTop,
      Real.log ((σ.census R).card : ℝ) / R ≤
        Real.log N / R + Packing.packingRate o ε' (κ.radius R) * (κ.radius R / R) := by
    filter_upwards [hdiv.eventually (eventually_gt_atTop (0 : ℝ)), eventually_gt_atTop 0]
      with R hρ hR
    have hRpos : (0 : ℝ) < R := by exact_mod_cast hR
    have hcount := census_card_le_coarse_packing hf q hb hrel ε' hε' R hρ.le
    rw [hN] at hcount
    have hcard1 : 1 ≤ (σ.census R).card := Finset.card_pos.mpr (σ.census_nonempty R)
    have hNpos : 0 < N := by
      rcases Nat.eq_zero_or_pos N with h | h
      · rw [h, zero_mul] at hcount; omega
      · exact h
    have hPpos : 0 < Packing.packingCount o ε' (κ.radius R) := by
      rcases Nat.eq_zero_or_pos (Packing.packingCount o ε' (κ.radius R)) with h | h
      · rw [h, mul_zero] at hcount; omega
      · exact h
    have hcardpos : (0 : ℝ) < (σ.census R).card := by exact_mod_cast hcard1
    have hlog : Real.log ((σ.census R).card : ℝ) ≤
        Real.log N + Real.log (Packing.packingCount o ε' (κ.radius R) : ℝ) := by
      rw [← Real.log_mul (by exact_mod_cast hNpos.ne') (by exact_mod_cast hPpos.ne')]
      apply Real.log_le_log hcardpos
      exact_mod_cast hcount
    have hr0 : κ.radius R ≠ 0 := hρ.ne'
    have hrate : Packing.packingRate o ε' (κ.radius R) * (κ.radius R / R) =
        Real.log (Packing.packingCount o ε' (κ.radius R) : ℝ) / R := by
      unfold Packing.packingRate
      field_simp
    rw [hrate, ← add_div]
    exact div_le_div_of_nonneg_right hlog hRpos.le
  have hlim : Tendsto
      (fun R : ℕ => Real.log N / R + Packing.packingRate o ε' (κ.radius R) * (κ.radius R / R))
      atTop (𝓝 (0 + h' * c)) :=
    (tendsto_const_div_atTop_nhds_zero_nat _).add ((hpacking.comp hdiv).mul hc)
  have := le_of_tendsto_of_tendsto hg hlim hev
  linarith

/-! ### The balloon above the diameter of its stars -/

/-- At any scale `ε' ≥ 2` the balloon's ball of radius `ρ` packs at most
    `⌊ρ⌋₊ + 1` points: one per star. -/
theorem balloon_packingCount_le {ε' : ℝ≥0} (hε' : 2 ≤ (ε' : ℝ)) {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount (hub 0) ε' ρ ≤ ⌊ρ⌋₊ + 1 := by
  classical
  have hfin : Metric.packingNumber ε' (Metric.closedBall (hub 0) ρ) ≠ ⊤ :=
    balloon_hasFinitePacking ε' hρ
  have hYfin : (Metric.maximalSeparatedSet ε' (Metric.closedBall (hub 0) ρ)).Finite :=
    Set.encard_ne_top_iff.mp (by rw [Metric.encard_maximalSeparatedSet hfin]; exact hfin)
  have hsub : (hYfin.toFinset : Set Balloon) ⊆ Metric.closedBall (hub 0) ρ := by
    rw [hYfin.coe_toFinset]; exact Metric.maximalSeparatedSet_subset
  have hfar : ∀ a ∈ hYfin.toFinset, ∀ b ∈ hYfin.toFinset, a ≠ b → 2 < balloonNDist a b := by
    intro a ha b hb hab
    have h0 := Metric.isSeparated_maximalSeparatedSet (ε := ε') (A := Metric.closedBall (hub 0) ρ)
      (hYfin.mem_toFinset.mp ha) (hYfin.mem_toFinset.mp hb) hab
    have h : (ε' : ℝ≥0∞) < edist a b := h0
    rw [edist_dist, ← ENNReal.ofReal_coe_nnreal] at h
    have h2 : (ε' : ℝ) < dist a b :=
      (ENNReal.ofReal_lt_ofReal_iff_of_nonneg (by positivity)).mp h
    have h3 : (2 : ℝ) < (balloonNDist a b : ℝ) := by
      have : dist a b = (balloonNDist a b : ℝ) := rfl
      linarith
    exact_mod_cast h3
  have hle := card_pairwise_gt_two_le_floor (ρ := ρ) hsub hfar
  have hYcard : hYfin.toFinset.card = Packing.packingCount (hub 0) ε' ρ := by
    unfold Packing.packingCount
    have h1 : (hYfin.toFinset.card : ℕ∞) =
        (Metric.maximalSeparatedSet ε' (Metric.closedBall (hub 0) ρ)).encard := by
      rw [← Set.encard_coe_eq_coe_finsetCard, hYfin.coe_toFinset]
    rw [← Metric.encard_maximalSeparatedSet hfin, ← h1]
    simp
  rw [← hYcard]
  exact hle

/-- **The balloon's coarse packing entropy is zero**: at every scale `ε' ≥ 2`
    the packing rate tends to `0`. -/
theorem balloon_coarse_entropy_zero {ε' : ℝ≥0} (hε' : 2 ≤ (ε' : ℝ)) :
    Tendsto (Packing.packingRate (hub 0) ε') atTop (𝓝 0) := by
  have hup : ∀ᶠ ρ : ℝ in atTop,
      Packing.packingRate (hub 0) ε' ρ ≤ Real.log (ρ + 1) / ρ := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with ρ hρ
    have hρ0 : 0 < ρ := by linarith
    have hc := balloon_packingCount_le hε' hρ0.le
    unfold Packing.packingRate
    apply div_le_div_of_nonneg_right _ hρ0.le
    rcases Nat.eq_zero_or_pos (Packing.packingCount (hub 0) ε' ρ) with h0 | hpos
    · rw [h0]; simp
      exact Real.log_nonneg (by linarith)
    · apply Real.log_le_log (by exact_mod_cast hpos)
      have : (Packing.packingCount (hub 0) ε' ρ : ℝ) ≤ (⌊ρ⌋₊ : ℝ) + 1 := by exact_mod_cast hc
      linarith [Nat.floor_le hρ0.le]
  have hlow : ∀ᶠ ρ : ℝ in atTop, 0 ≤ Packing.packingRate (hub 0) ε' ρ := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with ρ hρ
    unfold Packing.packingRate
    apply div_nonneg _ hρ.le
    rcases Nat.eq_zero_or_pos (Packing.packingCount (hub 0) ε' ρ) with h0 | hpos
    · simp [h0]
    · exact Real.log_nonneg (by exact_mod_cast hpos)
  have hlim : Tendsto (fun ρ : ℝ => Real.log (ρ + 1) / ρ) atTop (𝓝 0) := by
    have h := Real.tendsto_pow_log_div_mul_add_atTop 1 (-1) 1 one_ne_zero
    have h2 := h.comp (tendsto_atTop_add_const_right atTop (1 : ℝ) tendsto_id)
    refine h2.congr' ?_
    filter_upwards with ρ
    show Real.log (ρ + 1) ^ 1 / (1 * (ρ + 1) + -1) = Real.log (ρ + 1) / ρ
    rw [pow_one]
    congr 1
    ring
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le' tendsto_const_nhds hlim hlow hup

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
  have hfinE := Packing.hasFinitePacking_of_properSpace o hε hρ
  have hfinE' := Packing.hasFinitePacking_of_properSpace o hε' hρ
  have hsep : Metric.IsSeparated ε (Metric.maximalSeparatedSet ε' (Metric.closedBall o ρ)) :=
    (Metric.isSeparated_maximalSeparatedSet).anti (ENNReal.coe_le_coe.mpr hle)
  have h1 := hsep.encard_le_packingNumber (Metric.maximalSeparatedSet_subset)
  rw [Metric.encard_maximalSeparatedSet hfinE'] at h1
  unfold Packing.packingCount
  exact ENat.toNat_le_toNat h1 hfinE

/-- Under bounded geometry at scales `ε ≤ ε'`, the fine count is at most `Mb`
    times the coarse count. -/
theorem packingCount_le_mul_packingCount [ProperSpace M] {o : M} {ε ε' : ℝ≥0}
    (hε : ε ≠ 0) (hε' : ε' ≠ 0) {Mb : ℕ}
    (hMb : ∀ x : M, Metric.packingNumber ε (Metric.closedBall x ε') ≤ Mb)
    {ρ : ℝ} (hρ : 0 ≤ ρ) :
    Packing.packingCount o ε ρ ≤ Mb * Packing.packingCount o ε' ρ := by
  classical
  have hfinE : Metric.packingNumber ε (Metric.closedBall o ρ) ≠ ⊤ :=
    Packing.hasFinitePacking_of_properSpace o hε hρ
  have hfinE' : Metric.packingNumber ε' (Metric.closedBall o ρ) ≠ ⊤ :=
    Packing.hasFinitePacking_of_properSpace o hε' hρ
  have hXfin : (Metric.maximalSeparatedSet ε (Metric.closedBall o ρ)).Finite :=
    Set.encard_ne_top_iff.mp (by rw [Metric.encard_maximalSeparatedSet hfinE]; exact hfinE)
  have hYfin : (Metric.maximalSeparatedSet ε' (Metric.closedBall o ρ)).Finite :=
    Set.encard_ne_top_iff.mp (by rw [Metric.encard_maximalSeparatedSet hfinE']; exact hfinE')
  have hcov : ∀ x ∈ Metric.closedBall o ρ,
      ∃ y ∈ Metric.maximalSeparatedSet ε' (Metric.closedBall o ρ), dist x y ≤ (ε' : ℝ) := by
    intro x hx
    obtain ⟨y, hy, hd0⟩ := Metric.isCover_maximalSeparatedSet hfinE' hx
    refine ⟨y, hy, ?_⟩
    have hd : edist x y ≤ (ε' : ℝ≥0∞) := hd0
    rw [edist_dist] at hd
    have := (ENNReal.ofReal_le_iff_le_toReal ENNReal.coe_ne_top).mp hd
    simpa using this
  let G : M → M := fun x =>
    if h : x ∈ Metric.closedBall o ρ then (hcov _ h).choose else o
  have hG : ∀ x ∈ Metric.closedBall o ρ,
      G x ∈ Metric.maximalSeparatedSet ε' (Metric.closedBall o ρ) ∧ dist x (G x) ≤ (ε' : ℝ) := by
    intro x hx
    simp only [G, dif_pos hx]
    exact (hcov _ hx).choose_spec
  have hXsub : ∀ x ∈ hXfin.toFinset, x ∈ Metric.closedBall o ρ := fun x hx =>
    Metric.maximalSeparatedSet_subset (hXfin.mem_toFinset.mp hx)
  have hfib : ∀ y ∈ hXfin.toFinset.image G,
      (hXfin.toFinset.filter (fun x => G x = y)).card ≤ Mb := by
    intro y hy
    rcases Finset.mem_image.mp hy with ⟨x0, hx0, rfl⟩
    have hsep : Metric.IsSeparated ε
        ((hXfin.toFinset.filter (fun x => G x = G x0) : Finset M) : Set M) :=
      (Metric.isSeparated_maximalSeparatedSet (ε := ε) (A := Metric.closedBall o ρ)).subset (by
        intro z hz
        have hz' := Finset.mem_filter.mp (Finset.mem_coe.mp hz)
        exact hXfin.mem_toFinset.mp hz'.1)
    have hsub : ((hXfin.toFinset.filter (fun x => G x = G x0) : Finset M) : Set M) ⊆
        Metric.closedBall (G x0) ε' := by
      intro z hz
      rcases Finset.mem_filter.mp (Finset.mem_coe.mp hz) with ⟨hzX, hzG⟩
      rw [Metric.mem_closedBall, ← hzG]
      exact (hG z (hXsub z hzX)).2
    have h2 := (hsep.encard_le_packingNumber hsub).trans (hMb (G x0))
    rw [Set.encard_coe_eq_coe_finsetCard] at h2
    exact_mod_cast h2
  have hXcard : hXfin.toFinset.card = Packing.packingCount o ε ρ := by
    unfold Packing.packingCount
    have h1 : (hXfin.toFinset.card : ℕ∞) =
        (Metric.maximalSeparatedSet ε (Metric.closedBall o ρ)).encard := by
      rw [← Set.encard_coe_eq_coe_finsetCard, hXfin.coe_toFinset]
    rw [← Metric.encard_maximalSeparatedSet hfinE, ← h1]
    simp
  have hYcard : hYfin.toFinset.card = Packing.packingCount o ε' ρ := by
    unfold Packing.packingCount
    have h1 : (hYfin.toFinset.card : ℕ∞) =
        (Metric.maximalSeparatedSet ε' (Metric.closedBall o ρ)).encard := by
      rw [← Set.encard_coe_eq_coe_finsetCard, hYfin.coe_toFinset]
    rw [← Metric.encard_maximalSeparatedSet hfinE', ← h1]
    simp
  have himg : hXfin.toFinset.image G ⊆ hYfin.toFinset := by
    intro y hy
    rcases Finset.mem_image.mp hy with ⟨x, hx, rfl⟩
    exact hYfin.mem_toFinset.mpr (hG x (hXsub x hx)).1
  calc Packing.packingCount o ε ρ = hXfin.toFinset.card := hXcard.symm
    _ ≤ Mb * (hXfin.toFinset.image G).card := Finset.card_le_mul_card_image _ _ hfib
    _ ≤ Mb * hYfin.toFinset.card := Nat.mul_le_mul_left _ (Finset.card_le_card himg)
    _ = Mb * Packing.packingCount o ε' ρ := by rw [hYcard]

/-- **Bounded geometry closes the scale gap.** If `ε'`-balls pack boundedly
    many points at resolution `ε`, the packing rate at `ε` has the same limit
    as the packing rate at `ε'`. -/
theorem packingRate_scale_invariant [ProperSpace M] {o : M} {ε ε' : ℝ≥0}
    (hε : ε ≠ 0) (hε' : ε' ≠ 0) (hle : ε ≤ ε') {Mb : ℕ}
    (hMb : ∀ x : M, Metric.packingNumber ε (Metric.closedBall x ε') ≤ Mb)
    {h : ℝ} (hpacking : Tendsto (Packing.packingRate o ε') atTop (𝓝 h)) :
    Tendsto (Packing.packingRate o ε) atTop (𝓝 h) := by
  have hlog_nn : ∀ n : ℕ, 0 ≤ Real.log (n : ℝ) := by
    intro n
    rcases Nat.eq_zero_or_pos n with hm | hm
    · simp [hm]
    · exact Real.log_nonneg (by exact_mod_cast hm)
  have hlow : ∀ᶠ ρ : ℝ in atTop, Packing.packingRate o ε' ρ ≤ Packing.packingRate o ε ρ := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with ρ hρ
    unfold Packing.packingRate
    apply div_le_div_of_nonneg_right _ hρ.le
    have hc := packingCount_anti (o := o) hε hε' hle hρ.le
    rcases Nat.eq_zero_or_pos (Packing.packingCount o ε' ρ) with h0 | hpos
    · rw [h0]; simp
      exact hlog_nn _
    · exact Real.log_le_log (by exact_mod_cast hpos) (by exact_mod_cast hc)
  have hup : ∀ᶠ ρ : ℝ in atTop,
      Packing.packingRate o ε ρ ≤ Real.log (Mb : ℝ) / ρ + Packing.packingRate o ε' ρ := by
    filter_upwards [eventually_gt_atTop (0 : ℝ)] with ρ hρ
    unfold Packing.packingRate
    rw [← add_div]
    apply div_le_div_of_nonneg_right _ hρ.le
    have hc := packingCount_le_mul_packingCount (o := o) hε hε' hMb hρ.le
    rcases Nat.eq_zero_or_pos (Packing.packingCount o ε ρ) with h0 | hpos
    · rw [h0]; simp
      linarith [hlog_nn Mb, hlog_nn (Packing.packingCount o ε' ρ)]
    · have hMbpos : 0 < Mb := by
        rcases Nat.eq_zero_or_pos Mb with hm | hm
        · rw [hm, zero_mul] at hc; omega
        · exact hm
      have hP'pos : 0 < Packing.packingCount o ε' ρ := by
        rcases Nat.eq_zero_or_pos (Packing.packingCount o ε' ρ) with hm | hm
        · rw [hm, mul_zero] at hc; omega
        · exact hm
      rw [← Real.log_mul (by exact_mod_cast hMbpos.ne') (by exact_mod_cast hP'pos.ne')]
      apply Real.log_le_log (by exact_mod_cast hpos)
      exact_mod_cast hc
  have hlim : Tendsto (fun ρ : ℝ => Real.log (Mb : ℝ) / ρ + Packing.packingRate o ε' ρ)
      atTop (𝓝 (0 + h)) :=
    (tendsto_const_nhds.div_atTop tendsto_id).add hpacking
  rw [zero_add] at hlim
  exact tendsto_of_tendsto_of_tendsto_of_le_of_le' hpacking hlim hlow hup

/-- The balloon separation as a corollary of the coarse converse: no
    metric-ULF source has a positive relational rate in `B`. -/
theorem balloon_relational_rate_nonpos (q : Distortion) {σ : Source S} (hσ : σ.MetricULF)
    {β : ℝ} (hg : σ.HasGrowth β) {ε : ℝ≥0} {c : ℝ}
    (hr : Represents (hub 0) ε (Relational q) σ c) : β ≤ 0 := by
  have := coarse_packing_converse (ε' := 3) (by norm_num)
    (balloon_coarse_entropy_zero (by norm_num)) q hσ hg hr
  linarith

end ActiveGeometry.Constrained

#print axioms ActiveGeometry.Constrained.census_card_le_coarse_packing
#print axioms ActiveGeometry.Constrained.coarse_packing_converse
#print axioms ActiveGeometry.Constrained.balloon_packingCount_le
#print axioms ActiveGeometry.Constrained.balloon_coarse_entropy_zero
#print axioms ActiveGeometry.Constrained.packingCount_anti
#print axioms ActiveGeometry.Constrained.packingCount_le_mul_packingCount
#print axioms ActiveGeometry.Constrained.packingRate_scale_invariant
#print axioms ActiveGeometry.Constrained.balloon_relational_rate_nonpos
