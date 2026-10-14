#!/bin/bash
# PREREG23b, 14 Oct: the capped-search amendment is NOT applied (run.log, 09:5x UTC): the slow phase was the NNI pass on
# the 20 best initial trees (iterations 1-2 of the log), and the registered default search is now at ~1-2 min per
# iteration. This script waits for the running default search to finish, then computes site rates on the final tree
# under the fitted model (the -wsr step of finish_tree.sh, unchanged). Inside /fast/scratch_h23b, under nice.
set -u
S=/fast/scratch_h23b
PID="${1:-1830572}"
cd "$S" || exit 1
log() { echo "$(date '+%Y-%m-%d %H:%M:%S %Z') $*" | tee -a "$S/logs/run.log"; }
log "finish_tree2 start: waiting for the default search (pid $PID) to finish"
while kill -0 "$PID" 2>/dev/null; do sleep 120; done
log "search process gone; treefile $(stat -c %y work/iq.treefile 2>/dev/null | cut -c1-19); $(grep -c 'TREE SEARCH COMPLETED' work/iq.log) completion line(s)"
grep -q "TREE SEARCH COMPLETED" work/iq.log || { log "search did not complete; abort"; exit 2; }
echo "GTR+F+R10" > work/model_used.txt
nice "$S/bin/iqtree2" -s work/concat.fa -te work/iq.treefile -m GTR+F+R10 -n 0 -wsr -nt 8 -mem 12G -seed 23 -pre work/iqr -quiet
log "site rates done: $(grep -c '' work/iqr.rate) lines"
grep -i "Rate parameter R\|State frequencies\|Site proportion and rates\|Log-likelihood of the tree\|Total tree length" work/iq.iqtree | head -12 | tee -a "$S/logs/run.log"
log "finish_tree2 done"
