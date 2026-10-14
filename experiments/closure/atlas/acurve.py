"""A-curve / A-arch (PREREG9): one family image predicts packing curves (AC1), quartets (AC2), retrieval (AC3).

Usage: acurve.py bac|ar
"""
import hashlib
import json
import sys
import time

import numpy as np

import atlas_predict as ap
import exp_D_family as E
from atlas_data import build, core, patristic, taxonomy
from atlas_predict2 import MatKernel, clt_predict
from k2_packing import greedy_pack, joint_draw

A = ap.A
OUT = "/Users/rohitfenn/Documents/addressability-atlas-2026-09-26"
EDGES = np.geomspace(0.003, 1.5, 19)
EPS = [0.4, 0.6, 0.79, 1.0, 1.25, 1.6, 2.0]
TBINS = np.geomspace(0.01, 0.6, 10)


def load_domain(dom):
    Z = np.load(f"{A}/catalogue_coordinates.npz"); acc, z = Z["accession"], Z["z"]
    T = build(f"{A}/{'bac120' if dom == 'bac' else 'ar53'}_r220.tree")
    leaf_of = {core(T["name"][v]): v for v in np.flatnonzero(T["is_leaf"])}
    rows, leaves, seen = [], [], set()
    for i, a in enumerate(acc):
        v = leaf_of.get(core(a))
        if v is not None and v not in seen:
            rows.append(i); leaves.append(v); seen.add(v)
    rows, leaves = np.array(rows), np.array(leaves)
    tax = taxonomy()
    lab = {r: np.array([tax[core(T["name"][v])][r] for v in leaves]) for r in "pcofg"}
    train = np.array([int(hashlib.md5(("E-D:" + g).encode()).hexdigest(), 16) % 2 == 0 for g in lab["g"]])
    X = z[rows]
    if dom == "bac":
        X = X @ np.load(f"{A}/atlas_predictions.npz")["P"]
    return X, rows, leaves, T, lab, train


def variogram(X, T, leaves, I, J, edges, minpairs):
    tau = patristic(T, leaves[I], leaves[J]); b = np.digitize(tau, edges) - 1
    cen, Gam = [], []
    for k in range(len(edges) - 1):
        m = b == k
        if m.sum() >= minpairs:
            Dm = X[I[m]] - X[J[m]]; Gam.append(Dm.T @ Dm / (2 * m.sum())); cen.append(np.exp(np.log(tau[m]).mean()))
    return np.array(cen), np.array(Gam)


def pooled_process(X, T, leaves, lab, tr):
    E.rng = np.random.default_rng(20260925)
    I, J = [], []
    for rank in ["g", "f", "o", "c", "p"]:
        i, j = E.pairs_within(tr, lab[rank], 40_000); I.append(i); J.append(j)
    i, j = E.rng.choice(tr, 40_000), E.rng.choice(tr, 40_000); m = i != j; I.append(i[m]); J.append(j[m])
    I, J = np.concatenate(I), np.concatenate(J)
    cen, Gam = variogram(X, T, leaves, I, J, np.geomspace(0.003, 4.0, 31), 500)
    Sig = np.cov(X[tr].T)
    return MatKernel(cen, Gam, Sig), Sig


def pair_tau(T, leaves, gi):
    n = len(gi); lv = leaves[gi]; tau = np.zeros((n, n))
    for i in range(n - 1):
        tau[i, i + 1:] = patristic(T, np.repeat(lv[i], n - i - 1), lv[i + 1:]); tau[i + 1:, i] = tau[i, i + 1:]
    return tau


if __name__ == "__main__":
    dom = sys.argv[1]
    t0 = time.time()
    X, rows, leaves, T, lab, train = load_domain(dom)
    tr_all = np.flatnonzero(train)
    minfam, mintrain, mingen_te, mingen = (300, 100, 4, 10) if dom == "bac" else (100, 50, 3, 6)
    pooled, Sig_pool = pooled_process(X, T, leaves, lab, tr_all)
    Gam_pool = lambda t: Sig_pool - pooled.S(np.array([t]))[0]
    fams = [f for f, n in zip(*np.unique(lab["f"], return_counts=True)) if n >= minfam]
    ac1, ac2, ac3 = [], [], []
    for fam in sorted(fams):
        idx = np.flatnonzero(lab["f"] == fam); tr = idx[train[idx]]; te = idx[~train[idx]]
        if len(tr) < mintrain or len(set(lab["g"][te])) < mingen_te:
            continue
        E.rng = np.random.default_rng(260926)
        I1, J1 = E.pairs_within(tr, lab["g"], 20_000); I2, J2 = E.pairs_within(tr, lab["f"], 20_000)
        cen, Gam = variogram(X, T, leaves, np.concatenate([I1, I2]), np.concatenate([J1, J2]), EDGES, 150)
        if len(cen) < 3:
            continue
        Sig = np.cov(X[tr].T); fk = MatKernel(cen, Gam, Sig)
        scale = np.trace(Gam[0]) / np.trace(Gam_pool(cen[0]))

        def S_fam(tt, fk=fk, cen=cen, Sig=Sig, scale=scale):
            out = fk.S(tt)
            for q, t in enumerate(np.atleast_1d(tt)):
                if t < cen[0]:
                    out[q] = Sig - scale * Gam_pool(t)
            return out

        # AC1: packing curves on test genera
        rng = np.random.default_rng(9001)
        for g in sorted(set(lab["g"][te])):
            gi = te[lab["g"][te] == g]
            if len(gi) < mingen:
                continue
            if len(gi) > 30:
                gi = rng.choice(gi, 30, replace=False)
            tau = pair_tau(T, leaves, gi)
            Zf, _ = joint_draw(S_fam, Sig, tau, rng, 200); Zp, _ = joint_draw(pooled.S, Sig_pool, tau, rng, 200)
            rec = dict(family=fam, genus=g, n=len(gi))
            for e in EPS:
                rec[f"obs|{e}"] = greedy_pack(X[gi], e)
                rec[f"fam|{e}"] = float(np.mean([greedy_pack(Zf[r], e) for r in range(200)]))
                rec[f"pool|{e}"] = float(np.mean([greedy_pack(Zp[r], e) for r in range(200)]))
            ac1.append(rec)
        if dom == "bac":
            # AC2: new F4 quartets
            E.rng = np.random.default_rng(9002)
            Q = E.quartets(te, lab, "F4", 300)
            if len(Q):
                Q, t6, t, dl = ap.orient(Q, T, leaves)
                ok = E.four_point_ok(X, Q); p = clt_predict(t6, S_fam, Sig)
                ac2 += [(fam, float(t[k]), int(ok[k]), float(p[k])) for k in range(len(Q))]
            # AC3: retrieval among 60 test genomes
            rng3 = np.random.default_rng(9003)
            if len(te) >= 20 and len(set(lab["g"][te])) >= 2:
                sel = rng3.choice(te, min(60, len(te)), replace=False)
                tau = pair_tau(T, leaves, sel); same = lab["g"][sel][:, None] == lab["g"][sel][None, :]
                np.fill_diagonal(same, False)

                def nn_same(V):
                    D = ((V[:, None, :] - V[None, :, :]) ** 2).sum(-1); np.fill_diagonal(D, np.inf)
                    return float(same[np.arange(len(V)), D.argmin(1)].mean())
                Zs, _ = joint_draw(S_fam, Sig, tau, rng3, 50)
                ac3.append(dict(family=fam, n=len(sel), obs=nn_same(X[sel]), pred=float(np.mean([nn_same(Zs[r]) for r in range(50)]))))
        print(f"{fam:24s} genera {sum(r['family'] == fam for r in ac1):3d}  ({time.time()-t0:.0f}s)", flush=True)

    # ---- scoring ----
    print(f"\nAC1 packing curves ({len(ac1)} test genera, {dom}): ε | ΣN | Σobs | Σfam | Σpool | log-err fam / pool | median per-genus |err| fam")
    ac1_ok, base_fail = True, False
    N = sum(r["n"] for r in ac1)
    for e in EPS:
        o = sum(r[f"obs|{e}"] for r in ac1); f_ = sum(r[f"fam|{e}"] for r in ac1); p_ = sum(r[f"pool|{e}"] for r in ac1)
        ef, ep, ea = np.log(o / f_), np.log(o / p_), np.log(o / N)
        med = float(np.median([abs(np.log(max(r[f"obs|{e}"], 1) / max(r[f"fam|{e}"], 1e-9))) for r in ac1]))
        if abs(ef) > 0.15 or (e >= 1.0 and med > 0.25):
            ac1_ok = False
        if e >= 1.0 and abs(ef) <= 0.15 and (abs(ep) > 0.15 or abs(ea) > 0.15):
            base_fail = True
        print(f"   {e:.2f} | {N:5d} | {o:5d} | {f_:8.1f} | {p_:8.1f} | {ef:+.3f} / {ep:+.3f} (all-distinct {ea:+.3f}) | {med:.3f}")
    verdict_parts = dict(AC1=ac1_ok, AC1_baseline_fails=base_fail)
    if dom == "bac":
        fam_, t_, ok_, p_ = map(np.array, zip(*ac2)); b = np.digitize(t_, TBINS) - 1
        print("\nAC2 quartets: t-bin | n | observed | predicted")
        errs, worst = [], 0.0
        for k in range(len(TBINS) - 1):
            m = b == k
            if m.sum() < 150:
                continue
            e_ = ok_[m].mean() - p_[m].mean(); errs.append(abs(e_)); worst = max(worst, abs(e_))
            print(f"   {TBINS[k]:.3f}-{TBINS[k+1]:.3f} | {m.sum():5d} | {ok_[m].mean():.3f} | {p_[m].mean():.3f}")
        ac2_ok = worst <= 0.05 and np.mean(errs) <= 0.03
        print(f"   worst {worst:.3f}, mean {np.mean(errs):.3f} -> AC2 {'PASS' if ac2_ok else 'FAIL'}")
        o3 = np.mean([r["obs"] for r in ac3]); p3 = np.mean([r["pred"] for r in ac3]); e3 = np.mean([abs(r["obs"] - r["pred"]) for r in ac3])
        ac3_ok = abs(o3 - p3) <= 0.05 and e3 <= 0.10
        print(f"\nAC3 retrieval ({len(ac3)} families): pooled same-genus NN observed {o3:.3f} vs predicted {p3:.3f}; per-family mean |error| {e3:.3f} -> AC3 {'PASS' if ac3_ok else 'FAIL'}")
        verdict_parts.update(AC2=ac2_ok, AC3=ac3_ok)
        fails_ge1 = sum(1 for e in EPS if e >= 1.0 and abs(np.log(sum(r[f"obs|{e}"] for r in ac1) / sum(r[f"fam|{e}"] for r in ac1))) > 0.15)
        verdict = "CONFIRMED" if ac1_ok and ac2_ok and ac3_ok and base_fail else ("PARTIAL" if ac1_ok else ("REFUTED" if fails_ge1 >= 2 else "NOT CONFIRMED"))
    else:
        verdict = "PASS" if ac1_ok else "FAIL"
    print(f"\nA-{dom} verdict: {verdict}  ({time.time()-t0:.0f}s)")
    json.dump(dict(ac1=ac1, ac2=ac2, ac3=ac3, parts=verdict_parts, verdict=verdict), open(f"{OUT}/acurve_{dom}_results.json", "w"), indent=1, default=float)
