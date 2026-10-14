"""PREREG23b amendment (iv), 14 Oct, after the quartet summary and before any reader result: the registered
truth-set rule's second clause (C and D share a taxon containing neither A nor B) is unsatisfiable by the sampling
construction, which always places the root on the CD side; the first clause alone certifies the split. This script
draws quartets with the one-sided rule, in the same output format as run23b.cmd_quartets, for the labelled
secondary analyses S1 (registered balance: factor 1.5, four targets) and S2 (factor 2.0, eight targets). The frozen
run23b.py is unchanged; its read/predict/score steps take these files through --quartets.
Usage: python quartets23b_amended.py --scratch S --factor 1.5 --targets 4 --out work/quartets_S1.json
"""
import argparse, json, random, sys
import numpy as np
import run23b, prep23

ap = argparse.ArgumentParser()
ap.add_argument("--scratch", required=True); ap.add_argument("--factor", type=float, required=True)
ap.add_argument("--targets", type=int, required=True); ap.add_argument("--out", required=True)
a = ap.parse_args()
S = a.scratch
root = prep23.parse_newick(open(f"{S}/work/iq.treefile").read())
lin = run23b.load_taxonomy(f"{S}/data/taxonomy.tsv")
BINS = run23b.BINS
nodes = []; st = [root]
while st:
    x = st.pop(); nodes.append(x); st.extend(x.children)
down = {}
sys.setrecursionlimit(100000)
def post(x):
    if not x.children:
        down[id(x)] = [(x.name, 0.0)]; return
    lst = []
    for c in x.children:
        post(c); lst.extend((n, d + c.length) for n, d in down[id(c)])
    down[id(x)] = lst
post(root)
def up_pool(y):
    out = []; node, acc = y, 0.0
    while node.parent is not None:
        par = node.parent; acc += node.length
        for w in par.children:
            if w is not node:
                out.extend((n, d + w.length + acc) for n, d in down[id(w)])
        node = par
    return out
def one_sided(A, B, C, D):
    return bool((lin[A] & lin[B]) - (lin[C] | lin[D]))

quantiles = {4: (0.2, 0.4, 0.6, 0.8), 8: (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)}[a.targets]
rng = random.Random(run23b.SEED)
cands, n_edges, n_disc = [], 0, 0
for x in nodes:
    if not x.children or x.parent is None:
        continue
    tau = x.length
    if not (0.02 <= tau <= 0.50):
        continue
    n_edges += 1
    y = x.parent
    pools_x = [[(n, d + c.length) for n, d in down[id(c)]] for c in x.children][:2]
    pools_y = [[(n, d + w.length) for n, d in down[id(w)]] for w in y.children if w is not x]
    up = up_pool(y)
    if up:
        pools_y.append(up)
    if len(pools_x) < 2 or len(pools_y) < 2:
        continue
    pools = [sorted(p, key=lambda nd: nd[1]) for p in pools_x + pools_y[:2]]
    arrs = [np.array([d for _, d in p]) for p in pools]
    alld = np.concatenate(arrs)
    seen = set()
    for q in quantiles:
        tg = float(np.quantile(alld, q))
        ix = [int(np.argmin(np.abs(ar - tg))) for ar in arrs]
        depths = [float(arrs[j][ix[j]]) for j in range(4)]
        if max(depths) > a.factor * max(min(depths), 1e-9):
            continue
        tips = tuple(pools[j][ix[j]][0] for j in range(4))
        if tips in seen:
            continue
        seen.add(tips)
        A, B, C, D = tips
        if not one_sided(A, B, C, D):
            n_disc += 1; continue
        cands.append({"A": A, "B": B, "C": C, "D": D, "t": float(np.mean(depths)), "tau": float(tau),
                      "branches": depths + [float(tau)]})
per_bin = {}
for c in cands:
    b = int(np.searchsorted(BINS, c["t"], side="right") - 1)
    if 0 <= b < 8:
        per_bin.setdefault(b, []).append(c)
kept = []
for b in sorted(per_bin):
    lst = per_bin[b]; rng.shuffle(lst); kept.extend(lst[:400])
summary = {"rule": "one-sided (amendment iv)", "factor": a.factor, "targets": a.targets,
           "edges_in_tau_band": n_edges, "candidates": len(cands), "rejected_by_taxonomy": n_disc,
           "kept": len(kept), "per_bin": {str(b): min(len(v), 400) for b, v in sorted(per_bin.items())},
           "bins": BINS.tolist(), "median_tau": float(np.median([c["tau"] for c in kept])) if kept else None}
json.dump({"summary": summary, "quartets": kept}, open(a.out, "w"))
print(json.dumps(summary), flush=True)
