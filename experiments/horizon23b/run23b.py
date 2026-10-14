"""PREREG23b steps 3–7: taxonomy-concordant quartets on the IQ-TREE tree, exact per-quartet model (GTR+F+R
matrix exponentials), observed reads (U, W, S; RY arm), parametric predictions through the identical reader,
plateau-normalised isotonic readable depth, registered verdicts.

Usage (inside the scratch dir, venv python):
  python run23b.py quartets --scratch S --out work/quartets.json
  python run23b.py read     --scratch S --quartets work/quartets.json --out work/reads.json [--smoke]
  python run23b.py predict  --scratch S --quartets work/quartets.json --reads work/reads.json --out work/pred.json [--smoke]
  python run23b.py score    --scratch S --quartets work/quartets.json --reads work/reads.json --pred work/pred.json --out score23b.json
"""
import argparse, json, math, random, re, sys, time
import numpy as np

sys.path.insert(0, "/fast/scratch_h23b")
sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
sys.path.insert(0, (__file__.rsplit("/", 1)[0] if "/" in __file__ else ".") + "/../horizon23")
import prep23  # noqa: E402  (Newick parser)

SEED = 23
STATES = "ACGT"
L_GRID = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
BINS = np.logspace(math.log10(0.05), math.log10(3.0), 9)
PAIRS = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]  # AB, CD, AC, BD, AD, BC over leaf order A,B,C,D

# ------------------------------------------------------------------ model from the .iqtree file

def parse_model(path):
    txt = open(path).read()
    ex = {}
    for k in ("A-C", "A-G", "A-T", "C-G", "C-T", "G-T"):
        m = re.search(rf"^\s*{k}:\s*([0-9.eE+-]+)", txt, re.M)
        ex[k] = float(m.group(1))
    pi = {}
    for s in STATES:
        m = re.search(rf"pi\({s}\)\s*=\s*([0-9.eE+-]+)", txt)
        pi[s] = float(m.group(1))
    m = re.search(r"Site proportion and rates:\s*((?:\([0-9.eE+-]+,[0-9.eE+-]+\)\s*)+)", txt)
    pr = re.findall(r"\(([0-9.eE+-]+),([0-9.eE+-]+)\)", m.group(1))
    weights = np.array([float(p) for p, _ in pr]); rates = np.array([float(r) for _, r in pr])
    weights /= weights.sum()
    rates /= (weights * rates).sum()  # mean site rate 1 under the class weights
    return ex, np.array([pi[s] for s in STATES]), rates, weights


class GTR:
    def __init__(self, ex, pi):
        s = np.zeros((4, 4))
        idx = {"A": 0, "C": 1, "G": 2, "T": 3}
        for k, v in ex.items():
            i, j = idx[k[0]], idx[k[2]]
            s[i, j] = s[j, i] = v
        Q = s * pi[None, :]
        np.fill_diagonal(Q, 0.0)
        np.fill_diagonal(Q, -Q.sum(axis=1))
        Q /= -(pi * np.diag(Q)).sum()  # one expected substitution per site per unit length
        self.pi = pi
        sp = np.sqrt(pi)
        S = (sp[:, None] * Q) / sp[None, :]  # symmetric
        lam, V = np.linalg.eigh((S + S.T) / 2)
        self.lam, self.V, self.sp = lam, V, sp

    def P(self, ell):
        E = np.exp(self.lam * ell)
        M = (self.V * E[None, :]) @ self.V.T
        return (M / self.sp[:, None]) * self.sp[None, :]

    def joint(self, br, r):
        """Joint distribution of (A,B,C,D) letters for branch durations br = (la, lb, lc, ld, tau) at site rate r."""
        la, lb, lc, ld, tau = br
        Pt, Pa, Pb, Pc, Pd = (self.P(x * r) for x in (tau, la, lb, lc, ld))
        return np.einsum("x,xy,xa,xb,yc,yd->abcd", self.pi, Pt, Pa, Pb, Pc, Pd)


def value_vectors(nstates):
    """Per-outcome four-point contrasts v1 = (m_AC+m_BD)-(m_AB+m_CD), v2 = (m_AD+m_BC)-(m_AB+m_CD)."""
    g = np.indices((nstates,) * 4).reshape(4, -1)
    m = {p: (g[p[0]] != g[p[1]]).astype(float) for p in PAIRS}
    base = m[(0, 1)] + m[(2, 3)]
    return m[(0, 2)] + m[(1, 3)] - base, m[(0, 3)] + m[(1, 2)] - base


V1, V2 = value_vectors(4)
V1R, V2R = value_vectors(2)
RY_MAP = np.array([0, 1, 0, 1])  # A,G -> R(0); C,T -> Y(1)


def lump_ry(joint):
    j2 = np.zeros((2,) * 4)
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    j2[RY_MAP[a], RY_MAP[b], RY_MAP[c], RY_MAP[d]] += joint[a, b, c, d]
    return j2


def site_stats(joint, v1, v2):
    p = joint.reshape(-1)
    d = (v1 + v2) / 2
    s = float(p @ d); var = float(p @ (d * d) - s * s)
    return s, max(var, 1e-12)

# ------------------------------------------------------------------ quartets

def load_taxonomy(path):
    lin = {}
    for line in open(path):
        if line.startswith("accession"):
            continue
        acc, cls, org, lineage = line.rstrip("\n").split("\t")
        lin[acc] = set(lineage.split(";"))
    common = set.intersection(*lin.values()) if lin else set()
    return {k: v - common for k, v in lin.items()}


def concordant(lin, A, B, C, D):
    ab = lin[A] & lin[B]; cd = lin[C] & lin[D]
    return bool(ab - (lin[C] | lin[D])) and bool(cd - (lin[A] | lin[B]))


def cmd_quartets(a):
    S = a.scratch
    root = prep23.parse_newick(open(f"{S}/work/iq.treefile").read())
    lin = load_taxonomy(f"{S}/data/taxonomy.tsv")
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
    rng = random.Random(SEED)
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
        for q in (0.2, 0.4, 0.6, 0.8):
            tg = float(np.quantile(alld, q))
            ix = [int(np.argmin(np.abs(ar - tg))) for ar in arrs]
            depths = [float(arrs[j][ix[j]]) for j in range(4)]
            if max(depths) > 1.5 * max(min(depths), 1e-9):
                continue
            tips = tuple(pools[j][ix[j]][0] for j in range(4))
            if tips in seen:
                continue
            seen.add(tips)
            A, B, C, D = tips
            if not concordant(lin, A, B, C, D):
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
    summary = {"edges_in_tau_band": n_edges, "candidates": len(cands), "rejected_by_taxonomy": n_disc,
               "kept": len(kept), "per_bin": {str(b): min(len(v), 400) for b, v in sorted(per_bin.items())},
               "bins": BINS.tolist(), "median_tau": float(np.median([c["tau"] for c in kept])) if kept else None}
    json.dump({"summary": summary, "quartets": kept}, open(a.out, "w"))
    print(json.dumps(summary), flush=True)

# ------------------------------------------------------------------ alignment, rates, weights

def load_alignment(path, names):
    seqs = prep23.read_fasta_subset(path, set(names))
    code = np.full(256, 255, dtype=np.uint8)
    for i, s in enumerate(STATES):
        code[ord(s)] = i
    return {n: code[np.frombuffer(seqs[n].encode(), dtype=np.uint8)] for n in seqs}


def load_site_rates(path, L):
    rates = {}
    for line in open(path):
        if line.startswith("#") or not line.strip() or line.split()[0].lower() == "site":
            continue
        p = line.split(); rates[int(p[0])] = float(p[1])
    arr = np.array([rates[i] for i in range(1, L + 1)])
    return arr / arr.mean()


def read_quartet(codes, q, gtr, site_rates, rate_bins, bin_rates, shuf_bins, rng, grid, subsets):
    """Observed reads for one quartet: returns dict of per-L success counts for U, W, S, U_RY, W_RY, and the
    full-length reads; also the quartet's valid-site count."""
    X = np.stack([codes[q[k]] for k in "ABCD"])  # 4 × Lmax
    valid = (X != 255).all(axis=0)
    idx_valid = np.where(valid)[0]
    Xv = X[:, idx_valid]
    m = np.stack([(Xv[i] != Xv[j]).astype(np.float32) for i, j in PAIRS])  # 6 × n
    d1 = m[2] + m[3] - m[0] - m[1]; d2 = m[4] + m[5] - m[0] - m[1]
    Xr = RY_MAP[Xv]
    mr = np.stack([(Xr[i] != Xr[j]).astype(np.float32) for i, j in PAIRS])
    d1r = mr[2] + mr[3] - mr[0] - mr[1]; d2r = mr[4] + mr[5] - mr[0] - mr[1]
    # per-bin weights from the exact model at this quartet's branches
    wb, wbr = np.zeros(len(bin_rates)), np.zeros(len(bin_rates))
    for k, r in enumerate(bin_rates):
        J = gtr.joint(q["branches"], r)
        s, v = site_stats(J, V1, V2); wb[k] = s / v
        sr, vr = site_stats(lump_ry(J), V1R, V2R); wbr[k] = sr / vr
    w_true = wb[rate_bins[idx_valid]]; w_shuf = wb[shuf_bins[idx_valid]]; w_ry = wbr[rate_bins[idx_valid]]
    out = {"n_valid": int(len(idx_valid))}
    def decide(dd1, dd2, w=None):
        if w is None:
            return (dd1.sum(-1) > 0) & (dd2.sum(-1) > 0)
        return ((dd1 * w).sum(-1) > 0) & ((dd2 * w).sum(-1) > 0)
    # full length
    out["full"] = {"U": int(decide(d1, d2)), "W": int(decide(d1, d2, w_true)), "S": int(decide(d1, d2, w_shuf)),
                   "U_RY": int(decide(d1r, d2r)), "W_RY": int(decide(d1r, d2r, w_ry))}
    for L in grid:
        if L > len(idx_valid):
            continue
        sub = np.stack([rng.choice(len(idx_valid), size=L, replace=False) for _ in range(subsets)])
        res = {}
        res["U"] = int(decide(d1[sub], d2[sub]).sum())
        res["W"] = int(decide(d1[sub], d2[sub], w_true[sub]).sum())
        res["S"] = int(decide(d1[sub], d2[sub], w_shuf[sub]).sum())
        res["U_RY"] = int(decide(d1r[sub], d2r[sub]).sum())
        res["W_RY"] = int(decide(d1r[sub], d2r[sub], w_ry[sub]).sum())
        out[str(L)] = res
    return out


def cmd_read(a):
    S = a.scratch
    qs = json.load(open(a.quartets))["quartets"]
    if a.smoke:
        qs = qs[:100]
    names = sorted({q[k] for q in qs for k in "ABCD"})
    codes = load_alignment(f"{S}/work/concat.fa", names)
    Lmax = len(next(iter(codes.values())))
    ex, pi, rates, weights = parse_model(f"{S}/work/iq.iqtree")
    gtr = GTR(ex, pi)
    site_rates = load_site_rates(f"{S}/work/iqr.rate", Lmax)
    # 40 quantile bins of the posterior-mean rates
    edges = np.quantile(site_rates, np.linspace(0, 1, 41)[1:-1])
    rate_bins = np.searchsorted(edges, site_rates)
    bin_rates = np.array([site_rates[rate_bins == k].mean() for k in range(40)])
    rng = np.random.default_rng(SEED)
    shuf_bins = rate_bins[rng.permutation(Lmax)]
    grid = [64, 128, 2048] if a.smoke else L_GRID
    subsets = 10 if a.smoke else 40
    out = {"L": grid, "subsets": subsets, "Lmax": Lmax, "smoke": a.smoke, "quartets": []}
    t0 = time.time()
    for i, q in enumerate(qs):
        r = read_quartet(codes, q, gtr, site_rates, rate_bins, bin_rates, shuf_bins, rng, grid, subsets)
        r["t"] = q["t"]; r["tau"] = q["tau"]
        out["quartets"].append(r)
        if i % 100 == 0:
            print(f"read {i}/{len(qs)} {time.time()-t0:.0f}s", flush=True)
    out["elapsed_s"] = time.time() - t0
    json.dump(out, open(a.out, "w"))
    print("done", len(qs), f"{out['elapsed_s']:.0f}s", flush=True)

# ------------------------------------------------------------------ prediction (parametric, no free parameter)

def predict_quartet(q, gtr, rates, weights, n_valid, grid, reps, rng):
    """Multinomial parametric simulation on the quartet's own branches with sites drawn from the R spectrum."""
    K = len(rates)
    P4, P2, w4, w2 = [], [], [], []
    for r in rates:
        J = gtr.joint(q["branches"], r)
        P4.append(J.reshape(-1)); s, v = site_stats(J, V1, V2); w4.append(s / v)
        J2 = lump_ry(J); P2.append(J2.reshape(-1)); s2, v2 = site_stats(J2, V1R, V2R); w2.append(s2 / v2)
    P4 = np.array(P4); P2 = np.array(P2); w4 = np.array(w4); w2 = np.array(w2)
    out = {}
    for L in list(grid) + ["full"]:
        n = n_valid if L == "full" else L
        if L != "full" and L > n_valid:
            continue
        nk = rng.multinomial(n, weights, size=reps)  # reps × K
        S1 = np.zeros(reps); S2 = np.zeros(reps); W1 = np.zeros(reps); W2 = np.zeros(reps)
        R1 = np.zeros(reps); R2 = np.zeros(reps); RW1 = np.zeros(reps); RW2 = np.zeros(reps)
        for k in range(K):
            c4 = rng.multinomial(nk[:, k], P4[k])      # reps × 256
            c2 = rng.multinomial(nk[:, k], P2[k])      # reps × 16
            a1 = c4 @ V1; a2 = c4 @ V2; b1 = c2 @ V1R; b2 = c2 @ V2R
            S1 += a1; S2 += a2; W1 += w4[k] * a1; W2 += w4[k] * a2
            R1 += b1; R2 += b2; RW1 += w2[k] * b1; RW2 += w2[k] * b2
        out[str(L)] = {"U": int(((S1 > 0) & (S2 > 0)).sum()), "W": int(((W1 > 0) & (W2 > 0)).sum()),
                       "U_RY": int(((R1 > 0) & (R2 > 0)).sum()), "W_RY": int(((RW1 > 0) & (RW2 > 0)).sum())}
    return out


def cmd_predict(a):
    S = a.scratch
    qs = json.load(open(a.quartets))["quartets"]
    reads = json.load(open(a.reads))
    if a.smoke:
        qs = qs[:100]
    ex, pi, rates, weights = parse_model(f"{S}/work/iq.iqtree")
    gtr = GTR(ex, pi)
    reps = 20 if a.smoke else 200
    rng = np.random.default_rng(SEED + 1)
    out = {"L": reads["L"], "reps": reps, "rates": rates.tolist(), "weights": weights.tolist(), "quartets": []}
    t0 = time.time()
    for i, (q, r) in enumerate(zip(qs, reads["quartets"])):
        p = predict_quartet(q, gtr, rates, weights, r["n_valid"], reads["L"], reps, rng)
        p["t"] = q["t"]; out["quartets"].append(p)
        if i % 100 == 0:
            print(f"predict {i}/{len(qs)} {time.time()-t0:.0f}s", flush=True)
    json.dump(out, open(a.out, "w"))
    print("done", f"{time.time()-t0:.0f}s", flush=True)

# ------------------------------------------------------------------ estimator: plateau-normalised isotonic depth

def pava_decreasing(x, y, w):
    """Weighted isotonic regression, non-increasing in x (x sorted ascending)."""
    order = np.argsort(x); y = y[order].astype(float); w = w[order].astype(float)
    # fit non-decreasing on -y then negate
    yy = -y
    vals, wts, cnt = [], [], []
    for yi, wi in zip(yy, w):
        vals.append(yi); wts.append(wi); cnt.append(1)
        while len(vals) > 1 and vals[-2] > vals[-1]:
            v = (vals[-1] * wts[-1] + vals[-2] * wts[-2]) / (wts[-1] + wts[-2])
            wsum = wts[-1] + wts[-2]; c = cnt[-1] + cnt[-2]
            vals.pop(); wts.pop(); cnt.pop(); vals[-1] = v; wts[-1] = wsum; cnt[-1] = c
    fit = np.concatenate([np.full(c, -v) for v, c in zip(vals, cnt)])
    return x[order], fit


def tstar_curve(t, succ, nsub, full_succ, full_n, level=0.75):
    """Readable depth: first depth where iso(success_L)/iso(full-length success) ≤ level; None if no interior crossing."""
    xs, fL = pava_decreasing(t, succ / np.maximum(nsub, 1), nsub)
    _, fF = pava_decreasing(t, full_succ / np.maximum(full_n, 1), full_n)
    ratio = fL / np.maximum(fF, 1e-9)
    if ratio[0] <= level:
        return None  # no interior crossing at the shallow end
    below = np.where(ratio <= level)[0]
    if len(below) == 0:
        return None  # never crosses within the depth range
    i = below[0]
    return float(np.sqrt(xs[i - 1] * xs[i])) if i > 0 else float(xs[i])


def curves(pack, grid, readers, key_sub, full_n_value):
    """pack: list of per-quartet dicts with str(L) -> {reader: count} and 'full' -> {reader: count};
    key_sub = trials per subsampled cell (subsets or replicates), full_n_value = trials in the full-length cell
    (1 for the observed deterministic read, reps for the prediction)."""
    t = np.array([q["t"] for q in pack])
    out = {}
    for name in readers:
        full = np.array([q["full"][name] for q in pack], float)
        full_n = np.full(len(pack), float(full_n_value))
        for L in grid:
            have = np.array([str(L) in q for q in pack])
            if have.sum() < 50:
                out[f"{name}|{L}"] = None; continue
            s = np.array([q[str(L)][name] if str(L) in q else 0 for q in pack], float)
            n = np.where(have, key_sub, 0).astype(float)
            out[f"{name}|{L}"] = tstar_curve(t[have], s[have], n[have], full[have], full_n[have])
    return out


def cmd_score(a):
    reads = json.load(open(a.reads)); pred = json.load(open(a.pred))
    grid = reads["L"]
    obs = curves(reads["quartets"], grid, ["U", "W", "S", "U_RY", "W_RY"], reads["subsets"], 1)
    prd = curves(pred["quartets"], grid, ["U", "W", "U_RY", "W_RY"], pred["reps"], pred["reps"])
    rep = {"observed_tstar": obs, "predicted_tstar": prd, "verdicts": {}, "readings": {}}
    def resolved(name, L):
        return obs.get(f"{name}|{L}") is not None and prd.get(f"{name}|{L}") is not None
    def form(name, tol, Lmin):
        errs, ok = {}, True
        for L in grid:
            if L < Lmin:
                continue
            if not resolved(name, L):
                errs[str(L)] = None; ok = False; continue
            e = (obs[f"{name}|{L}"] - prd[f"{name}|{L}"]) / prd[f"{name}|{L}"]
            errs[str(L)] = e
            if abs(e) > tol:
                ok = False
        return ok, errs
    ok1, e1 = form("U", 0.20, 128); ok2, e2 = form("W", 0.20, 128)
    rep["verdicts"]["V1_form_unweighted"] = {"pass": ok1, "rel_err": e1}
    rep["verdicts"]["V2_form_weighted"] = {"pass": ok2, "rel_err": e2}
    ratios_o, ratios_p, ok3 = {}, {}, True
    Ls = [L for L in grid if L >= 128]
    for L in Ls:
        if resolved("U", L) and resolved("W", L):
            ratios_o[str(L)] = obs[f"W|{L}"] / obs[f"U|{L}"]; ratios_p[str(L)] = prd[f"W|{L}"] / prd[f"U|{L}"]
            if not obs[f"W|{L}"] > obs[f"U|{L}"]:
                ok3 = False
        else:
            ratios_o[str(L)] = None; ok3 = False
    if ok3 and ratios_o:
        ok3 = ratios_o[str(Ls[-1])] > ratios_o["128"] and ratios_p[str(Ls[-1])] > ratios_p["128"]
    rep["verdicts"]["V3_ordering"] = {"pass": ok3, "observed_ratio": ratios_o, "predicted_ratio": ratios_p}
    def slope(name, which):
        res = [L for L in grid if (obs if which == "o" else prd).get(f"{name}|{L}") is not None][-3:]
        if len(res) < 3:
            return None, res
        src = obs if which == "o" else prd
        x = np.log([float(L) for L in res]); y = np.log([src[f"{name}|{L}"] for L in res])
        return float(np.polyfit(x, y, 1)[0]), res
    v4, ok4 = {}, True
    for name in ("U", "W"):
        so, lo = slope(name, "o"); sp, lp = slope(name, "p")
        v4[name] = {"obs": so, "pred": sp, "L_obs": lo, "L_pred": lp}
        if so is None or sp is None or abs(so - sp) > 0.06:
            ok4 = False
    rep["verdicts"]["V4_exponent"] = {"pass": ok4, "slopes": v4}
    v5, ok5 = {}, True
    for L in grid:
        if L < 256:
            continue
        if obs.get(f"S|{L}") is None or obs.get(f"U|{L}") is None:
            v5[str(L)] = None; ok5 = False; continue
        d = obs[f"S|{L}"] / obs[f"U|{L}"] - 1; v5[str(L)] = d
        if abs(d) > 0.15:
            ok5 = False
    rep["verdicts"]["V5_shuffle"] = {"pass": ok5, "rel_diff": v5}
    ok6a, e6a = form("U_RY", 0.25, 128); ok6b, e6b = form("W_RY", 0.25, 128)
    rep["verdicts"]["V6_RY_arm"] = {"pass": ok6a and ok6b, "rel_err_U": e6a, "rel_err_W": e6b, "decisive": False}
    rep["overall"] = "LAW SUPPORTED ON REAL DATA" if all(rep["verdicts"][k]["pass"] for k in
        ("V1_form_unweighted", "V2_form_weighted", "V3_ordering", "V4_exponent", "V5_shuffle")) else "NOT SUPPORTED AS REGISTERED"
    # readings: plateau by bin, Gamma fit of the R spectrum
    rates, weights = np.array(pred["rates"]), np.array(pred["weights"])
    def gamma_nll(alpha):
        from math import lgamma
        return -float(np.sum(weights * ((alpha - 1) * np.log(rates) - alpha * rates + alpha * np.log(alpha) - lgamma(alpha))))
    al = np.exp(np.linspace(np.log(0.05), np.log(20), 600)); nll = [gamma_nll(x) for x in al]
    alpha = float(al[int(np.argmin(nll))])
    t = np.array([q["t"] for q in reads["quartets"]])
    bins = np.digitize(t, BINS) - 1
    plateau = {str(b): float(np.mean([q["full"]["U"] for q, bb in zip(reads["quartets"], bins) if bb == b]))
               for b in range(8) if (bins == b).any()}
    rep["readings"] = {"gamma_shape_of_R_spectrum": alpha, "asymptote_unweighted": 1 / (2 * (alpha + 1)),
                       "asymptote_weighted": 1 / (alpha + 2), "regime_depth_3a_over_8": 3 * alpha / 8,
                       "full_length_recovery_U_by_bin": plateau, "n_quartets": len(reads["quartets"]), "Lmax": reads["Lmax"]}
    json.dump(rep, open(a.out, "w"), indent=1)
    for k, v in rep["verdicts"].items():
        print(k, "PASS" if v["pass"] else "FAIL")
    print(rep["overall"]); print(json.dumps(rep["readings"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("quartets", "read", "predict", "score"):
        p = sub.add_parser(name); p.add_argument("--scratch", required=True); p.add_argument("--out", required=True)
        p.add_argument("--quartets"); p.add_argument("--reads"); p.add_argument("--pred"); p.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    {"quartets": cmd_quartets, "read": cmd_read, "predict": cmd_predict, "score": cmd_score}[args.cmd](args)
