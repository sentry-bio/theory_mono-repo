#!/bin/bash
# PREREG23b amendment (capped search): resume IQ-TREE from its checkpoint with -n 3, then site rates on the final
# tree under the fitted model. Inside /fast/scratch_h23b, under nice.
set -u
S=/fast/scratch_h23b
cd "$S" || exit 1
log() { echo "$(date '+%Y-%m-%d %H:%M:%S %Z') $*" | tee -a "$S/logs/run.log"; }
log "finish_tree start (resume with -n 3)"
nice "$S/bin/iqtree2" -s work/concat.fa -m GTR+F+R10 -nt 8 -mem 12G -seed 23 -pre work/iq -n 3 -quiet
log "iqtree resume exit $? ; treefile $(stat -c %y work/iq.treefile 2>/dev/null | cut -c1-19)"
echo "GTR+F+R10" > work/model_used.txt
nice "$S/bin/iqtree2" -s work/concat.fa -te work/iq.treefile -m GTR+F+R10 -n 0 -wsr -nt 8 -mem 12G -seed 23 -pre work/iqr -quiet
log "site rates done: $(grep -c '' work/iqr.rate) lines"
grep -i "Rate parameter R\|State frequencies\|Site proportion and rates\|Log-likelihood of the tree\|Total tree length" work/iq.iqtree | head -12 | tee -a "$S/logs/run.log"
log "finish_tree done"
