#!/bin/bash
# PREREG23b steps 1–2 on biosphereatlas: MAFFT per gene, concatenate + mask, IQ-TREE GTR+F+R10 (fallback R8, R6),
# then site rates on the final tree. Everything inside /fast/scratch_h23b, under nice.
set -u
S=/fast/scratch_h23b
cd "$S" || exit 1
PY="$S/venv/bin/python"
log() { echo "$(date '+%Y-%m-%d %H:%M:%S %Z') $*" | tee -a "$S/logs/run.log"; }
log "align_tree start"
for G in ND1 ND2 COX1 COX2 ATP8 ATP6 COX3 ND3 ND4L ND4 ND5 ND6 CYTB; do
  if [ ! -s "work/aln_$G.fa" ]; then
    nice "$S/bin/mafft-linux64/mafft.bat" --auto --thread 8 --quiet "data/genes/$G.fa" > "work/aln_$G.fa"
    log "aligned $G: $(grep -c '>' work/aln_$G.fa) seqs"
  fi
done
nice "$PY" "$S/concat.py" --scratch "$S" 2>&1 | tee -a "$S/logs/run.log"
log "iqtree start"
MODELS="GTR+F+R10 GTR+F+R8 GTR+F+R6"
for M in $MODELS; do
  rm -f work/iq.*
  nice "$S/bin/iqtree2" -s work/concat.fa -m "$M" -nt 8 -mem 12G -seed 23 -pre work/iq -quiet
  if [ -s work/iq.treefile ]; then log "iqtree done with $M"; echo "$M" > work/model_used.txt; break; fi
  log "iqtree failed with $M, trying next"
done
# posterior-mean site rates on the final tree under the fitted model
nice "$S/bin/iqtree2" -s work/concat.fa -te work/iq.treefile -m "$(cat work/model_used.txt)" -n 0 -wsr -nt 8 -mem 12G -seed 23 -pre work/iqr -quiet
log "site rates done: $(grep -c '' work/iqr.rate) lines"
grep -i "model of substitution\|Rate parameter R\|State frequencies\|Site proportion and rates\|Log-likelihood of the tree\|Total tree length" work/iq.iqtree | head -20 | tee -a "$S/logs/run.log"
log "align_tree done"
