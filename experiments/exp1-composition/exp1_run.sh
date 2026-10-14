#!/bin/bash
# PREREG17 runner (biosphereatlas): venv with numpy, 24 rule cells at R = 4000, report cells at R = 1500, then the scorer.
cd /fast/scratch_exp1
[ -x venv/bin/python ] || (python3 -m venv venv && PIP_CACHE_DIR=/fast/scratch_exp1/pipcache venv/bin/pip install -q numpy)
echo "frozen sha256:" > run.log
sha256sum exp1_sim.py closed_form.py exp1_score.py p15_var_site_over_P.json PREREG17_composition_worth.md >> run.log
date >> run.log
cat > cells.txt <<EOF
0.8 2 4000
1.0 2 4000
1.0 3 4000
1.0 4 4000
1.25 2 4000
1.25 3 4000
1.25 4 4000
1.25 6 4000
1.5 2 4000
1.5 3 4000
1.5 4 4000
1.5 6 4000
0.8 1 1500
1.0 1 1500
1.25 1 1500
1.5 1 1500
0.8 3 1500
0.8 4 1500
0.8 6 1500
1.0 6 1500
EOF
export OMP_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
cat cells.txt | xargs -P 5 -L 1 bash -c 'nice -n 10 venv/bin/python -u exp1_sim.py $0 $1 $2 > "run_$0_$1.log" 2>&1'
echo "cells done $(date)" >> run.log
nice -n 10 venv/bin/python -u exp1_score.py > score.log 2>&1
echo "ALL DONE" >> run.log
