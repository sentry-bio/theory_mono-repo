"""E-D (PREREG2.md): trait kernels fitted inside one family at a time; predictions saved before observation."""
import hashlib
import json
import time

import numpy as np

import atlas_predict as ap
from atlas_predict2 import MatKernel, clt_predict

A = ap.A
OUT = "/Users/rohitfenn/Documents/addressability-atlas-2026-09-26"
ap.rng = np.random.default_rng(260926)
rng = ap.rng


def group(idx, labels):
    g = {}
    for i in idx:
        g.setdefault(labels[i], []).append(i)
    return {k: np.array(v) for k, v in g.items()}


def pairs_within(idx, labels, n):
    g = [v for v in group(idx, labels).values() if len(v) >= 2]
    if not g:
        return np.array([], int), np.array([], int)
    sz = np.array([len(v) for v in g], float)
    pick = rng.choice(len(g), n, p=sz / sz.sum())
    P = np.array([rng.choice(g[k], 2, replace=False) for k in pick])
    return P[:, 0], P[:, 1]


def quartets(te, lab, kind, n):
    gen = group(te, lab["g"])
    names = [k for k, v in gen.items() if len(v) >= (2 if kind == "G" else 1)]
    need = 2 if kind == "G" else 4
    if len(names) < need:
        return np.zeros((0, 4), int)
    out = []
    for _ in range(n):
        ch = rng.choice(len(names), need, replace=False)
        if kind == "G":
            q = list(rng.choice(gen[names[ch[0]]], 2, replace=False)) + list(rng.choice(gen[names[ch[1]]], 2, replace=False))
        else:
            q = [rng.choice(gen[names[c]]) for c in ch]
        out.append(q)
    return np.array(out)


def four_point_ok(X, Q):
    V = X[Q]
    d = lambda i, j: ((V[:, i] - V[:, j]) ** 2).sum(1)
    S = np.stack([d(0, 1) + d(2, 3), d(0, 2) + d(1, 3), d(0, 3) + d(1, 2)], 1)
    return S.argmin(1) == 0


if __name__ == "__main__":
    t0 = time.time()
    z, rows, leaves, T, lab, train = ap.load()
    s1 = np.load(f"{A}/atlas_predictions.npz")
    f1 = np.load(f"{A}/atlas_predictions_full.npz")
    X = z[rows] @ s1["P"]
    pooled = MatKernel(f1["centers"], f1["Gam"], f1["Sig"])
    fam_counts = {f: c for f, c in zip(*np.unique(lab["f"], return_counts=True)) if c >= 300}
    edges = np.geomspace(0.003, 1.5, 19)
    recs, fams = [], {}
    for fam in sorted(fam_counts):
        idx = np.flatnonzero(lab["f"] == fam)
        tr_mask = np.array([int(hashlib.md5(("E-D:" + g).encode()).hexdigest(), 16) % 2 == 0 for g in lab["g"][idx]])
        tr, te = idx[tr_mask], idx[~tr_mask]
        if len(tr) < 100 or len(set(lab["g"][te])) < 4:
            continue
        I1, J1 = pairs_within(tr, lab["g"], 20_000)
        I2, J2 = pairs_within(tr, lab["f"], 20_000)
        I, J = np.concatenate([I1, I2]), np.concatenate([J1, J2])
        tau = ap.patristic(T, leaves[I], leaves[J])
        b = np.digitize(tau, edges) - 1
        cen, Gam = [], []
        for k in range(len(edges) - 1):
            m = b == k
            if m.sum() >= 150:
                D = X[I[m]] - X[J[m]]
                Gam.append(D.T @ D / (2 * m.sum())); cen.append(np.exp(np.log(tau[m]).mean()))
        if len(cen) < 3:
            continue
        Sig = np.cov(X[tr].T)
        mk = MatKernel(np.array(cen), np.array(Gam), Sig)
        frac = np.array([np.trace(G) for G in Gam]) / np.trace(Sig)
        t_half = float(np.exp(np.interp(0.5, frac, np.log(cen)))) if frac.max() >= 0.5 and frac.min() < 0.5 else float("nan")
        m = (tau < 0.3)
        D = X[I[m]] - X[J[m]]
        w, V = np.linalg.eigh(D.T @ D / max(len(D), 1)); p = D @ V[:, -3:]
        kurt = float(np.max(((p - p.mean(0)) ** 4).mean(0) / p.var(0) ** 2 - 3)) if len(D) > 100 else float("nan")
        fams[fam] = dict(n=len(idx), n_train=len(tr), t_half=t_half, kurtosis_max=kurt)
        for kind in ("G", "F4"):
            Q = quartets(te, lab, kind, 300)
            if not len(Q):
                continue
            Q, t6, t, dl = ap.orient(Q, T, leaves)
            pf = clt_predict(t6, mk.S, Sig)
            pp = clt_predict(t6, pooled.S, pooled.Sig)
            for k in range(len(Q)):
                recs.append((fam, kind, float(t[k]), float(dl[k]), float(pf[k]), float(pp[k]), Q[k].tolist()))
        print(f"{fam:28s} n={len(idx):5d} train={len(tr):4d} τ½={t_half:.3f} kurt={kurt:5.1f}  ({time.time()-t0:.0f}s)", flush=True)
    json.dump(dict(written=time.strftime("%Y-%m-%d %H:%M:%S"), families=fams, quartets=recs),
              open(f"{OUT}/expD_predictions.json", "w"))
    print(f"predictions saved ({len(recs)} quartets, {len(fams)} families)")

    # ---- observation (only after predictions are on disk) ----
    fam_, kind_, t_, dl_, pf_, pp_, Q_ = zip(*recs)
    t_, pf_, pp_ = map(np.array, (t_, pf_, pp_))
    ok = four_point_ok(X, np.array(Q_))
    fam_, kind_ = np.array(fam_), np.array(kind_)
    eb = np.geomspace(0.01, 0.6, 10)
    b = np.digitize(t_, eb) - 1
    print("\nD-a  t-bin        n   observed  family-kernel  pooled-kernel")
    errs, worst = [], 0.0
    for k in range(len(eb) - 1):
        m = b == k
        if m.sum() < 150:
            continue
        e = ok[m].mean() - pf_[m].mean(); errs.append(abs(e)); worst = max(worst, abs(e))
        print(f"     {eb[k]:.3f}-{eb[k+1]:.3f} {m.sum():5d}   {ok[m].mean():.3f}     {pf_[m].mean():.3f}         {pp_[m].mean():.3f}")
    mae = float(np.mean(errs))
    da = "PASS" if worst <= 0.05 and mae <= 0.03 else ("PARTIAL" if mae <= 0.05 else "FAIL")
    print(f"     mean |error| {mae:.3f}, worst {worst:.3f} -> D-a {da}")
    from scipy.stats import spearmanr
    rows_b = []
    for fam in fams:
        m = (fam_ == fam) & (kind_ == "F4")
        if m.sum() >= 50:
            rows_b.append((fam, ok[m].mean(), pf_[m].mean(), pp_[m].mean()))
    _, o, pfm, ppm = map(np.array, zip(*rows_b))
    rho = spearmanr(pfm, o).correlation
    mae_f, mae_p = np.mean(np.abs(o - pfm)), np.mean(np.abs(o - ppm))
    db = "PASS" if rho >= 0.6 and mae_f <= 0.75 * mae_p else "FAIL"
    print(f"D-b  {len(rows_b)} families: Spearman(pred, obs) {rho:.2f}; mean |error| family {mae_f:.3f} vs pooled {mae_p:.3f} -> D-b {db}")
    th = np.array([v["t_half"] for v in fams.values()])
    s = float(np.nanstd(np.log(th[np.isfinite(th)])))
    print(f"family τ½: median {np.nanmedian(th):.3f}, SD of log τ½ = {s:.2f} (feeds E-B′)")
    json.dump(dict(D_a=da, D_a_mae=mae, D_a_worst=worst, D_b=db, D_b_spearman=float(rho), D_b_mae_family=float(mae_f),
                   D_b_mae_pooled=float(mae_p), sd_log_t_half=s, families=fams,
                   per_family=[dict(family=r[0], obs=float(r[1]), pred_family=float(r[2]), pred_pooled=float(r[3])) for r in rows_b]),
              open(f"{OUT}/expD_results.json", "w"), indent=1)
