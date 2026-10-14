#!/bin/bash
cd /fast/scratch_lean2/addressability-limit-main/theory/lean/.lake/packages/mathlib/Mathlib || exit 1
grep -n "lemma packingNumber_anti\|lemma packingNumber_mono\|lemma IsSeparated.anti\|lemma packingNumber_le_packingNumber" Topology/MetricSpace/CoveringNumbers.lean Topology/MetricSpace/MetricSeparated.lean | head
sed -n "$(grep -n 'lemma packingNumber_anti' Topology/MetricSpace/CoveringNumbers.lean | cut -d: -f1),+4p" Topology/MetricSpace/CoveringNumbers.lean
grep -n "closedBall_subset_closedBall\b" Topology/MetricSpace/Pseudo/Defs.lean | head -2
