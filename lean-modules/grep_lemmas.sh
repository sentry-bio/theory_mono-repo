#!/bin/bash
# Look up Mathlib lemma names/signatures for BalloonPacking.lean (run on biosphereatlas).
cd /fast/scratch_lean2/addressability-limit-main/theory/lean/.lake/packages/mathlib/Mathlib || exit 1
echo "== IsSeparated"; grep -n "theorem\|lemma" Topology/MetricSpace/MetricSeparated.lean | head -30
echo "== proper / compact"; grep -rn "theorem properSpace_of_compact_closedBall_of_le\|theorem Set.Finite.isCompact\|closedBall_subset_closedBall'" Topology/MetricSpace/ Topology/Compactness/ 2>/dev/null | head -6
echo "== two_pow"; grep -rn "lt_two_pow_self" Data/Nat/Defs.lean Data/Nat/Basic.lean Algebra/Order/ 2>/dev/null | grep "theorem\|lemma" | head -3
echo "== limits"; grep -rn "theorem tendsto_inv_atTop_zero\b\|theorem tendsto_of_tendsto_of_tendsto_of_le_of_le'" Analysis/ Order/ Topology/ 2>/dev/null | head -4
echo "== encard"; grep -rn "encard_coe_eq_coe_finsetCard\|theorem encard_le_encard\|theorem encard_mono\|lemma encard_le_encard\|Finite.encard_lt_top\|encard_ne_top_iff\|theorem encard_lt_top_iff" Data/Set/Card.lean | head -8
echo "== ENat"; grep -rn "toNat_le_toNat" Data/ENat/Basic.lean Data/ENat/Lemmas.lean 2>/dev/null | head -2
echo "== biUnion"; grep -rn "theorem card_biUnion_le\b" Data/Finset/ Algebra/BigOperators/ 2>/dev/null | head -2
echo "== floor"; grep -rn "theorem lt_floor_add_one\|theorem floor_le\b\|theorem le_floor_iff\b\|theorem floor_pos\b\|theorem one_le_floor_iff\|theorem lt_floor_add_one\b" Algebra/Order/Floor/Defs.lean Algebra/Order/Floor/Semiring.lean Algebra/Order/Floor/Ring.lean 2>/dev/null | head -8
echo "== finite_toSet"; grep -rn "theorem finite_toSet" Data/Set/Finite/Basic.lean Data/Finset/ 2>/dev/null | head -2
echo "== packingNumber"; sed -n 136,152p Topology/MetricSpace/CoveringNumbers.lean
echo "== edist"; grep -rn "theorem edist_dist\b\|theorem edist_lt_ofReal\|theorem ofReal_lt_ofReal_iff\b" Topology/MetricSpace/Pseudo/Defs.lean Topology/MetricSpace/Pseudo/Basic.lean Data/ENNReal/ 2>/dev/null | head -4
echo "== HasFinitePacking users"; grep -n "hasFinitePacking_of_properSpace" -A 12 /fast/scratch_lean2/addressability-limit-main/theory/lean/ActiveGeometry/Packing.lean | head -30
echo "== Rates_bddAbove"; sed -n 424,436p /fast/scratch_lean2/addressability-limit-main/theory/lean/ActiveGeometry/Constrained.lean
echo "== capacity_block_eq_packing"; grep -n "capacity_block_eq_packing\|theorem capacity_eq_packing_of_endpoint_achievable" -A 8 /fast/scratch_lean2/addressability-limit-main/theory/lean/ActiveGeometry/Constrained.lean | head -40
