#!/bin/bash
# PREREG23b readers, prediction and scoring, in order: (1) the registered pipeline on the registered quartet file
# (verdict of record); (2) the disclosed smoke test on the S2 quartet file (kept, not interpreted); (3) secondary
# analysis S1 (one-sided truth set, registered balance); (4) secondary analysis S2 (one-sided, factor 2.0, eight
# targets). Frozen run23b.py throughout. Inside /fast/scratch_h23b, under nice.
set -u
S=/fast/scratch_h23b
cd "$S" || exit 1
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" | tee -a "$S/logs/run.log"; }
PY="nice $S/venv/bin/python $S/run23b.py"
run() {  # label quartets-file suffix [--smoke]
  local label="$1" q="$2" suf="$3" smoke="${4:-}"
  log "$label read start ($q $smoke)"
  $PY read --scratch "$S" --quartets "$q" --out "work/reads$suf.json" $smoke > "logs/read$suf.out" 2>&1
  log "$label read exit $? ; $(tail -1 logs/read$suf.out | cut -c1-120)"
  log "$label predict start"
  $PY predict --scratch "$S" --quartets "$q" --reads "work/reads$suf.json" --out "work/pred$suf.json" $smoke > "logs/pred$suf.out" 2>&1
  log "$label predict exit $? ; $(tail -1 logs/pred$suf.out | cut -c1-120)"
  if [ -z "$smoke" ]; then
    log "$label score start"
    $PY score --scratch "$S" --quartets "$q" --reads "work/reads$suf.json" --pred "work/pred$suf.json" --out "score23b$suf.json" > "logs/score$suf.out" 2>&1
    log "$label score exit $? ; $(grep -m1 -i 'verdict\|overall' logs/score$suf.out | cut -c1-120)"
  fi
}
log "pipeline23b start; run23b.py $(sha256sum run23b.py | cut -c1-16)"
run "REGISTERED (3 quartets)" work/quartets.json ""
run "SMOKE on S2 (disclosed; kept, not interpreted)" work/quartets_S2.json "_S2smoke" "--smoke"
run "SECONDARY S1 (one-sided truth set, registered balance)" work/quartets_S1.json "_S1"
run "SECONDARY S2 (one-sided, factor 2.0, eight targets)" work/quartets_S2.json "_S2"
log "pipeline23b done"
