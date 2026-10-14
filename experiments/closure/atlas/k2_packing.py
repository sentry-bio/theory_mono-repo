"""K2 (PREREG8): Atlas packing. Family process (train genera) simulated jointly on each test genus subtree; greedy
ε-packing of leaves in the recipe metric vs observed; ε = median halves distance / √2."""
import hashlib
import json

import numpy as np

import atlas_predict as ap
import exp_D_family as E
from atlas_data import lca
from atlas_predict2 import MatKernel

A = ap.A
OUT = "/Users/rohitfenn/Documents/addressability-atlas-2026-09-26"
EDGES = np.geomspace(0.003, 1.5, 19)
CROWN = np.geomspace(0.01, 0.6, 7)
REPS = 200
CAP = 30


def greedy_pack(V, eps):
    kept = []
    for v in V:
        if all(np.linalg.norm(v - k) > eps for k in kept):
            kept.append(v)
    return len(kept)


def joint_draw(S_of, Sig, tau, rng, reps):
    n = len(tau); d = Sig.shape[0]
    C = np.empty((n * d, n * d))
    for i in range(n):
        for j in range(n):
            C[i * d:(i + 1) * d, j * d:(j + 1) * d] = Sig if i == j else S_of(np.array([tau[i, j]]))[0]
    w, V = np.linalg.eigh((C + C.T) / 2)
    clipped = float(-w[w < 0].sum() / w[w > 0].sum()) if (w < 0).any() else 0.0
    L = V * np.sqrt(np.clip(w, 0, None))
    Z = (L @ rng.standard_normal((n * d, reps))).T.reshape(reps, n, d)
    return Z, clipped


if __name__ == "__main__":
    H = [json.loads(l) for l in open(f"{A}/k2_halves_out.jsonl")]
    dh = np.array([h["d_halves"] for h in H])
    eps_med, eps_p90 = float(np.median(dh) / np.sqrt(2)), float(np.percentile(dh, 90) / np.sqrt(2))
    print(f"halves distance: n={len(dh)}, median {np.median(dh):.3f}, p90 {np.percentile(dh, 90):.3f} -> ε = {eps_med:.3f} (sensitivity {eps_p90:.3f})")
    z, rows, leaves, T, lab, train = ap.load()
    X = z[rows] @ np.load(f"{A}/atlas_predictions.npz")["P"]
    f1 = np.load(f"{A}/atlas_predictions_full.npz")
    pooled = MatKernel(f1["centers"], f1["Gam"], f1["Sig"])
    Gam_pool = lambda tau: f1["Sig"] - pooled.S(np.array([tau]))[0]
    fams = {f: n for f, n in zip(*np.unique(lab["f"], return_counts=True)) if n >= 300}
    rng = np.random.default_rng(8003)
    recs = []
    for fam in sorted(fams):
        idx = np.flatnonzero(lab["f"] == fam)
        trm = np.array([int(hashlib.md5(("E-D:" + g).encode()).hexdigest(), 16) % 2 == 0 for g in lab["g"][idx]])
        tr, te = idx[trm], idx[~trm]
        if len(tr) < 100 or len(set(lab["g"][te])) < 4:
            continue
        E.rng = np.random.default_rng(260926)
        I1, J1 = E.pairs_within(tr, lab["g"], 20_000); I2, J2 = E.pairs_within(tr, lab["f"], 20_000)
        I, J = np.concatenate([I1, I2]), np.concatenate([J1, J2])
        tau = ap.patristic(T, leaves[I], leaves[J]); b = np.digitize(tau, EDGES) - 1
        cen, Gam = [], []
        for k in range(len(EDGES) - 1):
            m = b == k
            if m.sum() >= 150:
                Dm = X[I[m]] - X[J[m]]; Gam.append(Dm.T @ Dm / (2 * m.sum())); cen.append(np.exp(np.log(tau[m]).mean()))
        if len(cen) < 3:
            continue
        cen, Gam = np.array(cen), np.array(Gam); Sig = np.cov(X[tr].T)
        fk = MatKernel(cen, Gam, Sig)
        scale = np.trace(Gam[0]) / np.trace(Gam_pool(cen[0]))

        def S_fam(tt, fk=fk, cen=cen, Sig=Sig, scale=scale):
            out = fk.S(tt)
            for q, t in enumerate(np.atleast_1d(tt)):
                if t < cen[0]:
                    out[q] = Sig - scale * Gam_pool(t)
            return out

        for g in sorted(set(lab["g"][te])):
            gi = te[lab["g"][te] == g]
            if len(gi) < 4:
                continue
            if len(gi) > CAP:
                gi = rng.choice(gi, CAP, replace=False)
            lv = leaves[gi]
            n = len(gi)
            tau_g = np.zeros((n, n))
            for i in range(n):
                tau_g[i, i + 1:] = ap.patristic(T, np.repeat(lv[i], n - i - 1), lv[i + 1:]); tau_g[i + 1:, i] = tau_g[i, i + 1:]
            m = lv[0]
            for x in lv[1:]:
                m = lca(T, np.array([m]), np.array([x]))[0]
            crown = float(np.max(T["depth"][lv] - T["depth"][m]))
            obs = greedy_pack(X[gi], eps_med); obs90 = greedy_pack(X[gi], eps_p90)
            Zf, clip = joint_draw(S_fam, Sig, tau_g, rng, REPS)
            Zp, _ = joint_draw(pooled.S, f1["Sig"], tau_g, rng, REPS)
            pf = np.mean([greedy_pack(Zf[r], eps_med) for r in range(REPS)])
            pf90 = np.mean([greedy_pack(Zf[r], eps_p90) for r in range(REPS)])
            pp = np.mean([greedy_pack(Zp[r], eps_med) for r in range(REPS)])
            recs.append(dict(family=fam, genus=g, n=n, crown=crown, obs=obs, obs90=obs90, pred=pf, pred90=pf90, pooled=pp, clipped=clip))
        print(f"{fam:24s} genera done: {sum(r['family'] == fam for r in recs)}", flush=True)
    crown = np.array([r["crown"] for r in recs]); b = np.digitize(crown, CROWN) - 1
    first_bins = {}
    print(f"\n{len(recs)} test genera. crown bin | genera | leaves | packed obs | family pred | pooled pred | log-err family / pooled | (ε p90: obs/pred)")
    errs, gated = [], []
    for k in range(len(CROWN) - 1):
        m = b == k
        if m.sum() == 0:
            continue
        o = sum(r["obs"] for r in np.array(recs)[m]); pf = sum(r["pred"] for r in np.array(recs)[m]); pp = sum(r["pooled"] for r in np.array(recs)[m])
        o9 = sum(r["obs90"] for r in np.array(recs)[m]); p9 = sum(r["pred90"] for r in np.array(recs)[m])
        nl = sum(r["n"] for r in np.array(recs)[m])
        e, ep = np.log(o / pf), np.log(o / pp)
        if m.sum() >= 40:
            errs.append(abs(e)); gated.append((CROWN[k], abs(e) <= 0.15))
        print(f"  {CROWN[k]:.3f}-{CROWN[k+1]:.3f} | {m.sum():4d} | {nl:5d} | {o:5d} | {pf:8.1f} | {pp:8.1f} | {e:+.3f} / {ep:+.3f} | ({o9}/{p9:.1f})")
    allpass = all(ok for _, ok in gated)
    deep = [ok for c0, ok in gated if c0 >= 0.05]
    verdict = "PASS" if allpass else ("PARTIAL" if deep and all(deep) else "FAIL")
    clipm = float(np.mean([r["clipped"] for r in recs]))
    print(f"\nmean clipped negative-eigenvalue mass in joint covariances: {clipm:.3f}")
    print(f"K2 verdict: {verdict}")
    json.dump(dict(eps=eps_med, eps90=eps_p90, genera=recs, verdict=verdict), open(f"{OUT}/k2_results.json", "w"), indent=1, default=float)
