#!/bin/zsh
# PREREG19b runner (local): 12 cells, then the score. Frozen hashes first.
cd "$(dirname "$0")"
PY=/Users/rohitfenn/miniforge3/bin/python3
{
  echo "PREREG19b frozen sha256:"
  shasum -a 256 sim_core.py measures.py hgt_core.py misspec_core.py testB_perm.py RESULTS_PREREG19.md
  date
} >> perm_run.log
rm -f testB_perm.jsonl
for gen in Cstar T; do
  for D in 1.0 2.0; do
    for s in 0 1 2; do
      $PY testB_perm.py $gen $D $s >> perm_cells.log 2>&1
    done
  done
done
$PY testB_perm.py score >> perm_run.log 2>&1
echo "PERM ALL DONE" >> perm_run.log
