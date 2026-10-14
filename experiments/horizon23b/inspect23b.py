"""Local inspection of PREREG23b outputs (readings only): t* curves, pooled recovery by L, reader and depth bin,
observed against predicted. Usage: python inspect23b.py <suffix>  e.g. _S2"""
import json, sys
import numpy as np
suf = sys.argv[1] if len(sys.argv) > 1 else ""
s = json.load(open(f'results/score23b{suf}.json'))
fmt = lambda v: (round(v, 3) if isinstance(v, (int, float)) else v)
print("observed t*:", {k: fmt(v) for k, v in s['observed_tstar'].items()})
print("predicted t*:", {k: fmt(v) for k, v in s['predicted_tstar'].items()})
print("readings:", s['readings'])
r = json.load(open(f'work/reads{suf}.json')); p = json.load(open(f'work/pred{suf}.json'))
print("reads top keys", list(r.keys()))
q0 = r['quartets'][0]
print("quartet keys", list(q0.keys()))
for k, v in q0.items():
    print("  ", k, str(v)[:160])
print("pred top keys", list(p.keys()))
pq = p['quartets'][0] if isinstance(p.get('quartets'), list) else None
if pq:
    print("pred quartet keys", list(pq.keys()))
    for k, v in pq.items():
        print("  ", k, str(v)[:160])
