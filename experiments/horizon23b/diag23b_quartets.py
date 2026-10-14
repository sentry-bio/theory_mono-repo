"""PREREG23b diagnostic (14 Oct, after the quartet summary and before any reader result): why did the registered
quartet draw keep 3 of 103 candidates? Re-runs the draw of run23b.cmd_quartets with the truth-set rule and the
depth-balance factor varied, and reports counts per depth bin. Reads only the tree and the taxonomy; writes nothing
except its printout. Usage: python diag23b_quartets.py --scratch S
"""
import argparse, json, random, sys
import numpy as np
import run23b, prep23

ap = argparse.ArgumentParser(); ap.add_argument("--scratch", required=True); a = ap.parse_args()
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

def two_sided(A, B, C, D):
    return run23b.concordant(lin, A, B, C, D)
def one_sided(A, B, C, D):
    ab = lin[A] & lin[B]
    return bool(ab - (lin[C] | lin[D]))

def draw(rule, factor, quantiles):
    n_edges = 0; attempts = 0; balanced = 0; kept = []
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
            attempts += 1
            tg = float(np.quantile(alld, q))
            ix = [int(np.argmin(np.abs(ar - tg))) for ar in arrs]
            depths = [float(arrs[j][ix[j]]) for j in range(4)]
            if max(depths) > factor * max(min(depths), 1e-9):
                continue
            balanced += 1
            tips = tuple(pools[j][ix[j]][0] for j in range(4))
            if tips in seen:
                continue
            seen.add(tips)
            if rule(*tips):
                kept.append(float(np.mean(depths)))
    per_bin = {}
    for t in kept:
        b = int(np.searchsorted(BINS, t, side="right") - 1)
        if 0 <= b < 8:
            per_bin[b] = per_bin.get(b, 0) + 1
    return {"edges": n_edges, "attempts": attempts, "balanced": balanced, "kept": len(kept),
            "per_bin": {str(b): per_bin[b] for b in sorted(per_bin)}}

Q4 = (0.2, 0.4, 0.6, 0.8)
Q8 = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8)
for name, rule, factor, qs in [("registered: two-sided, factor 1.5, 4 targets", two_sided, 1.5, Q4),
                               ("one-sided, factor 1.5, 4 targets", one_sided, 1.5, Q4),
                               ("one-sided, factor 2.0, 4 targets", one_sided, 2.0, Q4),
                               ("one-sided, factor 1.5, 8 targets", one_sided, 1.5, Q8),
                               ("one-sided, factor 2.0, 8 targets", one_sided, 2.0, Q8),
                               ("no taxonomy, factor 1.5, 4 targets", lambda *t: True, 1.5, Q4)]:
    print(name, json.dumps(draw(rule, factor, qs)), flush=True)
# tip-depth spread on this tree, for the record
tipd = np.array([d for _, d in down[id(root)]])
print("tip depths from root: min %.3f median %.3f max %.3f" % (tipd.min(), np.median(tipd), tipd.max()))
print("bins", BINS.tolist())
