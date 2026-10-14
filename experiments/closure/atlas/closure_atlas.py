"""PREREG20, Atlas arm (reported decomposition): the audit chain on A-curve's frozen family images.

Usage: python3 closure_atlas.py bac|ar   -> closure_atlas_<dom>.json, closure_atlas_<dom>.log
Reproduces acurve.py's AC1 construction exactly (same family qualification, same genus subsets and rng stream, the
same fitted family kernel S_fam) and adds, per test genus and ε:
  room        log2 M(ε, r) = d·log2(r/ε)                   (volume-ratio convention; r = RMS distance of the genus's
                                                             genomes from the family centroid)
  available   log2 M_rel(ε, r) = Σ_i log2 max(1, a_i/ε)     (the family covariance's ellipsoid at the same mean-square
                                                             radius: a_i = r·sqrt(d·λ_i/Σλ))
  demand      n (genomes in the genus)
  written     Σ_lin(ε): packing of the joint draw with the LINEAR kernel Γ_lin(τ) = (τ/c0)·Γ(c0) (the family's own
              shallowest shape extended without saturation; 100 replicates)
  kept        Σ_fam(ε): packing of the joint draw with the fitted saturating kernel (A-curve's prediction, 200 reps)
  read/obs    Σ_obs(ε): the greedy packing of the real genomes (AC1's observation)
Collisions between genera are not in AC1 and are reported as 1. The residual log(Σ_obs/Σ_fam) is A-curve's log error."""
import hashlib
import json
import sys
import time

import numpy as np

import atlas_predict as ap
import exp_D_family as E
from acurve import EDGES, EPS, load_domain, pair_tau, pooled_process, variogram
from atlas_predict2 import MatKernel
from k2_packing import greedy_pack, joint_draw

A = ap.A
ETA_EPS = (0.79, 1.25)
SMOKE = "smoke" in sys.argv[1:]          # disclosed smoke test: the first qualifying family, two genera, nothing scored


def log2_room(d, r, eps):
    return d * np.log2(max(r / eps, 1.0))


def log2_room_ellipsoid(lam, r, eps):
    lam = np.clip(lam, 0, None); d = len(lam)
    a = r * np.sqrt(d * lam / max(lam.sum(), 1e-300))
    return float(np.sum(np.log2(np.maximum(a / eps, 1.0))))


def main():
    dom = sys.argv[1]
    t0 = time.time()
    X, rows, leaves, T, lab, train = load_domain(dom)
    d = X.shape[1]
    tr_all = np.flatnonzero(train)
    minfam, mintrain, mingen_te, mingen = (300, 100, 4, 10) if dom == "bac" else (100, 50, 3, 6)
    pooled, Sig_pool = pooled_process(X, T, leaves, lab, tr_all)
    Gam_pool = lambda t: Sig_pool - pooled.S(np.array([t]))[0]
    fams = [f for f, n in zip(*np.unique(lab["f"], return_counts=True)) if n >= minfam]
    recs = []
    tag = f"{dom}_smoke" if SMOKE else dom
    log = open(f"{A}/closure_atlas_{tag}.log", "a")
    log.write(f"{time.ctime()} dom={dom} d={d}\n"); log.flush()
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
        # amendment 9 Oct (before the full run): the unsaturated rate is the maximal secant over the family's bins,
        # not the first bin's (a convex shallow end made the first secant an underestimate in the smoke test)
        kstar = int(np.argmax([np.trace(Gam[k]) / cen[k] for k in range(len(cen))]))
        c0 = float(cen[kstar]); G0 = Gam[kstar]

        def S_fam(tt, fk=fk, cen=cen, Sig=Sig, scale=scale):
            out = fk.S(tt)
            for q, t in enumerate(np.atleast_1d(tt)):
                if t < cen[0]:
                    out[q] = Sig - scale * Gam_pool(t)
            return out

        lam_f = np.linalg.eigvalsh((Sig + Sig.T) / 2)
        centroid = X[tr].mean(0)
        rng = np.random.default_rng(9001)            # acurve's stream: genus subsets and the two registered draws
        rng2 = np.random.default_rng(9201)           # this arm's extra draws, so the registered stream is untouched
        for g in sorted(set(lab["g"][te])):
            gi = te[lab["g"][te] == g]
            if len(gi) < mingen:
                continue
            if len(gi) > 30:
                gi = rng.choice(gi, 30, replace=False)
            tau = pair_tau(T, leaves, gi)
            Zf, clip_f = joint_draw(S_fam, Sig, tau, rng, 200); _Zp, _ = joint_draw(pooled.S, Sig_pool, tau, rng, 200)
            tmax = float(tau.max())
            Sig_lin = Sig + (tmax / c0) * G0

            def S_lin(tt, Sig_lin=Sig_lin, c0=c0, G0=G0):
                tt = np.atleast_1d(np.asarray(tt, float))
                return Sig_lin[None] - (tt / c0)[:, None, None] * G0[None]

            Zl, clip_l = joint_draw(S_lin, Sig_lin, tau, rng2, 100)
            r = float(np.sqrt(((X[gi] - centroid) ** 2).sum(1).mean()))
            n = len(gi)
            rec = dict(family=fam, genus=g, n=n, r=r, tau_mean=float(tau[np.triu_indices(n, 1)].mean()),
                       clipped_fam=clip_f, clipped_lin=clip_l, secant_bin=kstar, secant_tau=c0)
            for e in EPS:
                rec[f"obs|{e}"] = greedy_pack(X[gi], e)
                rec[f"fam|{e}"] = float(np.mean([greedy_pack(Zf[k], e) for k in range(200)]))
                rec[f"lin|{e}"] = float(np.mean([greedy_pack(Zl[k], e) for k in range(100)]))
                rec[f"room|{e}"] = float(log2_room(d, r, e))
                rec[f"avail|{e}"] = float(log2_room_ellipsoid(lam_f, r, e))
            recs.append(rec)
            if SMOKE and len(recs) >= 2:
                break
        print(f"{fam:24s} genera {sum(r['family'] == fam for r in recs):3d}  ({time.time()-t0:.0f}s)", flush=True)
        log.write(f"{fam} done {time.time()-t0:.0f}s\n"); log.flush()
        if SMOKE and recs:
            break

    # ---- pooled chain by ε (sums over genera, as AC1 pools) ----
    L2 = lambda x: float(np.log2(max(x, 1 + 1e-9)))
    out = dict(dom=dom, d=int(d), n_genera=len(recs), genera=recs, pooled={})
    print(f"\n[{dom}] ε | Σ_obs | Σ_fam | Σ_lin | Σn | log err obs/fam | log err obs/lin | mean η_obs | mean factors: occupancy avail writing retention residual")
    for e in EPS:
        so = sum(r[f"obs|{e}"] for r in recs); sf = sum(r[f"fam|{e}"] for r in recs); sl = sum(r[f"lin|{e}"] for r in recs)
        sn = sum(r["n"] for r in recs)
        per = []
        for r in recs:
            room = r[f"room|{e}"]; av = r[f"avail|{e}"] / room if room > 0 else float("nan")
            occ = L2(r["n"]) / room if room > 0 else float("nan")
            wr = L2(r[f"lin|{e}"]) / L2(r["n"]); ke = L2(r[f"fam|{e}"]) / L2(r[f"lin|{e}"]); rs = L2(r[f"obs|{e}"]) / L2(r[f"fam|{e}"])
            eta = L2(r[f"obs|{e}"]) / room if room > 0 else float("nan")
            per.append((occ, av, wr, ke, rs, eta))
        per = np.array(per)
        mf = np.nanmean(per, 0)
        out["pooled"][str(e)] = dict(sum_obs=so, sum_fam=sf, sum_lin=sl, sum_n=sn, err_obs_fam=float(np.log(so / sf)),
                                      err_obs_lin=float(np.log(so / sl)), mean_eta=float(mf[5]),
                                      mean_factors=dict(occupancy=float(mf[0]), availability=float(mf[1]), writing=float(mf[2]),
                                                        retention=float(mf[3]), residual=float(mf[4])))
        print(f"  {e:4.2f} | {so:6d} | {sf:7.1f} | {sl:7.1f} | {sn:5d} | {np.log(so/sf):+.3f} | {np.log(so/sl):+.3f} | {mf[5]:.4f} | "
              f"{mf[0]:.4f} {mf[1]:.3f} {mf[2]:.3f} {mf[3]:.3f} {mf[4]:.3f}")
    out["seconds"] = time.time() - t0
    json.dump(out, open(f"{A}/closure_atlas_{tag}.json", "w"), indent=1)
    print(f"ATLAS ARM DONE {tag} ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    main()
