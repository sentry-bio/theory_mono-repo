"""Stage 1b (Amendment 1): full-matrix Gaussian tree predictions for the saved test quartets.

Re-derives the train variogram with the same seed as atlas_predict.py, validates the bivariate-normal (CLT)
accuracy formula against the saved per-axis Monte Carlo, then predicts both readers without assuming independent
axes. Still computes no observed accuracy.
"""
import json
import time

import numpy as np
from scipy.linalg import eigh

import atlas_predict as ap

A = ap.A
PIDX = {p: k for k, p in enumerate(ap.PAIRS)}
AV = np.array([-1, -1, 1, 1, 0, 0.0])
BV = np.array([-1, -1, 0, 0, 1, 1.0])
E = np.random.default_rng(7).standard_normal((20000, 2))


class MatKernel:
    def __init__(self, centers, Gam, Sig):
        self.lc, self.Gam, self.Sig = np.log(centers), Gam, Sig

    def S(self, tau):
        x = np.clip(np.log(np.maximum(tau, 1e-6)), self.lc[0], self.lc[-1])
        k = np.clip(np.searchsorted(self.lc, x) - 1, 0, len(self.lc) - 2)
        f = ((x - self.lc[k]) / (self.lc[k + 1] - self.lc[k]))[..., None, None]
        return self.Sig - (self.Gam[k] * (1 - f) + self.Gam[k + 1] * f)


def clt_predict(tau6, Sfun, Sig, B=None, chunk=24):
    out = np.empty(len(tau6))
    Sb = Sig if B is None else B.T @ Sig @ B
    for s in range(0, len(tau6), chunk):
        S6 = Sfun(tau6[s:s + chunk])                               # (q, 6, d, d)
        if B is not None:
            S6 = B.T @ S6 @ B
        q = len(S6)

        def Sab(a, b):
            return np.broadcast_to(Sb, S6.shape[:1] + Sb.shape) if a == b else S6[:, PIDX[(min(a, b), max(a, b))]]

        m = np.stack([2 * np.trace(Sb - S6[:, p], axis1=-2, axis2=-1) for p in range(6)], 1)
        V = np.empty((q, 6, 6))
        for p, (i, j) in enumerate(ap.PAIRS):
            for r in range(p, 6):
                k, l = ap.PAIRS[r]
                C = Sab(i, k) - Sab(i, l) - Sab(j, k) + Sab(j, l)
                V[:, p, r] = V[:, r, p] = 2 * (C * C).sum((-1, -2))
        mx, my = m @ AV, m @ BV
        vxx = np.einsum("i,qij,j->q", AV, V, AV)
        vyy = np.einsum("i,qij,j->q", BV, V, BV)
        vxy = np.einsum("i,qij,j->q", AV, V, BV)
        L11 = np.sqrt(vxx)
        L21 = vxy / L11
        L22 = np.sqrt(np.maximum(vyy - L21 ** 2, 0))
        X = mx[:, None] + L11[:, None] * E[:, 0]
        Y = my[:, None] + L21[:, None] * E[:, 0] + L22[:, None] * E[:, 1]
        out[s:s + q] = ((X > 0) & (Y > 0)).mean(1)
    return out


def reader_B(mk, tau6_train):
    ts = np.median((tau6_train[:, 0] + tau6_train[:, 1]) / 2)
    tx = np.median(tau6_train[:, 2:].mean(1))
    Gs, Gx = mk.Sig - mk.S(np.array([ts]))[0], mk.Sig - mk.S(np.array([tx]))[0]
    mu, U = eigh(Gs, Gx)
    w = np.clip((1 - mu) / (1 + (1 - mu) ** 2), 0, None)
    return U * np.sqrt(w), ts, tx, int((w > 0).sum())


if __name__ == "__main__":
    t0 = time.time()
    z, rows, leaves, T, lab, train = ap.load()
    tr, te = np.flatnonzero(train), np.flatnonzero(~train)
    saved = np.load(f"{A}/atlas_predictions.npz")
    assert (saved["rows"] == rows).all() and (saved["train"] == train).all()
    P = saved["P"]
    Y0 = z[rows] @ P
    Sig = np.cov(Y0[tr].T)
    I, J = [], []
    for rank in ["g", "f", "o", "c", "p", None]:
        i, j = ap.sample_pairs(tr, lab, rank, 60_000)
        I.append(i); J.append(j)
    I, J = np.concatenate(I), np.concatenate(J)
    tau = ap.patristic(T, leaves[I], leaves[J])
    edges = np.geomspace(0.003, 4.0, 31)
    b = np.digitize(tau, edges) - 1
    centers, Gam = [], []
    for k in range(len(edges) - 1):
        msk = b == k
        if msk.sum() >= 500:
            D = Y0[I[msk]] - Y0[J[msk]]
            Gam.append(D.T @ D / (2 * msk.sum()))
            centers.append(np.exp(np.log(tau[msk]).mean()))
    centers, Gam = np.array(centers), np.array(Gam)
    assert np.allclose(centers, saved["centers"]), "variogram not reproduced"
    mk = MatKernel(centers, Gam, Sig)

    # 1. validate the CLT formula on the per-axis model against the saved Monte Carlo
    U = saved["U"]
    Ui = np.linalg.inv(U)
    kern = ap.Kernel(centers, saved["Ckern"])

    def S_axis(t6):
        c = kern(t6)                                                # (q, 6, a)
        return np.einsum("ab,qpa,ac->qpbc", Ui, c, Ui, optimize=True)

    Sig_axis = Ui.T @ Ui
    print("CLT check (per-axis model): level  MC  vs  CLT")
    for lv in ap.LEVELS:
        t6 = saved[f"{lv}_tau"][:400]
        clt = clt_predict(t6, S_axis, Sig_axis)
        print(f"   {lv}: {saved[f'{lv}_p_map'][:400].mean():.3f} vs {clt.mean():.3f}")

    # 2. full-matrix predictions for both readers
    ap.rng = np.random.default_rng(99)
    res, Bs = {}, {}
    for lv in ap.LEVELS:
        t6 = saved[f"{lv}_tau"]
        _, tau_tr, _, _ = ap.orient(ap.sample_quartets(tr, lab, lv, ap.N_TRAIN), T, leaves)
        B, ts, tx, npos = reader_B(mk, tau_tr)
        pm = clt_predict(t6, mk.S, Sig)
        po = clt_predict(t6, mk.S, Sig, B=B)
        res[lv] = (pm, po); Bs[lv] = B
        print(f"{lv}: sister τ {ts:.3f}, non-sister τ {tx:.3f}, {npos} axes weighted; "
              f"predicted map {pm.mean():.3f}, optimal {po.mean():.3f} (gain {po.mean()-pm.mean():+.3f})")
    np.savez_compressed(f"{A}/atlas_predictions_full.npz", Sig=Sig, Gam=Gam, centers=centers,
                        **{f"{lv}_p_map": r[0] for lv, r in res.items()}, **{f"{lv}_p_opt": r[1] for lv, r in res.items()},
                        **{f"{lv}_B": B for lv, B in Bs.items()})
    summ = {"written": time.strftime("%Y-%m-%d %H:%M:%S"),
            "levels": {lv: {"pred_map": float(r[0].mean()), "pred_opt": float(r[1].mean())} for lv, r in res.items()}}
    json.dump(summ, open(f"{A}/atlas_predictions_full.json", "w"), indent=1)
    print(f"saved full-matrix predictions at {summ['written']} ({time.time()-t0:.0f}s)")
