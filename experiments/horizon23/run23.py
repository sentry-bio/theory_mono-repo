"""PREREG23 steps 3–6: quartets on the pruned tree, two readers (plus the shuffle control), readable depth,
exact-curve prediction, registered verdicts.

Usage:
  python3 -I run23.py quartets --tree work/iq.treefile --out work/quartets.json [--max-per-bin 400]
  python3 -I run23.py read --msa work/sub.faa --quartets work/quartets.json --rates work/iq.rate \
          --L 64 128 256 512 1024 2048 4096 --subsets 40 --out work/reads.json [--smoke]
  python3 -I run23.py tstar --reads work/reads.json --quartets work/quartets.json --out work/tstar.json
  python3 -I run23.py predict --tstar work/tstar.json --iqtree work/iq.iqtree --quartets work/quartets.json --out work/pred23.json
  python3 -I run23.py score --tstar work/tstar.json --pred work/pred23.json --out score23.json
"""
import argparse, json, math, random, re, sys, time
import numpy as np

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
import prep23  # noqa: E402

Q = 20  # amino-acid alphabet
SEED = 23
GAPS = set("-?X.*")

# ------------------------------------------------------------------ channel (q-letter symmetric)

def lam(r, ell):
    return np.exp(-(Q / (Q - 1.0)) * r * ell)

def p_same(r, ell):
    return 1.0 / Q + (1 - 1.0 / Q) * lam(r, ell)

def signal(r, t, tau):
    return p_same(r, 2 * t) - p_same(r, 2 * t + tau)

def variance(r, t, tau):
    p1 = p_same(r, 2 * t); p2 = p_same(r, 2 * t + tau)
    P0t, P1t = p_same(r, t), (1 - lam(r, t)) / Q
    P0s, P1s = p_same(r, t + tau), (1 - lam(r, t + tau)) / Q
    q = P0t ** 2 * P0s + (Q - 1) * P1t ** 2 * P1s
    return p1 * (1 - p1) + p2 * (1 - p2) - 2 * (q - p1 * p2)

# ------------------------------------------------------------------ quartets

def cmd_quartets(a):
    root = prep23.parse_newick(open(a.tree).read())
    # index tips, parents, children; compute down-lists (tip, depth) per node
    nodes = []
    st = [root]
    while st:
        x = st.pop(); nodes.append(x); st.extend(x.children)
    down = {}
    for x in reversed(nodes):  # children before parents (reverse of pre-order push order is not guaranteed; do post-order)
        pass
    def post(x):
        if not x.children:
            down[id(x)] = [(x.name, 0.0)]
            return
        lst = []
        for c in x.children:
            post(c)
            lst.extend((n, d + c.length) for n, d in down[id(c)])
        down[id(x)] = lst
    sys.setrecursionlimit(100000)
    post(root)
    def up_pool(y):
        """Tips not below y, with their path length to y (the complement subtree at y)."""
        out = []
        node, acc = y, 0.0
        while node.parent is not None:
            par = node.parent
            acc += node.length
            for w in par.children:
                if w is not node:
                    out.extend((n, d + w.length + acc) for n, d in down[id(w)])
            node = par
        return out
    rng = random.Random(SEED)
    cands = []
    for x in nodes:
        if not x.children or x.parent is None:
            continue
        y = x.parent
        tau = x.length
        if not (0.02 <= tau <= 0.20):
            continue
        pools_x = [[(n, d + c.length) for n, d in down[id(c)]] for c in x.children]
        pools_y = [[(n, d + w.length) for n, d in down[id(w)]] for w in y.children if w is not x]
        up = up_pool(y)
        if up:
            pools_y.append(up)
        if len(pools_x) < 2 or len(pools_y) < 2:
            continue
        pools = [sorted(p, key=lambda nd: nd[1]) for p in (pools_x[:2] + pools_y[:2])]
        arrs = [np.array([d for _, d in p]) for p in pools]
        # amendment (iv): target depth minimising the max/min ratio of the four closest-depth picks
        cand = np.unique(np.concatenate(
            [a[np.linspace(0, len(a) - 1, min(len(a), 25)).astype(int)] for a in arrs]))
        best = None
        for tg in cand:
            ix = [int(np.argmin(np.abs(a - tg))) for a in arrs]
            depths = [arrs[j][ix[j]] for j in range(4)]
            ratio = max(depths) / max(min(depths), 1e-9)
            if best is None or ratio < best[0]:
                best = (ratio, ix, depths)
        ratio, ix, depths = best
        if ratio > 1.5:
            continue
        pick = [pools[j][ix[j]] for j in range(4)]
        t = float(np.mean(depths))
        cands.append({"A": pick[0][0], "B": pick[1][0], "C": pick[2][0], "D": pick[3][0],
                      "t": t, "tau": float(tau), "depths": [float(d) for d in depths]})
    bins = np.logspace(math.log10(0.03), math.log10(1.5), 9)  # amendment (v)
    kept = []
    per_bin = {}
    for c in cands:
        b = int(np.searchsorted(bins, c["t"], side="right") - 1)
        if b < 0 or b >= 8:
            continue
        per_bin.setdefault(b, []).append(c)
    for b in sorted(per_bin):
        lst = per_bin[b]
        rng.shuffle(lst)
        kept.extend(lst[:a.max_per_bin])
    summary = {"candidates": len(cands), "kept": len(kept), "bins": bins.tolist(),
               "per_bin": {str(b): min(len(v), a.max_per_bin) for b, v in sorted(per_bin.items())},
               "median_tau": float(np.median([c["tau"] for c in kept])) if kept else None}
    json.dump({"summary": summary, "quartets": kept}, open(a.out, "w"))
    print(json.dumps(summary), flush=True)

# ------------------------------------------------------------------ reading

def read_rates(path):
    rates = {}
    for line in open(path):
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        if parts[0].lower() == "site":
            continue
        rates[int(parts[0])] = float(parts[1])
    L = max(rates)
    arr = np.array([rates[i] for i in range(1, L + 1)])
    return arr / arr.mean()

def cmd_read(a):
    qs = json.load(open(a.quartets))["quartets"]
    if a.smoke:
        qs = qs[:100]
    names = set()
    for q in qs:
        names.update((q["A"], q["B"], q["C"], q["D"]))
    seqs = prep23.read_fasta_subset(a.msa, names)
    rates = read_rates(a.rates)
    Lmax = len(next(iter(seqs.values())))
    assert len(rates) == Lmax, (len(rates), Lmax)
    rng = np.random.default_rng(SEED)
    perm = rng.permutation(Lmax)
    rates_shuf = rates[perm]
    code = {n: np.frombuffer(s.encode(), dtype=np.uint8) for n, s in seqs.items()}  # fix 05:2x: keys are names
    gapset = np.frombuffer("".join(sorted(GAPS)).encode(), dtype=np.uint8)
    grid = [L for L in a.L if L <= Lmax]
    out = {"L": grid, "subsets": a.subsets, "Lmax": Lmax, "smoke": a.smoke, "quartets": []}
    t0 = time.time()
    pairs = [("A", "B"), ("C", "D"), ("A", "C"), ("B", "D"), ("A", "D"), ("B", "C")]
    for qi, q in enumerate(qs):
        S = {k: code[q[k]] for k in "ABCD"}
        valid = np.ones(Lmax, dtype=bool)
        for k in "ABCD":
            valid &= ~np.isin(S[k], gapset)
        mm = np.stack([(S[x] != S[y]) & valid for x, y in pairs]).astype(np.float64)  # 6 × Lmax
        w_true = signal(rates, q["t"], q["tau"]) / variance(rates, q["t"], q["tau"])
        w_shuf = signal(rates_shuf, q["t"], q["tau"]) / variance(rates_shuf, q["t"], q["tau"])
        res = {"t": q["t"], "tau": q["tau"], "valid": int(valid.sum())}
        for L in grid:
            idx = np.stack([rng.choice(Lmax, size=L, replace=False) for _ in range(a.subsets)])  # subsets × L
            sub = mm[:, idx]  # 6 × subsets × L
            for name, w in (("U", None), ("W", w_true), ("S", w_shuf)):
                s = sub.sum(axis=2) if w is None else (sub * w[idx]).sum(axis=2)  # 6 × subsets
                true = s[0] + s[1]; alt1 = s[2] + s[3]; alt2 = s[4] + s[5]
                ok = (true < alt1) & (true < alt2)
                res[f"{name}|{L}"] = int(ok.sum())
        out["quartets"].append(res)
        if qi % 200 == 0:
            print(f"quartet {qi}/{len(qs)} {time.time() - t0:.0f}s", flush=True)
    out["elapsed_s"] = time.time() - t0
    json.dump(out, open(a.out, "w"))
    print("done", len(qs), "quartets", f"{out['elapsed_s']:.0f}s", flush=True)

# ------------------------------------------------------------------ readable depth (logistic in ln t)

def fit_logistic(x, k, n):
    """Maximise sum k·log p + (n−k)·log(1−p), p = σ(a + b x). Newton with damping; returns (a, b)."""
    a, b = 0.0, -1.0
    for _ in range(200):
        z = a + b * x
        p = 1 / (1 + np.exp(-z))
        g = np.array([np.sum(k - n * p), np.sum((k - n * p) * x)])
        wv = n * p * (1 - p) + 1e-12
        H = np.array([[np.sum(wv), np.sum(wv * x)], [np.sum(wv * x), np.sum(wv * x * x)]])
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            break
        a, b = a + step[0], b + step[1]
        if np.max(np.abs(step)) < 1e-9:
            break
    return a, b

def cmd_tstar(a):
    reads = json.load(open(a.reads))
    grid, n = reads["L"], reads["subsets"]
    x = np.log(np.array([q["t"] for q in reads["quartets"]]))
    out = {"L": grid, "subsets": n, "cells": {}, "tmin": float(np.exp(x.min())), "tmax": float(np.exp(x.max()))}
    for name in ("U", "W", "S"):
        for L in grid:
            k = np.array([q[f"{name}|{L}"] for q in reads["quartets"]], dtype=float)
            nn = np.full_like(k, n)
            A, B = fit_logistic(x, k, nn)
            cell = {"a": A, "b": B}
            if B < 0:
                xs = (math.log(0.9 / 0.1) - A) / B
                ts = math.exp(xs)
                cell["tstar"] = ts
                cell["resolved"] = bool(out["tmin"] <= ts <= out["tmax"])
            else:
                cell["tstar"] = None; cell["resolved"] = False
            out["cells"][f"{name}|{L}"] = cell
    json.dump(out, open(a.out, "w"), indent=1)
    for name in ("U", "W", "S"):
        print(name, " ".join(f"{L}:{out['cells'][f'{name}|{L}']['tstar'] or float('nan'):.3f}{'' if out['cells'][f'{name}|{L}']['resolved'] else '!'}" for L in grid))

# ------------------------------------------------------------------ prediction

def rate_sample(alpha, n=400000, seed=12345):
    rng = np.random.default_rng(seed)
    return rng.gamma(shape=alpha, scale=1.0 / alpha, size=n)

def snr(L, t, tau, which, r):
    s = signal(r, t, tau); v = variance(r, t, tau)
    if which == "U":
        return math.sqrt(L) * s.mean() / math.sqrt(v.mean())
    return math.sqrt(L * (s * s / v).mean())

def solve_t(L, tau, which, kappa, r, lo=1e-4, hi=400.0):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if snr(L, mid, tau, which, r) >= kappa:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def parse_alpha(path):
    for line in open(path):
        m = re.search(r"Gamma shape alpha:\s*([0-9.]+)", line)
        if m:
            return float(m.group(1))
    raise SystemExit("alpha not found")

def cmd_predict(a):
    ts = json.load(open(a.tstar)); qs = json.load(open(a.quartets))
    alpha = parse_alpha(a.iqtree); tau = qs["summary"]["median_tau"]
    r = rate_sample(alpha)
    grid = ts["L"]
    out = {"alpha": alpha, "median_tau": tau, "fit_L": {}, "kappa": {}, "pred": {}}
    for which in ("U", "W"):
        # amendment (vi): κ fitted on the smallest RESOLVED L for this reader
        fitL = next((L for L in grid if ts["cells"][f"{which}|{L}"]["resolved"]), None)
        out["fit_L"][which] = fitL
        if fitL is None:
            out["kappa"][which] = None; continue
        c = ts["cells"][f"{which}|{fitL}"]
        kappa = snr(fitL, c["tstar"], tau, which, r)
        out["kappa"][which] = kappa
        out["pred"][which] = {str(L): solve_t(L, tau, which, kappa, r) for L in grid}
    out["asymptote"] = {"U": 1 / (2 * (alpha + 1)), "W": 1 / (alpha + 2)}
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("alpha", "median_tau", "kappa", "asymptote")}))

# ------------------------------------------------------------------ scoring

def local_slope(Ls, ts):
    return float(np.polyfit(np.log(np.array(Ls, float)), np.log(np.array(ts, float)), 1)[0])

def cmd_score(a):
    ts = json.load(open(a.tstar)); pr = json.load(open(a.pred))
    grid = ts["L"]
    def obs(name, L):
        c = ts["cells"][f"{name}|{L}"]
        return c["tstar"] if c["resolved"] else None
    rep = {"verdicts": {}, "readings": {"alpha": pr["alpha"], "kappa": pr["kappa"], "asymptote": pr["asymptote"],
                                         "fit_L": pr["fit_L"]}}
    unresolved = [k for k, c in ts["cells"].items() if not c["resolved"]]
    rep["readings"]["unresolved_cells"] = unresolved
    # amendment (vi): thresholds relative to the fit L of each reader (64 → 256/128 as registered)
    fitU = pr["fit_L"].get("U") or 64; fitW = pr["fit_L"].get("W") or 64
    for which, vname in (("U", "V1_form_unweighted"), ("W", "V2_form_weighted")):
        errs, ok = {}, True
        fitL = fitU if which == "U" else fitW
        for L in grid:
            if L < 4 * fitL:
                continue
            o = obs(which, L); p = pr["pred"].get(which, {}).get(str(L))
            if o is None or p is None:
                ok = False; errs[str(L)] = None; continue
            e = (o - p) / p; errs[str(L)] = e
            if abs(e) > 0.25:
                ok = False
        rep["verdicts"][vname] = {"pass": ok, "rel_err": errs}
    ratios, ok = {}, True
    firstL = 2 * max(fitU, fitW)
    for L in grid:
        if L < firstL:
            continue
        u, w = obs("U", L), obs("W", L)
        if u is None or w is None:
            ok = False; ratios[str(L)] = None; continue
        ratios[str(L)] = w / u
        if not w > u:
            ok = False
    incl = [L for L in grid if L >= firstL]
    if ok and incl and ratios.get(str(incl[-1])) is not None and ratios.get(str(incl[0])) is not None:
        ok = ratios[str(incl[-1])] > ratios[str(incl[0])]
    rep["verdicts"]["V3_ordering"] = {"pass": ok, "ratios": ratios, "first_L": firstL}
    top = grid[-3:]
    v4, ok = {}, True
    for which in ("U", "W"):
        o = [obs(which, L) for L in top]; p = [pr["pred"].get(which, {}).get(str(L)) for L in top]
        if any(v is None for v in o + p):
            ok = False; v4[which] = None; continue
        so, sp = local_slope(top, o), local_slope(top, p)
        v4[which] = {"obs": so, "pred_exact": sp, "asymptote": pr["asymptote"][which]}
        if abs(so - sp) > 0.08:
            ok = False
    rep["verdicts"]["V4_exponent"] = {"pass": ok, "slopes": v4}
    v5, ok = {}, True
    for L in grid:
        if L < 4 * fitU:
            continue
        u, s = obs("U", L), obs("S", L)
        if u is None or s is None:
            ok = False; v5[str(L)] = None; continue
        v5[str(L)] = s / u - 1
        if abs(s / u - 1) > 0.15:
            ok = False
    rep["verdicts"]["V5_shuffle"] = {"pass": ok, "rel_diff": v5}
    rep["overall"] = "LAW SUPPORTED ON REAL DATA" if all(v["pass"] for v in rep["verdicts"].values()) else "NOT SUPPORTED AS REGISTERED"
    json.dump(rep, open(a.out, "w"), indent=1)
    for k, v in rep["verdicts"].items():
        print(k, "PASS" if v["pass"] else "FAIL")
    print(rep["overall"])

# ------------------------------------------------------------------ cli

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("quartets"); q.add_argument("--tree", required=True); q.add_argument("--out", required=True); q.add_argument("--max-per-bin", dest="max_per_bin", type=int, default=400)
    r = sub.add_parser("read"); r.add_argument("--msa", required=True); r.add_argument("--quartets", required=True); r.add_argument("--rates", required=True)
    r.add_argument("--L", type=int, nargs="+", default=[64, 128, 256, 512, 1024, 2048, 4096]); r.add_argument("--subsets", type=int, default=40); r.add_argument("--smoke", action="store_true"); r.add_argument("--out", required=True)
    t = sub.add_parser("tstar"); t.add_argument("--reads", required=True); t.add_argument("--quartets", required=True); t.add_argument("--out", required=True)
    p = sub.add_parser("predict"); p.add_argument("--tstar", required=True); p.add_argument("--iqtree", required=True); p.add_argument("--quartets", required=True); p.add_argument("--out", required=True)
    s = sub.add_parser("score"); s.add_argument("--tstar", required=True); s.add_argument("--pred", required=True); s.add_argument("--out", required=True)
    args = ap.parse_args()
    {"quartets": cmd_quartets, "read": cmd_read, "tstar": cmd_tstar, "predict": cmd_predict, "score": cmd_score}[args.cmd](args)
