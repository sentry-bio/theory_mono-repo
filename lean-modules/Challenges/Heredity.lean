/-
  Challenge module for `ActiveGeometry.Heredity` (room of compositions): the same definitions and theorem
  statements, every proof replaced by `sorry`. Namespace `Challenges.Heredity`.
-/
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Sym.Card
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Tactic

namespace Challenges.Heredity

open Finset Filter

variable {α : Type*} [Fintype α] [DecidableEq α]

omit [DecidableEq α] in
/-- Ordered carriers of length `L` number exactly `|α|^L`. -/
theorem card_carrier (L : ℕ) : Fintype.card (Fin L → α) = Fintype.card α ^ L := by
  sorry

/-- The window of length `k` of `s` starting at position `i`. -/
def window {L : ℕ} (k : ℕ) (s : Fin L → α) (i : Fin (L + 1 - k)) : Fin k → α :=
  fun j => s ⟨i.1 + j.1, by have := i.2; have := j.2; omega⟩

/-- The `k`-mer spectrum of `s`: the number of windows equal to each word. -/
def spectrum {L : ℕ} (k : ℕ) (s : Fin L → α) (w : Fin k → α) : ℕ :=
  (univ.filter fun i => window k s i = w).card

omit [Fintype α] in
theorem spectrum_le {L : ℕ} (k : ℕ) (s : Fin L → α) (w : Fin k → α) :
    spectrum k s w ≤ L + 1 := by
  sorry

/-- The spectrum with values bounded in `Fin (L + 2)`. -/
def spectrumFin {L : ℕ} (k : ℕ) (s : Fin L → α) : (Fin k → α) → Fin (L + 2) :=
  fun w => ⟨spectrum k s w, Nat.lt_succ_of_le (spectrum_le k s w)⟩

/-- **Theorem 1 (room of compositions).** -/
theorem card_spectra_le (L k : ℕ) :
    (univ.image (spectrum (α := α) (L := L) k)).card ≤ (L + 2) ^ (Fintype.card α ^ k) := by
  sorry

/-- Exact room of single-letter composition: multisets of size `L`. -/
theorem card_composition (L : ℕ) :
    Fintype.card (Sym α L) = (Fintype.card α + L - 1).choose L := by
  sorry

/-- **Addressability form, composition.** -/
theorem histories_le_composition_room {ι : Type*} [Fintype ι] (L k : ℕ)
    (code : ι → Fin L → α) (hdist : Function.Injective fun i => spectrum k (code i)) :
    Fintype.card ι ≤ (L + 2) ^ (Fintype.card α ^ k) := by
  sorry

omit [DecidableEq α] in
/-- **Addressability form, order.** -/
theorem histories_le_sequence_room {ι : Type*} [Fintype ι] (L : ℕ)
    (code : ι → Fin L → α) (hdist : Function.Injective code) :
    Fintype.card ι ≤ Fintype.card α ^ L := by
  sorry

/-- **Limited heredity (finite form).** -/
theorem spectrum_not_injective (L k : ℕ)
    (h : (L + 2) ^ (Fintype.card α ^ k) < Fintype.card α ^ L) :
    ¬ Function.Injective (spectrum (α := α) (L := L) k) := by
  sorry

/-- Every fixed polynomial room is eventually exceeded by an exponential one. -/
theorem eventually_poly_lt_exp (m : ℕ) {a : ℕ} (ha : 2 ≤ a) :
    ∀ᶠ L : ℕ in atTop, (L + 2) ^ m < a ^ L := by
  sorry

/-- **Limited heredity (asymptotic form).** -/
theorem eventually_spectrum_not_injective (k : ℕ) (ha : 2 ≤ Fintype.card α) :
    ∀ᶠ L in atTop, ¬ Function.Injective (spectrum (α := α) (L := L) k) := by
  sorry

end Challenges.Heredity
