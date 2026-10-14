"""PREREG23b readings: pooled recovery by tape length and reader, observed (40 subsets per quartet) against the
parameter-free prediction (200 replicates per quartet), overall and by depth bin. Usage: python pooled23b.py _S2"""
import json, sys
import numpy as np
suf = sys.argv[1] if len(sys.argv) > 1 else ""
r = json.load(open(f'work/reads{suf}.json')); p = json.load(open(f'work/pred{suf}.json'))
BINS = np.logspace(np.log10(0.05), np.log10(3.0), 9)
L = [str(x) for x in r['L']]; ns = r['subsets']; reps = p['reps']
readers = ['U', 'W', 'S', 'U_RY', 'W_RY']
pq = {round(q['t'], 9): q for q in p['quartets']}
rows = []
for q in r['quartets']:
    b = int(np.searchsorted(BINS, q['t'], side='right') - 1)
    rows.append((b, q, pq.get(round(q['t'], 9))))
print(f"n={len(rows)} quartets; subsets={ns}; reps={reps}; depth bins present:", sorted(set(b for b, _, _ in rows)))
def table(sel, label):
    print(f"\n{label}: n={len(sel)}")
    print("L      " + "  ".join(f"{rd:>11}" for rd in readers) + "   (obs/pred)")
    for l in L + ['full']:
        cells = []
        for rd in readers:
            o = np.mean([q[l][rd] / (1 if l == 'full' else ns) for _, q, _ in sel])
            if rd == 'S':
                cells.append(f"{o:5.3f}/  -  ")
            else:
                pr = np.mean([pp[l][rd] / (1 if l == 'full' else reps) for _, _, pp in sel if pp])
                cells.append(f"{o:5.3f}/{pr:5.3f}")
        print(f"{l:<6} " + "  ".join(f"{c:>11}" for c in cells))
table(rows, "ALL quartets")
for b in sorted(set(b for b, _, _ in rows)):
    sel = [x for x in rows if x[0] == b]
    if len(sel) >= 5:
        table(sel, f"depth bin {b} [{BINS[b]:.3f}, {BINS[b+1]:.3f})")
# the W-U contrast per L, observed and predicted, pooled
print("\nW minus U (pooled), observed / predicted:")
for l in L:
    ou = np.mean([q[l]['U'] / ns for _, q, _ in rows]); ow = np.mean([q[l]['W'] / ns for _, q, _ in rows])
    pu = np.mean([pp[l]['U'] / reps for _, _, pp in rows if pp]); pw = np.mean([pp[l]['W'] / reps for _, _, pp in rows if pp])
    osv = np.mean([q[l]['S'] / ns for _, q, _ in rows])
    print(f"  L={l:>5}: obs W-U {ow-ou:+.3f}  pred W-U {pw-pu:+.3f}   obs S-U {osv-ou:+.3f}")
