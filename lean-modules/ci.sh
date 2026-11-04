#!/usr/bin/env bash
# The Lean CI for lean-modules/, runnable locally from this directory with the pinned toolchain
# (lean-toolchain) after `lake exe cache get` has fetched the Mathlib oleans. Steps, in order:
#
#   1. lake build            the proved modules (ActiveGeometryModules), timed
#   2. axiom check           axcheck/AxiomCheck.lean: every declaration on propext, Classical.choice,
#                            Quot.sound only; every theorem printed; the names the legacy axcheck/<M>Ax.lean
#                            files printed must all appear
#   3. sorry check           check_sorry.py: no `sorry` in code outside Challenges/
#   4. challenges            lake build Challenges, then per module: the number of declarations that
#                            use `sorry` (Lean's own warning) equals the number of theorems in the twin
#                            under ActiveGeometry/, and equals the number of `sorry` tokens in its code
#
# Any failure exits non-zero. The GitHub workflow .github/workflows/lean.yml runs exactly this script.
set -euo pipefail
cd "$(dirname "$0")"

PERMITTED="propext, Classical.choice, Quot.sound"
MODULES=(AuditFactors BalloonCapacity BalloonPacking CoarseConverse Heredity Persistent Rigidity Window)
fail() { echo "FAIL: $*" >&2; exit 1; }
step() { echo; echo "######## $*"; }

step "0. toolchain"
cat lean-toolchain; lean --version; lake --version

step "1. lake build (ActiveGeometryModules)"
t0=$(date +%s)
lake build
t1=$(date +%s)
echo "lake build: $((t1 - t0)) s"

step "2. axiom check (permitted: $PERMITTED)"
# The module list in AxiomCheck.lean must be the roots of ActiveGeometryModules in lakefile.toml.
roots=$(python3 -I - <<'PY'
import re,tomllib
cfg=tomllib.load(open("lakefile.toml","rb"))
lib=[l for l in cfg["lean_lib"] if l["name"]=="ActiveGeometryModules"][0]
print("\n".join(sorted(lib["roots"])))
PY
)
listed=$(grep -oE '^  `[A-Za-z]+,?$' axcheck/AxiomCheck.lean | tr -d ' `,' | sort)
[ "$roots" = "$listed" ] || fail "AxiomCheck.lean module list differs from lakefile.toml roots"
t0=$(date +%s)
lake env lean axcheck/AxiomCheck.lean | tee axcheck/axcheck.out
t1=$(date +%s)
echo "axiom check: $((t1 - t0)) s"
grep -q "== AXIOM CHECK PASSED" axcheck/axcheck.out || fail "axiom check did not pass"
# Every theorem the legacy per-module check files named must still exist and have been printed.
missing=0
for f in axcheck/*Ax.lean; do
  for n in $(grep -oE '^#print axioms [A-Za-z0-9_.'"'"']+' "$f" | awk '{print $3}'); do
    grep -qF "'$n' depends on axioms:" axcheck/axcheck.out || { echo "not printed: $n (from $f)"; missing=1; }
  done
done
[ "$missing" = 0 ] || fail "a theorem named in a legacy axcheck file was not printed (renamed or removed?)"
echo "every theorem named in axcheck/*Ax.lean was printed (and so passed the axiom check)"

step "3. sorry check (outside Challenges/)"
python3 -I check_sorry.py

step "4. challenges: build and compare sorry count with the twin's theorem count"
t0=$(date +%s)
lake build Challenges
t1=$(date +%s)
echo "lake build Challenges: $((t1 - t0)) s"
bad=0
total_thm=0; total_sorry=0
for m in "${MODULES[@]}"; do
  thm=$(grep -cE '^theorem ' "ActiveGeometry/$m.lean")
  tok=$(python3 -I check_sorry.py --count "Challenges/$m.lean" | awk '{print $1}')
  # Lean warns once per declaration whose proof or body uses sorry.
  decl=$(lake env lean "Challenges/$m.lean" 2>&1 | grep -c "declaration uses" || true)
  printf "%-16s theorems(twin)=%-3s sorry-tokens=%-3s sorry-declarations=%-3s" "$m" "$thm" "$tok" "$decl"
  if [ "$thm" = "$tok" ] && [ "$thm" = "$decl" ]; then echo " ok"; else echo " MISMATCH"; bad=1; fi
  total_thm=$((total_thm + thm)); total_sorry=$((total_sorry + decl))
done
echo "total: $total_thm theorems in ActiveGeometry/, $total_sorry sorry declarations in Challenges/"
[ "$bad" = 0 ] || fail "a challenge file's sorry count differs from its twin's theorem count"

step "ALL CHECKS PASSED"
