"""Diagnostic (tree only, no alignment): internal-edge length distribution and achievable quartet balance."""
import sys, json, math
import numpy as np
sys.path.insert(0, ".")
import prep23

root = prep23.parse_newick(open(sys.argv[1]).read())
nodes = []
st = [root]
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
internal = [x for x in nodes if x.children and x.parent is not None]
taus = np.array([x.length for x in internal])
print("internal edges", len(internal), "tau quantiles", np.quantile(taus, [0.1, 0.25, 0.5, 0.75, 0.9]).round(4).tolist())
for lo, hi in [(0.02, 0.20), (0.01, 0.30), (0.005, 0.5)]:
    print("edges with tau in", (lo, hi), int(((taus >= lo) & (taus <= hi)).sum()))
# achievable balance with best-target picking
ratios_med, ratios_best, ts_best = [], [], []
for x in internal:
    tau = x.length
    if not (0.02 <= tau <= 0.20):
        continue
    y = x.parent
    pools = [[(n, d + c.length) for n, d in down[id(c)]] for c in x.children][:2]
    py = [[(n, d + w.length) for n, d in down[id(w)]] for w in y.children if w is not x]
    up = up_pool(y)
    if up: py.append(up)
    if len(pools) < 2 or len(py) < 2:
        continue
    pools = pools + py[:2]
    arrs = [np.array(sorted(d for _, d in p)) for p in pools]
    alld = np.concatenate(arrs)
    med = float(np.median(alld))
    picks = [a[np.argmin(np.abs(a - med))] for a in arrs]
    ratios_med.append(max(picks) / max(min(picks), 1e-9))
    best = (1e9, None)
    cand = np.unique(np.concatenate([a[np.linspace(0, len(a) - 1, min(len(a), 25)).astype(int)] for a in arrs]))
    for tg in cand:
        pk = [a[np.argmin(np.abs(a - tg))] for a in arrs]
        r = max(pk) / max(min(pk), 1e-9)
        if r < best[0]:
            best = (r, float(np.mean(pk)))
    ratios_best.append(best[0]); ts_best.append(best[1])
ratios_med, ratios_best, ts_best = map(np.array, (ratios_med, ratios_best, ts_best))
print("edges considered", len(ratios_med))
print("median-rule: frac ratio<=1.5", float((ratios_med <= 1.5).mean()), "<=2", float((ratios_med <= 2).mean()))
print("best-rule:   frac ratio<=1.5", float((ratios_best <= 1.5).mean()), "<=2", float((ratios_best <= 2).mean()))
ok = ratios_best <= 1.5
bins = np.logspace(math.log10(0.05), math.log10(4.0), 9)
print("best-rule depth bins (ratio<=1.5):", np.histogram(ts_best[ok], bins=bins)[0].tolist())
print("tip depth quantiles overall", np.quantile([d for v in down.values() for _, d in v if len(v) > 1], [0.1, 0.5, 0.9]).round(3).tolist())
