"""PREREG21: composition's horizon on the Atlas kernels — a pairwise reader against an ancestor-aware reader at every
qualifying family's deepest split, both predicted from A-curve's frozen family kernel with nothing fitted.

Usage: python3 horizon21.py bac|ar [smoke]   (run from horizon21/; imports the staged Atlas scripts in closure/atlas)
Writes horizon21_<dom>.json and prints the per-family table and the H1–H3 scores."""
import hashlib
import json
import os
import sys
import time

import numpy as np
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS = os.path.join(os.path.dirname(HERE), "closure", "atlas")
sys.path.insert(0, ATLAS)
import atlas_predict as ap  # noqa: E402
import exp_D_family as E  # noqa: E402
from acurve import EDGES, load_domain, pair_tau, pooled_process, variogram  # noqa: E402
from atlas_data import lca  # noqa: E402
from atlas_predict2 import MatKernel  # noqa: E402
from k2_packing import joint_draw  # noqa: E402

A = ap.A
SMOKE = "smoke" in sys.argv[2:]
CAP, NQ, REPS = 30, 200, (10 if SMOKE else 100)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def children_of(T):
    kids = {}
    for v, p in enumerate(T["parent"]):
        if p >= 0:
            kids.setdefault(int(p), []).append(int(v))
    return kids


def mrca(T, lv):
    """Most recent common ancestor of the leaves lv, by pairwise folding of the vectorised lca."""
    anc = np.asarray(lv)
    while len(anc) > 1:
        a, b = anc[0::2], anc[1::2]
        m = len(b)
        anc = np.concatenate([lca(T, a[:m], b), a[m:]])
    return int(anc[0])


def under(T, lv, node):
    """Mask of leaves lv that lie below `node` (lca(leaf, node) == node)."""
    return lca(T, lv, np.full(len(lv), node)) == node


def deepest_split(T, kids, lv, mingen):
    """Descend from the MRCA until both of the two largest child clades carry >= mingen of the family's leaves."""
    node = mrca(T, lv)
    while True:
        ch = kids.get(node, [])
        if len(ch) < 2:
            return None
        masks = [under(T, lv, c) for c in ch]
        order = np.argsort([-m.sum() for m in masks])
        mA, mB = masks[order[0]], masks[order[1]]
        if mA.sum() >= mingen and mB.sum() >= mingen:
            return node, mA, mB
        if mA.sum() < mingen:
            return None
        node = ch[order[0]]


def four_point_acc(V, qa, qb):
    """Fraction of quartets (a1 a2 | b1 b2) resolved as that split by the four-point method on Euclidean distances."""
    D = np.sqrt(((V[:, None, :] - V[None, :, :]) ** 2).sum(-1))
    ok = 0
    for (a1, a2), (b1, b2) in zip(qa, qb):
        s0 = D[a1, a2] + D[b1, b2]; s1 = D[a1, b1] + D[a2, b2]; s2 = D[a1, b2] + D[a2, b1]
        ok += int(s0 < s1 and s0 < s2)
    return ok / len(qa)


def centroid_acc(V, side):
    """Leave-one-out centroid classification: side is a boolean array (True = A)."""
    nA, nB = side.sum(), (~side).sum()
    sA, sB = V[side].sum(0), V[~side].sum(0)
    ok = 0
    for i in range(len(V)):
        if side[i]:
            cA = (sA - V[i]) / (nA - 1); cB = sB / nB
            ok += int(((V[i] - cA) ** 2).sum() < ((V[i] - cB) ** 2).sum())
        else:
            cA = sA / nA; cB = (sB - V[i]) / (nB - 1)
            ok += int(((V[i] - cB) ** 2).sum() < ((V[i] - cA) ** 2).sum())
    return ok / len(V)


def main():
    dom = sys.argv[1]
    t0 = time.time()
    tag = f"{dom}_smoke" if SMOKE else dom
    with open(f"{HERE}/run.log", "a") as log:
        log.write(f"PREREG21 {tag} frozen sha256:\n" + "".join(
            f"{sha(os.path.join(ATLAS, f))}  {f}\n" for f in
            ("acurve.py", "k2_packing.py", "exp_D_family.py", "atlas_predict.py", "atlas_predict2.py", "atlas_data.py"))
            + f"{sha(os.path.abspath(__file__))}  horizon21.py\n{time.ctime()}\n")
    X, rows, leaves, T, lab, train = load_domain(dom)
    kids = children_of(T)
    tr_all = np.flatnonzero(train)
    minfam, mintrain, mingen_te, mingen = (300, 100, 4, 10) if dom == "bac" else (100, 50, 3, 6)
    pooled, Sig_pool = pooled_process(X, T, leaves, lab, tr_all)
    Gam_pool = lambda t: Sig_pool - pooled.S(np.array([t]))[0]
    fams = [f for f, n in zip(*np.unique(lab["f"], return_counts=True)) if n >= minfam]
    recs = []
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

        # the trait's rates
        trS = float(np.trace(Sig))
        ratios = np.array([np.trace(G) / trS for G in Gam])
        ok = (ratios > 0.05) & (ratios < 0.95)
        theta = float(np.median(-np.log(1 - ratios[ok]) / (2 * cen[ok]))) if ok.any() else float("nan")
        lv = leaves[idx]
        root = mrca(T, lv)
        depth_mean = float((T["depth"][lv] - T["depth"][root]).mean())
        beta = float(np.log(len(idx)) / depth_mean) if depth_mean > 0 else float("nan")

        # amendment 9 Oct (before the full run): the split's sides are drawn from TEST genera only, held out from
        # the kernel fit as in A-curve; the MRCA, depth and rates above use the whole family
        lv_te = leaves[te]
        split = deepest_split(T, kids, lv_te, mingen)
        if split is None:
            print(f"{fam:24s} no qualifying split among test genera", flush=True)
            continue
        node, mA, mB = split
        rng = np.random.default_rng(21001)
        iA = te[mA]; iB = te[mB]
        if len(iA) > CAP:
            iA = rng.choice(iA, CAP, replace=False)
        if len(iB) > CAP:
            iB = rng.choice(iB, CAP, replace=False)
        sel = np.concatenate([iA, iB]); side = np.zeros(len(sel), bool); side[:len(iA)] = True
        rngq = np.random.default_rng(21002)
        qa = [tuple(rngq.choice(len(iA), 2, replace=False)) for _ in range(NQ)]
        qb = [tuple(len(iA) + rngq.choice(len(iB), 2, replace=False)) for _ in range(NQ)]
        V = X[sel]
        obs_q = four_point_acc(V, qa, qb); obs_c = centroid_acc(V, side)
        tau = pair_tau(T, leaves, sel)
        Z, clipped = joint_draw(S_fam, Sig, tau, np.random.default_rng(21003), REPS)
        pq = np.array([four_point_acc(Z[k], qa, qb) for k in range(REPS)])
        pc = np.array([centroid_acc(Z[k], side) for k in range(REPS)])
        split_depth = float((T["depth"][leaves[sel]] - T["depth"][node]).mean())
        rec = dict(family=fam, n_family=int(len(idx)), nA=int(len(iA)), nB=int(len(iB)), theta=theta, beta=beta,
                   line=beta - 2 * theta, split_depth=split_depth, family_depth=depth_mean, clipped=clipped,
                   obs_quartet=obs_q, obs_centroid=obs_c, pred_quartet=float(pq.mean()), pred_quartet_sd=float(pq.std()),
                   pred_centroid=float(pc.mean()), pred_centroid_sd=float(pc.std()))
        recs.append(rec)
        print(f"{fam:24s} n {len(idx):4d} split {len(iA):2d}|{len(iB):2d} depth {split_depth:.3f}  θ {theta:.2f} β {beta:.2f} "
              f"β−2θ {beta-2*theta:+.2f} | quartet obs {obs_q:.3f} pred {pq.mean():.3f}±{pq.std():.3f} | centroid obs {obs_c:.3f} "
              f"pred {pc.mean():.3f}±{pc.std():.3f}  ({time.time()-t0:.0f}s)", flush=True)
        if SMOKE:
            break

    # ---- scoring ----
    R = recs
    out = dict(dom=dom, tag=tag, families=R, n_families=len(R))
    if R:
        oq = np.array([r["obs_quartet"] for r in R]); pq_ = np.array([r["pred_quartet"] for r in R])
        oc = np.array([r["obs_centroid"] for r in R]); pc_ = np.array([r["pred_centroid"] for r in R])
        h1 = (abs(oq.mean() - pq_.mean()) <= 0.05 and abs(oc.mean() - pc_.mean()) <= 0.05
              and np.median(abs(oq - pq_)) <= 0.10 and np.median(abs(oc - pc_)) <= 0.10)
        adv_obs = oc - oq; adv_pred = pc_ - pq_
        h2 = (np.mean(adv_obs > 0) >= 0.80) and (np.mean(abs(adv_obs - adv_pred) <= 0.10) >= 0.70)
        line = np.array([r["line"] for r in R]); fin = np.isfinite(line)
        rho = float(spearmanr(line[fin], oc[fin]).correlation) if fin.sum() >= 5 else float("nan")
        h3 = bool(rho >= 0.4)
        verdict = "HORIZON READ" if (h1 and h2) else ("PARTIAL" if (h1 or h2) else "FAIL")
        out.update(H1=bool(h1), H2=bool(h2), H3=h3, spearman_line_centroid=rho, verdict=verdict,
                   pooled=dict(obs_quartet=float(oq.mean()), pred_quartet=float(pq_.mean()), obs_centroid=float(oc.mean()),
                               pred_centroid=float(pc_.mean()), median_abs_err_quartet=float(np.median(abs(oq - pq_))),
                               median_abs_err_centroid=float(np.median(abs(oc - pc_))), frac_adv_positive=float(np.mean(adv_obs > 0)),
                               frac_adv_within=float(np.mean(abs(adv_obs - adv_pred) <= 0.10)),
                               families_above_line=int((line > 0).sum()), families_below_line=int((line <= 0).sum())))
        print(f"\n[{tag}] {len(R)} families. quartet obs {oq.mean():.3f} pred {pq_.mean():.3f} (median |err| {np.median(abs(oq-pq_)):.3f}); "
              f"centroid obs {oc.mean():.3f} pred {pc_.mean():.3f} (median |err| {np.median(abs(oc-pc_)):.3f})")
        print(f"[{tag}] advantage centroid−quartet: positive in {np.mean(adv_obs>0):.0%}, within 0.10 of prediction in "
              f"{np.mean(abs(adv_obs-adv_pred)<=0.10):.0%}; Spearman(β−2θ, centroid) = {rho:+.2f}; above line {int((line>0).sum())}, "
              f"below {int((line<=0).sum())}")
        print(f"[{tag}] H1 {h1}  H2 {h2}  H3 {h3}  -> PREREG21 verdict: {verdict}   ({time.time()-t0:.0f}s)")
    out["seconds"] = time.time() - t0
    json.dump(out, open(f"{HERE}/horizon21_{tag}.json", "w"), indent=1)
    print(f"HORIZON21 DONE {tag}")


if __name__ == "__main__":
    main()
