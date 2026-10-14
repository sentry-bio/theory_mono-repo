"""Stage 1 of the Atlas test (see PREREG.md): fit trait kernels on train orders, sample quartets, save predictions.

Nothing here computes an observed quartet accuracy. atlas_observe.py does that afterwards.
"""
import hashlib
import json
import os
import time

import numpy as np
from scipy.linalg import eigh

from atlas_data import build, core, patristic, taxonomy

A = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(20260925)
R = 200                       # Monte Carlo draws per quartet
N_TEST, N_TRAIN = 2500, 800   # quartets per level
LEVELS = {"L1": ("f", "g", 2), "L2": ("f", "g", 4), "L3": ("o", "f", 4),
          "L4": ("c", "o", 4), "L5": ("p", "c", 4), "L6": (None, "p", 4)}


def load():
    Z = np.load(f"{A}/catalogue_coordinates.npz")
    acc, z = Z["accession"], Z["z"]
    T = build(f"{A}/bac120_r220.tree")
    leaf_of = {core(T["name"][v]): v for v in np.flatnonzero(T["is_leaf"])}
    rows, leaves, seen = [], [], set()
    for i, a in enumerate(acc):
        v = leaf_of.get(core(a))
        if v is not None and v not in seen:
            rows.append(i); leaves.append(v); seen.add(v)
    rows, leaves = np.array(rows), np.array(leaves)
    tax = taxonomy()
    lab = {r: np.array([tax[core(T["name"][v])][r] for v in leaves]) for r in "pcofg"}
    train = np.array([int(hashlib.md5(o.encode()).hexdigest(), 16) % 2 == 0 for o in lab["o"]])
    return z, rows, leaves, T, lab, train


def groups(idx, labels):
    g = {}
    for i in idx:
        g.setdefault(labels[i], []).append(i)
    return {k: np.array(v) for k, v in g.items()}


def sample_pairs(idx, lab, rank, n):
    if rank is None:
        i, j = rng.choice(idx, n), rng.choice(idx, n)
        keep = i != j
        return i[keep], j[keep]
    g = [v for v in groups(idx, lab[rank]).values() if len(v) >= 2]
    sizes = np.array([len(v) for v in g], float)
    pick = rng.choice(len(g), n, p=sizes / sizes.sum())
    I, J = [], []
    for k in pick:
        a, b = rng.choice(g[k], 2, replace=False)
        I.append(a); J.append(b)
    return np.array(I), np.array(J)


def sample_quartets(idx, lab, level, n):
    parent, child, per = LEVELS[level]
    out = []
    if parent is None:
        kids = groups(idx, lab[child])
        names = list(kids)
        while len(out) < n:
            ch = rng.choice(len(names), 4, replace=False)
            out.append([rng.choice(kids[names[c]]) for c in ch])
        return np.array(out)
    par = groups(idx, lab[parent])
    elig = []
    for p, members in par.items():
        kids = groups(members, lab[child])
        kids = {k: v for k, v in kids.items() if len(v) >= (2 if per == 2 else 1)}
        if len(kids) >= (2 if per == 2 else 4):
            elig.append(kids)
    while len(out) < n:
        kids = elig[rng.integers(len(elig))]
        names = list(kids)
        if per == 2:
            a, b = rng.choice(len(names), 2, replace=False)
            q = list(rng.choice(kids[names[a]], 2, replace=False)) + list(rng.choice(kids[names[b]], 2, replace=False))
        else:
            ch = rng.choice(len(names), 4, replace=False)
            q = [rng.choice(kids[names[c]]) for c in ch]
        out.append(q)
    return np.array(out)


PAIRS = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]


def orient(Q, T, leaves):
    """Reorder each quartet so the tree's true split is 01|23; return quartets, six τ, t, δ."""
    tau = np.stack([patristic(T, leaves[Q[:, a]], leaves[Q[:, b]]) for a, b in PAIRS], 1)
    sums = np.stack([tau[:, 0] + tau[:, 1], tau[:, 2] + tau[:, 3], tau[:, 4] + tau[:, 5]], 1)
    best = sums.argmin(1)
    perm = {0: [0, 1, 2, 3], 1: [0, 2, 1, 3], 2: [0, 3, 1, 2]}
    Q = np.stack([Q[k, perm[b]] for k, b in enumerate(best)])
    tau = np.stack([patristic(T, leaves[Q[:, a]], leaves[Q[:, b]]) for a, b in PAIRS], 1)
    s_true = tau[:, 0] + tau[:, 1]
    delta = (np.minimum(tau[:, 2] + tau[:, 3], tau[:, 4] + tau[:, 5]) - s_true) / 2
    keep = delta > 1e-4
    return Q[keep], tau[keep], s_true[keep] / 4, delta[keep]


class Kernel:
    def __init__(self, centers, C):
        self.lc, self.C = np.log(centers), C   # C: (n_bins, n_axes)

    def __call__(self, tau):
        x = np.clip(np.log(np.maximum(tau, 1e-6)), self.lc[0], self.lc[-1])
        k = np.clip(np.searchsorted(self.lc, x) - 1, 0, len(self.lc) - 2)
        f = (x - self.lc[k]) / (self.lc[k + 1] - self.lc[k])
        return self.C[k] * (1 - f)[..., None] + self.C[k + 1] * f[..., None]


def predict(tau6, kern, G=None, w=None, chunk=64):
    """Monte Carlo four-point accuracy for quartets with six τ (true split 01|23)."""
    out = np.empty(len(tau6))
    for s in range(0, len(tau6), chunk):
        t6 = tau6[s:s + chunk]
        q = len(t6)
        c = kern(t6)                                   # (q, 6, a)
        a = c.shape[-1]
        K = np.broadcast_to(np.eye(4), (q, a, 4, 4)).copy()
        for p, (i, j) in enumerate(PAIRS):
            K[:, :, i, j] = K[:, :, j, i] = c[:, p, :]
        ev, V = np.linalg.eigh(K)
        L = V * np.sqrt(np.clip(ev, 1e-6, None))[..., None, :]
        eps = rng.standard_normal((q, a, 4, R))
        y = L @ eps                                    # (q, a, 4, R)
        d = {}
        for (i, j) in PAIRS:
            D = y[:, :, i, :] - y[:, :, j, :]          # (q, a, R)
            if G is not None:
                GD = np.einsum("ab,qbr->qar", G, D, optimize=True)
                d[(i, j)] = (GD * D).sum(1)
            else:
                d[(i, j)] = (w[None, :, None] * D * D).sum(1)
        s_true = d[(0, 1)] + d[(2, 3)]
        alt = np.minimum(d[(0, 2)] + d[(1, 3)], d[(0, 3)] + d[(1, 2)])
        out[s:s + q] = (s_true < alt).mean(1)
    return out


def opt_weights(kern, tau6):
    ts = np.median((tau6[:, 0] + tau6[:, 1]) / 2)
    tx = np.median((tau6[:, 2] + tau6[:, 3] + tau6[:, 4] + tau6[:, 5]) / 4)
    c0, cx = kern(np.array([ts]))[0], kern(np.array([tx]))[0]
    dc = c0 - cx
    return np.clip(dc / ((1 - cx) ** 2 + dc ** 2), 0, None)


if __name__ == "__main__":
    t0 = time.time()
    z, rows, leaves, T, lab, train = load()
    tr, te = np.flatnonzero(train), np.flatnonzero(~train)
    print(f"{len(rows):,} bacterial genomes on the r220 tree; train {len(tr):,} / test {len(te):,} "
          f"({len(set(lab['o'][tr])):,} / {len(set(lab['o'][te])):,} orders)")

    Z = z[rows]
    ev, V = np.linalg.eigh(np.cov(Z.T))
    P = V[:, ev > 1e-9 * ev.max()]
    print(f"z range: {P.shape[1]} of 136 dims carry variance (dropped variance {ev[ev <= 1e-9 * ev.max()].sum():.2e})")
    Y0 = Z @ P
    Sig = np.cov(Y0[tr].T)

    # variogram from train pairs across the ranks
    I, J = [], []
    for rank in ["g", "f", "o", "c", "p", None]:
        i, j = sample_pairs(tr, lab, rank, 60_000)
        I.append(i); J.append(j)
    I, J = np.concatenate(I), np.concatenate(J)
    tau = patristic(T, leaves[I], leaves[J])
    edges = np.geomspace(0.003, 4.0, 31)
    b = np.digitize(tau, edges) - 1
    centers, Gam = [], []
    for k in range(len(edges) - 1):
        m = b == k
        if m.sum() >= 500:
            D = Y0[I[m]] - Y0[J[m]]
            Gam.append(D.T @ D / (2 * m.sum()))
            centers.append(np.exp(np.log(tau[m]).mean()))
    centers, Gam = np.array(centers), np.array(Gam)
    mid = np.argmin(np.abs(np.log(centers / 0.3)))
    lam, U = eigh(Gam[mid], Sig)
    offdiag = []
    for Gb in Gam:
        M = U.T @ Gb @ U
        offdiag.append(np.linalg.norm(M - np.diag(np.diag(M))) / np.linalg.norm(np.diag(M)))
    Ckern = np.array([1 - np.diag(U.T @ Gb @ U) for Gb in Gam])
    kern = Kernel(centers, Ckern)
    G = np.linalg.inv(U.T @ U)
    print(f"variogram: {len(centers)} τ bins from {centers[0]:.3f} to {centers[-1]:.2f}; "
          f"off-diagonal share after joint diagonalisation: median {np.median(offdiag):.3f}, max {np.max(offdiag):.3f}")
    print(f"random-pair variogram vs Σ: mean diag {np.mean(np.diag(U.T @ Gam[-1] @ U)):.3f} (1 = no memory)")

    quart = {}
    for lv in LEVELS:
        Qte, tau_te, t_te, d_te = orient(sample_quartets(te, lab, lv, N_TEST), T, leaves)
        Qtr, tau_tr, _, _ = orient(sample_quartets(tr, lab, lv, N_TRAIN), T, leaves)
        w = opt_weights(kern, tau_tr)
        p_map = predict(tau_te, kern, G=G)
        p_opt = predict(tau_te, kern, w=w)
        quart[lv] = dict(Q=Qte, tau=tau_te, t=t_te, delta=d_te, w=w, p_map=p_map, p_opt=p_opt)
        print(f"{lv}: {len(Qte):,} test quartets, median t {np.median(t_te):.3f}, δ {np.median(d_te):.3f}; "
              f"predicted accuracy map {p_map.mean():.3f}, optimal {p_opt.mean():.3f} (gain {p_opt.mean()-p_map.mean():+.3f})")

    np.savez_compressed(f"{A}/atlas_predictions.npz", rows=rows, leaves=leaves, train=train, P=P, U=U, G=G,
                        centers=centers, Ckern=Ckern, offdiag=np.array(offdiag),
                        **{f"{lv}_{k}": v for lv, d in quart.items() for k, v in d.items()})
    summ = {"written": time.strftime("%Y-%m-%d %H:%M:%S"), "n_genomes": int(len(rows)),
            "levels": {lv: {"n": int(len(d["Q"])), "median_t": float(np.median(d["t"])), "median_delta": float(np.median(d["delta"])),
                            "pred_map": float(d["p_map"].mean()), "pred_opt": float(d["p_opt"].mean())} for lv, d in quart.items()}}
    json.dump(summ, open(f"{A}/atlas_predictions.json", "w"), indent=1)
    print(f"saved predictions at {summ['written']} ({time.time()-t0:.0f}s)")
