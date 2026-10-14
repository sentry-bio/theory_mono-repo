#!/bin/bash
# PREREG19 runner (biosphereatlas): venv, frozen hashes, smoke test, 21 jobs (each runs its L values), then the scorer.
cd /fast/scratch_testB
[ -x venv/bin/python ] || (python3 -m venv venv && PIP_CACHE_DIR=/fast/scratch_testB/pipcache venv/bin/pip install -q numpy scipy)
echo "frozen sha256:" > run.log
sha256sum sim_core.py measures.py hgt_core.py misspec_core.py testB_run.py testB_score.py PREREG19_testB.md >> run.log
date >> run.log
export OMP_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1
venv/bin/python smoke.py > smoke.log 2>&1 || { echo "SMOKE FAILED" >> run.log; exit 1; }
echo "smoke ok" >> run.log
rm -f testB_cells.jsonl
cat > jobs.txt <<EOF
T 1.0 0
T 2.0 0
G 1.0 0
G 2.0 0
H 1.0 0
H 2.0 0
Cstar 1.0 0
T 1.0 1
T 2.0 1
G 1.0 1
G 2.0 1
H 1.0 1
H 2.0 1
Cstar 1.0 1
T 1.0 2
T 2.0 2
G 1.0 2
G 2.0 2
H 1.0 2
H 2.0 2
Cstar 1.0 2
EOF
cat jobs.txt | xargs -P 4 -L 1 bash -c 'nice -n 10 venv/bin/python -u testB_run.py $0 $1 $2 > "job_$0_$1_$2.log" 2>&1'
echo "jobs done $(date)" >> run.log
nice -n 10 venv/bin/python -u testB_score.py > score.log 2>&1
echo "ALL DONE" >> run.log
