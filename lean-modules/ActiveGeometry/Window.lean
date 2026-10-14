/-
  The window: the erasure side, in the medium's own terms
  =======================================================

  Designed codes can reach the envelope; lineages written by a random process
  keep genealogy only inside a window. This file supplies the three pieces of
  the erasure side that are elementary, and names the one that is not.

  1. `symChannel`: the `q`-state symmetric substitution channel
     `M = λ·I + (1−λ)/q · J`. Its powers close: `M^d = symChannel (λ^d)`, so two
     leaves at path length `d` share a letter with probability
     `λ^d + (1 − λ^d)/q` (`same_letter_prob`). For `q = 4` this is the
     Jukes–Cantor `1/4 + 3/4·λ^d`.

  2. `identity_sites`: the identity price. If each of `N` pairs shares a letter
     with probability at most `p < 1` per site, independently across sites, then
     `L ≥ log(N/δ) / (−log p)` sites leave every pair distinct with probability
     at least `1 − δ`, by the union bound. Identity costs `O(log N)` sites.
     The union bound is the modelling step; the lemma is the real inequality.

  3. `kestenStigum_iff_rate`: the Kesten–Stigum line `b·λ² > 1`, written with
     `b = e^{βτ}` (branching per edge time `τ`) and `λ = e^{−ρτ}` (the
     channel's second eigenvalue), is exactly `β > 2ρ`: the lineage must branch
     faster than twice the rate at which the medium forgets.

  What is NOT proved here: that reconstruction of the root is possible exactly
  above that line. For the symmetric channel this is Kesten–Stigum (1966) and
  Mossel–Peres (2003) above the line, and tightness (no reconstruction below)
  is proved for `q = 2` (Bleher–Ruiz–Zagrebnov 1995; Evans–Kenyon–Peres–Schulman
  2000), claimed for `q = 3` and `q = 4` in the openai/math collection
  (family 229, October 2026; only the supercritical half is formalized there),
  and found numerically for `q = 4` on binary trees in PREREG15b. It enters as
  the named hypothesis `ReconstructionThreshold`, whose shape follows the
  comparator statement `OAI.ThreeState.Reconstructs`: a positive limit of the
  reconstruction advantage.

  STATUS. 1–3 LEAN-CHECKED once built. `ReconstructionThreshold` is a
  hypothesis, never derived.
-/

import Mathlib.Data.Matrix.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic

namespace ActiveGeometry.Window

open Filter Real
open scoped Topology

/-! ### The symmetric channel and its powers -/

/-- The all-ones matrix on `Fin q`. -/
def allOnes (q : ℕ) : Matrix (Fin q) (Fin q) ℝ := Matrix.of fun _ _ => (1 : ℝ)

theorem allOnes_mul_allOnes (q : ℕ) :
    allOnes q * allOnes q = (q : ℝ) • allOnes q := by
  ext i j
  simp [allOnes, Matrix.mul_apply]

/-- The `q`-state symmetric channel with second eigenvalue `lam`. -/
noncomputable def symChannel (q : ℕ) (lam : ℝ) : Matrix (Fin q) (Fin q) ℝ :=
  lam • (1 : Matrix (Fin q) (Fin q) ℝ) + ((1 - lam) / q) • allOnes q

/-- Composition of two symmetric channels is the symmetric channel with the
    product eigenvalue. This is the closure that makes `λ^d` the signal. -/
theorem symChannel_mul (q : ℕ) (hq : (q : ℝ) ≠ 0) (a b : ℝ) :
    symChannel q a * symChannel q b = symChannel q (a * b) := by
  unfold symChannel
  rw [Matrix.add_mul, Matrix.mul_add, Matrix.mul_add]
  simp only [Matrix.smul_mul, Matrix.mul_smul, Matrix.one_mul, Matrix.mul_one, smul_smul,
    allOnes_mul_allOnes]
  match_scalars <;> field_simp <;> ring

/-- Powers of the symmetric channel. -/
theorem symChannel_pow (q : ℕ) (hq : (q : ℝ) ≠ 0) (lam : ℝ) (d : ℕ) :
    symChannel q lam ^ d = symChannel q (lam ^ d) := by
  induction d with
  | zero => simp [symChannel]
  | succ n ih => rw [pow_succ, ih, symChannel_mul q hq, pow_succ]

/-- Two letters at path length `d` agree with probability `λ^d + (1 − λ^d)/q`:
    the diagonal entry of the `d`-fold channel. -/
theorem same_letter_prob (q : ℕ) (hq : (q : ℝ) ≠ 0) (lam : ℝ) (d : ℕ) (i : Fin q) :
    (symChannel q lam ^ d) i i = lam ^ d + (1 - lam ^ d) / q := by
  rw [symChannel_pow q hq]
  simp [symChannel, allOnes, Matrix.add_apply, Matrix.smul_apply]

/-- The Jukes–Cantor case. -/
theorem same_letter_prob_four (lam : ℝ) (d : ℕ) (i : Fin 4) :
    (symChannel 4 lam ^ d) i i = 1 / 4 + 3 / 4 * lam ^ d := by
  rw [same_letter_prob 4 (by norm_num) lam d i]
  push_cast
  ring

/-! ### The identity price -/

/-- **Identity costs `O(log N)` sites.** With `N` pairs, each sharing a letter
    with probability at most `p ∈ (0, 1)` per site independently, the union
    bound gives `P(some pair identical on all L sites) ≤ N · p^L`, and this is
    at most `δ` as soon as `L ≥ log(N/δ) / (−log p)`. -/
theorem identity_sites {N δ p : ℝ} (hN : 0 < N) (hδ : 0 < δ) (hp0 : 0 < p) (hp1 : p < 1)
    {L : ℝ} (hL : Real.log (N / δ) / (-Real.log p) ≤ L) :
    N * p ^ L ≤ δ := by
  have hlogp : Real.log p < 0 := Real.log_neg hp0 hp1
  have hneg : 0 < -Real.log p := by linarith
  have h1 : Real.log (N / δ) ≤ L * (-Real.log p) := by
    rw [div_le_iff₀ hneg] at hL
    exact hL
  have h2 : Real.log N - Real.log δ ≤ -(L * Real.log p) := by
    rw [Real.log_div hN.ne' hδ.ne'] at h1
    linarith
  have h3 : Real.log N + L * Real.log p ≤ Real.log δ := by linarith
  have h4 : Real.log (N * p ^ L) ≤ Real.log δ := by
    rw [Real.log_mul hN.ne' (Real.rpow_pos_of_pos hp0 L).ne', Real.log_rpow hp0]
    exact h3
  exact (Real.log_le_log_iff (mul_pos hN (Real.rpow_pos_of_pos hp0 L)) hδ).1 h4

/-! ### The Kesten–Stigum line in rate form -/

/-- `b·λ² > 1` with `b = e^{βτ}`, `λ = e^{−ρτ}`, `τ > 0`, is `β > 2ρ`. -/
theorem kestenStigum_iff_rate {β ρ τ : ℝ} (hτ : 0 < τ) :
    1 < Real.exp (β * τ) * Real.exp (-ρ * τ) ^ 2 ↔ 2 * ρ < β := by
  have hsq : Real.exp (-ρ * τ) ^ 2 = Real.exp (2 * (-ρ * τ)) := by
    rw [← Real.exp_nat_mul]; push_cast; ring_nf
  rw [hsq, ← Real.exp_add, ← Real.exp_zero, Real.exp_lt_exp]
  constructor
  · intro h
    nlinarith
  · intro h
    nlinarith

/-- The signal `e^{(β − 2ρ) t}` diverges above the line … -/
theorem signal_tendsto_atTop {β ρ : ℝ} (h : 2 * ρ < β) :
    Tendsto (fun t : ℝ => Real.exp ((β - 2 * ρ) * t)) atTop atTop := by
  have hpos : 0 < β - 2 * ρ := by linarith
  exact Real.tendsto_exp_atTop.comp (tendsto_id.const_mul_atTop hpos)

/-- … and vanishes below it. -/
theorem signal_tendsto_zero {β ρ : ℝ} (h : β < 2 * ρ) :
    Tendsto (fun t : ℝ => Real.exp ((β - 2 * ρ) * t)) atTop (𝓝 0) := by
  have hneg : 0 < 2 * ρ - β := by linarith
  have h1 : Tendsto (fun t : ℝ => (2 * ρ - β) * t) atTop atTop :=
    tendsto_id.const_mul_atTop hneg
  have h2 : Tendsto (fun t : ℝ => -((2 * ρ - β) * t)) atTop atBot :=
    tendsto_neg_atTop_atBot.comp h1
  have h3 : Tendsto (fun t : ℝ => Real.exp (-((2 * ρ - β) * t))) atTop (𝓝 0) :=
    Real.tendsto_exp_atBot.comp h2
  refine h3.congr' ?_
  filter_upwards with t
  ring_nf

/-! ### The named hypothesis: reconstruction is possible exactly above the line

Shape follows `OAI.ThreeState.Reconstructs` (openai/math, family 229): a
sequence of reconstruction advantages has a positive limit. -/

/-- A sequence of root-reconstruction advantages converges to a positive limit. -/
def Reconstructs (a : ℕ → ℝ) : Prop :=
  ∃ L : ℝ, 0 < L ∧ Tendsto a atTop (𝓝 L)

/-- **Hypothesis, never derived.** For the `q`-state symmetric channel on the
    `b`-ary tree, the advantage sequence of the optimal (Bayes) root estimator
    reconstructs exactly when `b·λ² > 1`. Proved for `q = 2`; claimed for
    `q = 3, 4` (family 229, supercritical half formalized); numerical support
    for `q = 4`, `b = 2` in PREREG15b. -/
structure ReconstructionThreshold (q b : ℕ) where
  advantage : ℝ → ℕ → ℝ
  tight : ∀ lam : ℝ, 0 ≤ lam → lam ≤ 1 →
    (1 < (b : ℝ) * lam ^ 2 ↔ Reconstructs (advantage lam))

/-- Under the hypothesis, the genealogy horizon in rate form: with
    `b = e^{βτ}` lineages per edge and eigenvalue `λ = e^{−ρτ}`, the root is
    reconstructible exactly when `β > 2ρ`. -/
theorem horizon_of_threshold {q b : ℕ} (H : ReconstructionThreshold q b)
    {β ρ τ : ℝ} (hτ : 0 < τ) (hρ : 0 ≤ ρ)
    (hb : (b : ℝ) = Real.exp (β * τ)) :
    (2 * ρ < β ↔ Reconstructs (H.advantage (Real.exp (-ρ * τ)))) := by
  have h0 : 0 ≤ Real.exp (-ρ * τ) := (Real.exp_pos _).le
  have h1 : Real.exp (-ρ * τ) ≤ 1 := by
    rw [← Real.exp_zero, Real.exp_le_exp]
    nlinarith
  rw [← H.tight _ h0 h1, hb]
  exact (kestenStigum_iff_rate hτ).symm

/-! ### The window of a distance reader: both edges from one inequality

The companion's window has two exits, and both are failures of the same lower
bound, "histories that are far apart stay far apart in the record", at two
depths: sisters (identity) and a deep split (genealogy). This section states
the two edges for a four-point (distance) reader on a Jukes–Cantor tape at one
rate `ρ` and proves that a clock which reads depth `t` lies in an explicit
interval. The identity edge is one-sided (`identified_mono`): a faster clock
never loses identity. The genealogy edge is two-sided in `ρ` for one reason on
each side: too slow and the internal branch is not written
(`readable_branch_lower`), too fast and the deep contrast saturates
(`readable_depth_le`, the logarithmic depth law). The second-moment
Kesten–Stigum line above is the ceiling for the best reader and is not
derived from this inequality. -/

/-- Jukes–Cantor same-letter probability at path duration `ℓ` when the channel
    eigenvalue decays at rate `ρ`: `1/4 + 3/4·e^{−ρℓ}`. -/
noncomputable def pSame (ρ ℓ : ℝ) : ℝ := 1 / 4 + 3 / 4 * Real.exp (-ρ * ℓ)

theorem pSame_pos (ρ ℓ : ℝ) : 0 < pSame ρ ℓ := by
  unfold pSame; positivity

theorem pSame_lt_one {ρ ℓ : ℝ} (hρ : 0 < ρ) (hℓ : 0 < ℓ) : pSame ρ ℓ < 1 := by
  unfold pSame
  have : Real.exp (-ρ * ℓ) < Real.exp 0 := Real.exp_lt_exp.mpr (by nlinarith)
  rw [Real.exp_zero] at this
  linarith

theorem pSame_le_pSame {ρ₁ ρ₂ ℓ : ℝ} (hℓ : 0 ≤ ℓ) (h : ρ₁ ≤ ρ₂) :
    pSame ρ₂ ℓ ≤ pSame ρ₁ ℓ := by
  unfold pSame
  have : Real.exp (-ρ₂ * ℓ) ≤ Real.exp (-ρ₁ * ℓ) := by
    apply Real.exp_le_exp.mpr; nlinarith
  linarith

/-- The identity edge: `N` sister pairs at path duration `ℓ` stay distinct on
    `L` sites except with probability at most `δ` (union-bound form). -/
def Identified (N δ L ρ ℓ : ℝ) : Prop := N * pSame ρ ℓ ^ L ≤ δ

/-- `identity_sites`, in the clock's terms. -/
theorem identified_of_sites {N δ L ρ ℓ : ℝ} (hN : 0 < N) (hδ : 0 < δ) (hρ : 0 < ρ)
    (hℓ : 0 < ℓ) (hL : Real.log (N / δ) / (-Real.log (pSame ρ ℓ)) ≤ L) :
    Identified N δ L ρ ℓ :=
  identity_sites hN hδ (pSame_pos ρ ℓ) (pSame_lt_one hρ hℓ) hL

/-- **The identity edge is one-sided.** A faster clock never loses identity. -/
theorem identified_mono {N δ L ℓ ρ₁ ρ₂ : ℝ} (hN : 0 ≤ N) (hL : 0 ≤ L) (hℓ : 0 ≤ ℓ)
    (h : ρ₁ ≤ ρ₂) (hid : Identified N δ L ρ₁ ℓ) : Identified N δ L ρ₂ ℓ := by
  unfold Identified at *
  have hp := pSame_le_pSame hℓ h
  have hpow := Real.rpow_le_rpow (pSame_pos ρ₂ ℓ).le hp hL
  calc N * pSame ρ₂ ℓ ^ L ≤ N * pSame ρ₁ ℓ ^ L := mul_le_mul_of_nonneg_left hpow hN
    _ ≤ δ := hid

/-- The genealogy edge for a four-point (distance) reader at depth `t` with
    internal branch `τ` on `L` sites: the expected per-site contrast
    `3/4·e^{−2ρt}(1 − e^{−ρτ})` times `√L` clears the detection constant `κ`. -/
def Readable (L t τ κ ρ : ℝ) : Prop :=
  κ ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t)) * (1 - Real.exp (-ρ * τ)))

theorem sqrt_pos_of_readable {L t τ κ ρ : ℝ} (hκ : 0 < κ) (h : Readable L t τ κ ρ) :
    0 < Real.sqrt L := by
  by_contra hs
  have h0 : Real.sqrt L = 0 := le_antisymm (not_lt.mp hs) (Real.sqrt_nonneg L)
  unfold Readable at h
  rw [h0, zero_mul] at h
  linarith

/-- **Erasure edge, as a depth law.** At one rate a distance reader cannot read
    deeper than `log(3√L/(4κ)) / (2ρ)`: logarithmic in the record. -/
theorem readable_depth_le {L t τ κ ρ : ℝ} (hκ : 0 < κ) (hρ : 0 < ρ)
    (h : Readable L t τ κ ρ) :
    t ≤ Real.log (3 * Real.sqrt L / (4 * κ)) / (2 * ρ) := by
  have hs := sqrt_pos_of_readable hκ h
  unfold Readable at h
  have h1 : 1 - Real.exp (-ρ * τ) ≤ 1 := by linarith [Real.exp_pos (-ρ * τ)]
  have hpos : 0 ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t))) := by positivity
  have h2 : κ ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t))) := by
    calc κ ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t)) * (1 - Real.exp (-ρ * τ))) := h
      _ = Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t))) * (1 - Real.exp (-ρ * τ)) := by ring
      _ ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t))) * 1 :=
          mul_le_mul_of_nonneg_left h1 hpos
      _ = Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t))) := mul_one _
  have h3 : 4 * κ / (3 * Real.sqrt L) ≤ Real.exp (-ρ * (2 * t)) := by
    rw [div_le_iff₀ (by positivity)]
    nlinarith [h2]
  have h4 : Real.log (4 * κ / (3 * Real.sqrt L)) ≤ -ρ * (2 * t) := by
    have := Real.log_le_log (by positivity) h3
    rwa [Real.log_exp] at this
  have h5 : Real.log (4 * κ / (3 * Real.sqrt L)) =
      -Real.log (3 * Real.sqrt L / (4 * κ)) := by
    rw [← Real.log_inv, inv_div]
  rw [h5] at h4
  rw [le_div_iff₀ (by positivity)]
  linarith

/-- **Collision edge, for the same reader.** The internal branch must be
    written: `e^{−ρτ} ≤ 1 − 4κ/(3√L)`. -/
theorem readable_branch_lower {L t τ κ ρ : ℝ} (hκ : 0 < κ) (hρ : 0 ≤ ρ) (ht : 0 ≤ t)
    (hτ : 0 ≤ τ) (h : Readable L t τ κ ρ) :
    Real.exp (-ρ * τ) ≤ 1 - 4 * κ / (3 * Real.sqrt L) := by
  have hs := sqrt_pos_of_readable hκ h
  unfold Readable at h
  have he : Real.exp (-ρ * (2 * t)) ≤ 1 := by
    rw [Real.exp_le_one_iff]; nlinarith
  have hb : 0 ≤ 1 - Real.exp (-ρ * τ) := by
    have : Real.exp (-ρ * τ) ≤ 1 := by rw [Real.exp_le_one_iff]; nlinarith
    linarith
  have hnn : 0 ≤ Real.sqrt L * (3 / 4) * (1 - Real.exp (-ρ * τ)) :=
    mul_nonneg (mul_nonneg (Real.sqrt_nonneg L) (by norm_num)) hb
  have h2 : κ ≤ Real.sqrt L * (3 / 4) * (1 - Real.exp (-ρ * τ)) := by
    calc κ ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t)) * (1 - Real.exp (-ρ * τ))) := h
      _ = Real.sqrt L * (3 / 4) * (1 - Real.exp (-ρ * τ)) * Real.exp (-ρ * (2 * t)) := by ring
      _ ≤ Real.sqrt L * (3 / 4) * (1 - Real.exp (-ρ * τ)) * 1 :=
          mul_le_mul_of_nonneg_left he hnn
      _ = Real.sqrt L * (3 / 4) * (1 - Real.exp (-ρ * τ)) := mul_one _
  have h3 : 4 * κ / (3 * Real.sqrt L) ≤ 1 - Real.exp (-ρ * τ) := by
    rw [div_le_iff₀ (by positivity)]
    nlinarith [h2]
  linarith

/-- **The window.** A clock at which a distance reader reads depth `t` with
    internal branch `τ` lies in an explicit interval: at least enough writing
    on the internal branch, at most the saturation rate for that depth. With
    `identified_mono`, both edges of the companion's window are bounds on one
    quantity, the written contrast on the shortest branch that must be read,
    against the saturation of the deepest. -/
theorem window {L t τ κ ρ : ℝ} (hκ : 0 < κ) (hρ : 0 < ρ) (ht : 0 < t) (hτ : 0 < τ)
    (h : Readable L t τ κ ρ) :
    -Real.log (1 - 4 * κ / (3 * Real.sqrt L)) / τ ≤ ρ ∧
      ρ ≤ Real.log (3 * Real.sqrt L / (4 * κ)) / (2 * t) := by
  constructor
  · have hb := readable_branch_lower hκ hρ.le ht.le hτ.le h
    have hlog := Real.log_le_log (Real.exp_pos _) hb
    rw [Real.log_exp] at hlog
    rw [div_le_iff₀ hτ]
    linarith
  · have hd := readable_depth_le hκ hρ h
    rw [le_div_iff₀ (by positivity)] at hd ⊢
    linarith

end ActiveGeometry.Window
