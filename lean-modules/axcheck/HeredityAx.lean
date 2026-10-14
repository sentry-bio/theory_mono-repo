import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Sym.Card
import Mathlib.Analysis.SpecificLimits.Normed
import Mathlib.Tactic

/-!
# Room of hereditary carriers: order versus composition

Theorem 1 of the heredity program. A carrier is a string of length `L` over a
finite alphabet `α`. Read as an ordered string it has `|α|^L` states. Read
through its `k`-mer spectrum (how often each word of length `k` occurs) it has
at most `(L+2)^(|α|^k)` distinguishable states, a polynomial in `L`.

Consequences, all proved below:

* histories that a code tells apart only by composition are bounded by the
  compositional room, while ordered codes reach `|α|^L`;
* once the ordered room exceeds the compositional room, the spectrum map is
  not injective: composition cannot tell all carriers apart;
* for every fixed `k` and every alphabet with at least two letters, this happens
  for all sufficiently long carriers.

This file only counts states. Dynamics (what a mutational process retains) and
estimator-level statements are outside it.
-/

namespace ActiveGeometry.Heredity

open Finset Filter

variable {α : Type*} [Fintype α] [DecidableEq α]

omit [DecidableEq α] in
/-- Ordered carriers of length `L` number exactly `|α|^L`. -/
theorem card_carrier (L : ℕ) : Fintype.card (Fin L → α) = Fintype.card α ^ L := by
  simp

/-- The window of length `k` of `s` starting at position `i`. -/
def window {L : ℕ} (k : ℕ) (s : Fin L → α) (i : Fin (L + 1 - k)) : Fin k → α :=
  fun j => s ⟨i.1 + j.1, by have := i.2; have := j.2; omega⟩

/-- The `k`-mer spectrum of `s`: the number of windows equal to each word. -/
def spectrum {L : ℕ} (k : ℕ) (s : Fin L → α) (w : Fin k → α) : ℕ :=
  (univ.filter fun i => window k s i = w).card

omit [Fintype α] in
theorem spectrum_le {L : ℕ} (k : ℕ) (s : Fin L → α) (w : Fin k → α) :
    spectrum k s w ≤ L + 1 := by
  unfold spectrum
  calc (univ.filter fun i => window k s i = w).card
      ≤ (univ : Finset (Fin (L + 1 - k))).card := card_filter_le _ _
    _ = L + 1 - k := by simp
    _ ≤ L + 1 := Nat.sub_le _ _

/-- The spectrum with values bounded in `Fin (L + 2)`. -/
def spectrumFin {L : ℕ} (k : ℕ) (s : Fin L → α) : (Fin k → α) → Fin (L + 2) :=
  fun w => ⟨spectrum k s w, Nat.lt_succ_of_le (spectrum_le k s w)⟩

/-- **Theorem 1 (room of compositions).** Carriers of length `L` have at most
    `(L + 2)^(|α|^k)` distinct `k`-mer spectra. -/
theorem card_spectra_le (L k : ℕ) :
    (univ.image (spectrum (α := α) (L := L) k)).card ≤ (L + 2) ^ (Fintype.card α ^ k) := by
  have hsub : univ.image (spectrum (α := α) (L := L) k) ⊆
      univ.image (fun h : (Fin k → α) → Fin (L + 2) => fun w => (h w : ℕ)) := by
    intro f hf
    simp only [mem_image, mem_univ, true_and] at hf ⊢
    obtain ⟨s, rfl⟩ := hf
    exact ⟨spectrumFin k s, rfl⟩
  calc (univ.image (spectrum (α := α) (L := L) k)).card
      ≤ (univ.image (fun h : (Fin k → α) → Fin (L + 2) => fun w => (h w : ℕ))).card :=
        card_le_card hsub
    _ ≤ (univ : Finset ((Fin k → α) → Fin (L + 2))).card := card_image_le
    _ = (L + 2) ^ (Fintype.card α ^ k) := by simp

/-- Exact room of single-letter composition: multisets of size `L`. -/
theorem card_composition (L : ℕ) :
    Fintype.card (Sym α L) = (Fintype.card α + L - 1).choose L :=
  Sym.card_sym_eq_choose L

/-- **Addressability form, composition.** Histories that a code distinguishes only
    through the `k`-mer spectra of their carriers are bounded by the compositional room. -/
theorem histories_le_composition_room {ι : Type*} [Fintype ι] (L k : ℕ)
    (code : ι → Fin L → α) (hdist : Function.Injective fun i => spectrum k (code i)) :
    Fintype.card ι ≤ (L + 2) ^ (Fintype.card α ^ k) := by
  calc Fintype.card ι = (univ.image fun i => spectrum k (code i)).card := by
        rw [card_image_of_injective _ hdist, card_univ]
    _ ≤ (univ.image (spectrum (α := α) (L := L) k)).card := by
        apply card_le_card
        intro f hf
        simp only [mem_image, mem_univ, true_and] at hf ⊢
        obtain ⟨i, rfl⟩ := hf
        exact ⟨code i, rfl⟩
    _ ≤ _ := card_spectra_le L k

omit [DecidableEq α] in
/-- **Addressability form, order.** Codes that distinguish histories by the ordered
    carrier are bounded by `|α|^L`, and `card_carrier` shows the bound is attained. -/
theorem histories_le_sequence_room {ι : Type*} [Fintype ι] (L : ℕ)
    (code : ι → Fin L → α) (hdist : Function.Injective code) :
    Fintype.card ι ≤ Fintype.card α ^ L := by
  simpa using Fintype.card_le_of_injective code hdist

/-- **Limited heredity (finite form).** Once the ordered room exceeds the
    compositional room, composition cannot tell all carriers apart. -/
theorem spectrum_not_injective (L k : ℕ)
    (h : (L + 2) ^ (Fintype.card α ^ k) < Fintype.card α ^ L) :
    ¬ Function.Injective (spectrum (α := α) (L := L) k) := by
  intro hinj
  have hle := histories_le_composition_room (ι := Fin L → α) L k (fun s => s) hinj
  rw [card_carrier] at hle
  exact absurd hle (not_le.mpr h)

/-- Every fixed polynomial room is eventually exceeded by an exponential one. -/
theorem eventually_poly_lt_exp (m : ℕ) {a : ℕ} (ha : 2 ≤ a) :
    ∀ᶠ L : ℕ in atTop, (L + 2) ^ m < a ^ L := by
  have hr : (1 : ℝ) < a := by exact_mod_cast (by omega : 1 < a)
  have ho := isLittleO_pow_const_const_pow_of_one_lt (R := ℝ) m hr
  have hc : (0 : ℝ) < 1 / (2 : ℝ) ^ (m + 1) := by positivity
  filter_upwards [ho.def hc, eventually_ge_atTop 2] with L hL h2
  have hL' : (L : ℝ) ^ m ≤ 1 / (2 : ℝ) ^ (m + 1) * (a : ℝ) ^ L := by
    simpa [Real.norm_eq_abs, abs_of_nonneg, pow_nonneg] using hL
  have h2' : (2 : ℝ) ≤ L := by exact_mod_cast h2
  have hapos : (0 : ℝ) < (a : ℝ) ^ L := by positivity
  have key : ((L : ℝ) + 2) ^ m < (a : ℝ) ^ L := by
    calc ((L : ℝ) + 2) ^ m ≤ ((2 : ℝ) * L) ^ m := by gcongr; linarith
      _ = (2 : ℝ) ^ m * (L : ℝ) ^ m := mul_pow _ _ _
      _ ≤ (2 : ℝ) ^ m * (1 / (2 : ℝ) ^ (m + 1) * (a : ℝ) ^ L) := by gcongr
      _ = (a : ℝ) ^ L / 2 := by rw [pow_succ]; field_simp
      _ < (a : ℝ) ^ L := by linarith
  exact_mod_cast key

/-- **Limited heredity (asymptotic form).** For every fixed word length `k` and any
    alphabet with at least two letters, all sufficiently long carriers include pairs
    with identical `k`-mer spectra. -/
theorem eventually_spectrum_not_injective (k : ℕ) (ha : 2 ≤ Fintype.card α) :
    ∀ᶠ L in atTop, ¬ Function.Injective (spectrum (α := α) (L := L) k) := by
  filter_upwards [eventually_poly_lt_exp (Fintype.card α ^ k) ha] with L hL
  exact spectrum_not_injective L k hL

end ActiveGeometry.Heredity

#print axioms ActiveGeometry.Heredity.card_carrier
#print axioms ActiveGeometry.Heredity.spectrum_le
#print axioms ActiveGeometry.Heredity.card_spectra_le
#print axioms ActiveGeometry.Heredity.card_composition
#print axioms ActiveGeometry.Heredity.histories_le_composition_room
#print axioms ActiveGeometry.Heredity.histories_le_sequence_room
#print axioms ActiveGeometry.Heredity.spectrum_not_injective
#print axioms ActiveGeometry.Heredity.eventually_poly_lt_exp
#print axioms ActiveGeometry.Heredity.eventually_spectrum_not_injective
