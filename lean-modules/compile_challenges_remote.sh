#!/bin/bash
# LEGACY PATH. See compile_remote.sh; the build from this repository alone is `lake build Challenges`
# in lean-modules/, run and checked by `lean-modules/ci.sh`.
#
# Type-check challenge modules (statements with `sorry`) against the pinned library on biosphereatlas.
# Usage: compile_challenges_remote.sh <Module> [<Module> ...]   (files in /fast/scratch_lean2/new_modules/Challenges/)
set -u
cd /fast/scratch_lean2/addressability-limit-main/theory/lean || exit 1
export PATH=/fast/scratch_lean2/elan/bin:$PATH ELAN_HOME=/fast/scratch_lean2/elan
mkdir -p Challenges
for M in "$@"; do
  cp "/fast/scratch_lean2/new_modules/Challenges/$M.lean" "Challenges/$M.lean"
  echo "== challenge $M"
  nice lake env lean "Challenges/$M.lean" 2>&1 | grep -v "declaration uses 'sorry'" | grep -v '^$' | head -30
  echo "EXIT ${PIPESTATUS[0]}"
done
