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

namespace Challenges.Window

open Filter Real
open scoped Topology

/-! ### The symmetric channel and its powers -/

/-- The all-ones matrix on `Fin q`. -/
def allOnes (q : ℕ) : Matrix (Fin q) (Fin q) ℝ := Matrix.of fun _ _ => (1 : ℝ)

theorem allOnes_mul_allOnes (q : ℕ) :
    allOnes q * allOnes q = (q : ℝ) • allOnes q := by
  sorry

/-- The `q`-state symmetric channel with second eigenvalue `lam`. -/
noncomputable def symChannel (q : ℕ) (lam : ℝ) : Matrix (Fin q) (Fin q) ℝ :=
  lam • (1 : Matrix (Fin q) (Fin q) ℝ) + ((1 - lam) / q) • allOnes q

/-- Composition of two symmetric channels is the symmetric channel with the
    product eigenvalue. This is the closure that makes `λ^d` the signal. -/
theorem symChannel_mul (q : ℕ) (hq : (q : ℝ) ≠ 0) (a b : ℝ) :
    symChannel q a * symChannel q b = symChannel q (a * b) := by
  sorry

/-- Powers of the symmetric channel. -/
theorem symChannel_pow (q : ℕ) (hq : (q : ℝ) ≠ 0) (lam : ℝ) (d : ℕ) :
    symChannel q lam ^ d = symChannel q (lam ^ d) := by
  sorry

/-- Two letters at path length `d` agree with probability `λ^d + (1 − λ^d)/q`:
    the diagonal entry of the `d`-fold channel. -/
theorem same_letter_prob (q : ℕ) (hq : (q : ℝ) ≠ 0) (lam : ℝ) (d : ℕ) (i : Fin q) :
    (symChannel q lam ^ d) i i = lam ^ d + (1 - lam ^ d) / q := by
  sorry

/-- The Jukes–Cantor case. -/
theorem same_letter_prob_four (lam : ℝ) (d : ℕ) (i : Fin 4) :
    (symChannel 4 lam ^ d) i i = 1 / 4 + 3 / 4 * lam ^ d := by
  sorry

/-! ### The identity price -/

/-- **Identity costs `O(log N)` sites.** With `N` pairs, each sharing a letter
    with probability at most `p ∈ (0, 1)` per site independently, the union
    bound gives `P(some pair identical on all L sites) ≤ N · p^L`, and this is
    at most `δ` as soon as `L ≥ log(N/δ) / (−log p)`. -/
theorem identity_sites {N δ p : ℝ} (hN : 0 < N) (hδ : 0 < δ) (hp0 : 0 < p) (hp1 : p < 1)
    {L : ℝ} (hL : Real.log (N / δ) / (-Real.log p) ≤ L) :
    N * p ^ L ≤ δ := by
  sorry

/-! ### The Kesten–Stigum line in rate form -/

/-- `b·λ² > 1` with `b = e^{βτ}`, `λ = e^{−ρτ}`, `τ > 0`, is `β > 2ρ`. -/
theorem kestenStigum_iff_rate {β ρ τ : ℝ} (hτ : 0 < τ) :
    1 < Real.exp (β * τ) * Real.exp (-ρ * τ) ^ 2 ↔ 2 * ρ < β := by
  sorry

/-- The signal `e^{(β − 2ρ) t}` diverges above the line … -/
theorem signal_tendsto_atTop {β ρ : ℝ} (h : 2 * ρ < β) :
    Tendsto (fun t : ℝ => Real.exp ((β - 2 * ρ) * t)) atTop atTop := by
  sorry

/-- … and vanishes below it. -/
theorem signal_tendsto_zero {β ρ : ℝ} (h : β < 2 * ρ) :
    Tendsto (fun t : ℝ => Real.exp ((β - 2 * ρ) * t)) atTop (𝓝 0) := by
  sorry

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
  sorry

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
  sorry

theorem pSame_lt_one {ρ ℓ : ℝ} (hρ : 0 < ρ) (hℓ : 0 < ℓ) : pSame ρ ℓ < 1 := by
  sorry

theorem pSame_le_pSame {ρ₁ ρ₂ ℓ : ℝ} (hℓ : 0 ≤ ℓ) (h : ρ₁ ≤ ρ₂) :
    pSame ρ₂ ℓ ≤ pSame ρ₁ ℓ := by
  sorry

/-- The identity edge: `N` sister pairs at path duration `ℓ` stay distinct on
    `L` sites except with probability at most `δ` (union-bound form). -/
def Identified (N δ L ρ ℓ : ℝ) : Prop := N * pSame ρ ℓ ^ L ≤ δ

/-- `identity_sites`, in the clock's terms. -/
theorem identified_of_sites {N δ L ρ ℓ : ℝ} (hN : 0 < N) (hδ : 0 < δ) (hρ : 0 < ρ)
    (hℓ : 0 < ℓ) (hL : Real.log (N / δ) / (-Real.log (pSame ρ ℓ)) ≤ L) :
    Identified N δ L ρ ℓ := by
  sorry

/-- **The identity edge is one-sided.** A faster clock never loses identity. -/
theorem identified_mono {N δ L ℓ ρ₁ ρ₂ : ℝ} (hN : 0 ≤ N) (hL : 0 ≤ L) (hℓ : 0 ≤ ℓ)
    (h : ρ₁ ≤ ρ₂) (hid : Identified N δ L ρ₁ ℓ) : Identified N δ L ρ₂ ℓ := by
  sorry

/-- The genealogy edge for a four-point (distance) reader at depth `t` with
    internal branch `τ` on `L` sites: the expected per-site contrast
    `3/4·e^{−2ρt}(1 − e^{−ρτ})` times `√L` clears the detection constant `κ`. -/
def Readable (L t τ κ ρ : ℝ) : Prop :=
  κ ≤ Real.sqrt L * (3 / 4 * Real.exp (-ρ * (2 * t)) * (1 - Real.exp (-ρ * τ)))

theorem sqrt_pos_of_readable {L t τ κ ρ : ℝ} (hκ : 0 < κ) (h : Readable L t τ κ ρ) :
    0 < Real.sqrt L := by
  sorry

/-- **Erasure edge, as a depth law.** At one rate a distance reader cannot read
    deeper than `log(3√L/(4κ)) / (2ρ)`: logarithmic in the record. -/
theorem readable_depth_le {L t τ κ ρ : ℝ} (hκ : 0 < κ) (hρ : 0 < ρ)
    (h : Readable L t τ κ ρ) :
    t ≤ Real.log (3 * Real.sqrt L / (4 * κ)) / (2 * ρ) := by
  sorry

/-- **Collision edge, for the same reader.** The internal branch must be
    written: `e^{−ρτ} ≤ 1 − 4κ/(3√L)`. -/
theorem readable_branch_lower {L t τ κ ρ : ℝ} (hκ : 0 < κ) (hρ : 0 ≤ ρ) (ht : 0 ≤ t)
    (hτ : 0 ≤ τ) (h : Readable L t τ κ ρ) :
    Real.exp (-ρ * τ) ≤ 1 - 4 * κ / (3 * Real.sqrt L) := by
  sorry

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
  sorry

end Challenges.Window
