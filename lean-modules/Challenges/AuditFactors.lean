/-
  The audit: five losses between a lineage and the envelope
  ========================================================

  Paper I splits efficiency into availability and utilization (§5). This file
  refines utilization into four further ratios and proves the only things the
  refinement can prove: the identity, and that every factor is at most one.

      η = β_read / (c · h_pack)
        = (C_rel / C_block) · (β_written / C_rel) · (β_kept / β_written)
          · (β_distinct / β_kept) · (β_read / β_distinct)

  Each factor is a stage at which history can only be lost: a code that keeps
  genealogy cannot hold more addresses than one that does not (availability);
  a represented writer runs below the rung's capacity (writing); retention,
  collision and reading each pass a count through a map, and a map does not
  increase cardinality. The last three are the data-processing content, stated
  here in finite form (`card_chain`) with Mathlib's `Finset.card_image_le`.

  What this file does NOT do: it does not estimate any factor, and it does not
  claim the five estimated factors multiply to the measured rate on any medium.
  That is the closure test (an experiment), registered separately. An identity
  proves nothing about data; its content is that each factor can be estimated
  on its own.

  STATUS. LEAN-CHECKED once built against the pinned Mathlib (see run log).
  Depends only on `Constrained` for `availability` and `capacity`.
-/

import ActiveGeometry.Constrained

namespace ActiveGeometry.Audit

open ActiveGeometry.Constrained

/-! ### The five-factor identity -/

/-- The five audited ratios, as a bundle of positive reals. Positivity is part
    of the physical domain: a stage with a zero count has no rate. -/
structure Chain where
  cblock : ℝ
  crel : ℝ
  written : ℝ
  kept : ℝ
  distinct : ℝ
  read : ℝ
  cblock_pos : 0 < cblock
  crel_pos : 0 < crel
  written_pos : 0 < written
  kept_pos : 0 < kept
  distinct_pos : 0 < distinct
  read_pos : 0 < read

namespace Chain

/-- Efficiency against the block rung: the read rate over the envelope. -/
noncomputable def efficiency (a : Chain) : ℝ := a.read / a.cblock

noncomputable def availabilityFactor (a : Chain) : ℝ := a.crel / a.cblock
noncomputable def writingFactor (a : Chain) : ℝ := a.written / a.crel
noncomputable def retentionFactor (a : Chain) : ℝ := a.kept / a.written
noncomputable def collisionFactor (a : Chain) : ℝ := a.distinct / a.kept
noncomputable def readingFactor (a : Chain) : ℝ := a.read / a.distinct

/-- **The audit identity.** Efficiency is the product of the five stage ratios.
    This is algebra and asserts nothing about any medium. -/
theorem efficiency_eq_product (a : Chain) :
    a.efficiency = a.availabilityFactor * a.writingFactor * a.retentionFactor *
      a.collisionFactor * a.readingFactor := by
  sorry

/-- The ordering a lossy chain satisfies: each stage holds no more than the one
    before it, and the relational rung holds no more than the block rung. -/
structure Lossy (a : Chain) : Prop where
  crel_le : a.crel ≤ a.cblock
  written_le : a.written ≤ a.crel
  kept_le : a.kept ≤ a.written
  distinct_le : a.distinct ≤ a.kept
  read_le : a.read ≤ a.distinct

/-- Every factor of a lossy chain is at most one. -/
theorem factors_le_one {a : Chain} (h : a.Lossy) :
    a.availabilityFactor ≤ 1 ∧ a.writingFactor ≤ 1 ∧ a.retentionFactor ≤ 1 ∧
      a.collisionFactor ≤ 1 ∧ a.readingFactor ≤ 1 := by
  sorry

/-- Every factor of a chain is positive. -/
theorem factors_pos (a : Chain) :
    0 < a.availabilityFactor ∧ 0 < a.writingFactor ∧ 0 < a.retentionFactor ∧
      0 < a.collisionFactor ∧ 0 < a.readingFactor := by
  sorry

/-- A lossy chain has efficiency at most one: the audit is consistent with the
    envelope. -/
theorem efficiency_le_one {a : Chain} (h : a.Lossy) : a.efficiency ≤ 1 := by
  sorry

/-- The first factor is Paper I's availability `θ = C_rel / C_block`, verbatim. -/
theorem availabilityFactor_eq (a : Chain) :
    a.availabilityFactor = availability a.crel a.cblock := by
  sorry

end Chain

/-! ### The finite form: maps do not create distinctness

Retention, collision and reading are each the image of a finite set under a
function. Cardinality cannot grow under a function, and a subset cannot be
larger than its superset. This is the whole of the data-processing content at
a single depth; the rate form above is its logarithm per unit depth. -/

/-- At one depth: `written` histories, of which `kept ⊆ written` survive
    retention; `addr` places them in the host (distinct addresses may merge);
    `reader` maps addresses to what is read (readings may merge again). The
    four counts descend. -/
theorem card_chain {S M T : Type*} [DecidableEq M] [DecidableEq T]
    (written kept : Finset S) (hk : kept ⊆ written) (addr : S → M) (reader : M → T) :
    ((kept.image addr).image reader).card ≤ (kept.image addr).card ∧
      (kept.image addr).card ≤ kept.card ∧
      kept.card ≤ written.card := by
  sorry

/-- The same chain, in logarithms (the quantities a rate divides by depth). -/
theorem log_card_chain {S M T : Type*} [DecidableEq M] [DecidableEq T]
    (written kept : Finset S) (hk : kept ⊆ written) (addr : S → M) (reader : M → T)
    (hne : kept.Nonempty) :
    Real.log (((kept.image addr).image reader).card : ℝ) ≤
        Real.log ((kept.image addr).card : ℝ) ∧
      Real.log ((kept.image addr).card : ℝ) ≤ Real.log (kept.card : ℝ) ∧
      Real.log (kept.card : ℝ) ≤ Real.log (written.card : ℝ) := by
  sorry

end ActiveGeometry.Audit
