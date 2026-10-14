#!/bin/bash
cd /fast/scratch_lean2/addressability-limit-main/theory/lean/.lake/packages/mathlib/Mathlib || exit 1
echo "== IsCover / maximalSeparatedSet"
grep -n "def IsCover\|def maximalSeparatedSet\|lemma isCover_maximalSeparatedSet\|lemma encard_maximalSeparatedSet\|lemma maximalSeparatedSet_subset\|lemma isSeparated_maximalSeparatedSet\|theorem isCover_iff\|lemma IsCover\b" Topology/MetricSpace/CoveringNumbers.lean | head
sed -n 60,78p Topology/MetricSpace/CoveringNumbers.lean
sed -n 262,320p Topology/MetricSpace/CoveringNumbers.lean
echo "== log/x limits"
grep -rn "theorem tendsto_pow_log_div_mul_add_atTop\|theorem tendsto_log_div" Analysis/SpecialFunctions/Log/ | head -3
grep -rn "theorem tendsto_const_div_atTop_nhds_zero_nat" Analysis/ Topology/ Order/ | head -2
echo "== Set.Finite.toFinset mem"; grep -rn "theorem Finite.mem_toFinset\b" Data/Set/Finite/Basic.lean | head -2
