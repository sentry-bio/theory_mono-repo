#!/bin/bash
# LEGACY PATH. This script compiled the modules on the team's build host against a kernel checkout there,
# and cannot run anywhere else. The build from this repository alone is `lake build` in lean-modules/
# (lakefile.toml, lean-toolchain) and `lean-modules/ci.sh`, which is what CI runs. Kept unchanged below
# as the record of how the modules were first compiled.
#
# Compile one new module (and optionally its axiom-check file) against the pinned library on biosphereatlas.
# Usage: compile_remote.sh <Module>   (expects /fast/scratch_lean2/new_modules/<Module>.lean and optional <Module>Ax.lean)
set -u
M="$1"
cd /fast/scratch_lean2/addressability-limit-main/theory/lean || exit 1
export PATH=/fast/scratch_lean2/elan/bin:$PATH ELAN_HOME=/fast/scratch_lean2/elan
cp "/fast/scratch_lean2/new_modules/$M.lean" "ActiveGeometry/$M.lean"
echo "== lake build ActiveGeometry.$M"
nice lake build "ActiveGeometry.$M" 2>&1 | tee "/fast/scratch_lean2/compile_$M.log" | grep -v '^$' | head -120
echo "EXIT ${PIPESTATUS[0]}"
if [ -f "/fast/scratch_lean2/new_modules/${M}Ax.lean" ]; then
  cp "/fast/scratch_lean2/new_modules/${M}Ax.lean" "ActiveGeometry/${M}Ax.lean"
  echo "== axioms $M"
  nice lake env lean "ActiveGeometry/${M}Ax.lean" 2>&1 | tee "/fast/scratch_lean2/axioms_$M.log" | grep -v '^$' | grep -v "^'" | head -40
  grep "^'" "/fast/scratch_lean2/axioms_$M.log" | tr -d '\n ' | sed "s/'ActiveGeometry/\n'ActiveGeometry/g"
  echo
  rm "ActiveGeometry/${M}Ax.lean"
fi
