"""PREREG20, recorder arm: stage counts, factors, closure and η on the intMEMOIR recorder.

Imports the frozen PREREG4/9 code unchanged from ~/Documents/addressability-recorders-2026-09-26 (rec_test, rmix,
fusion, path_test, k1_scaling); the data are read in place from closure/intmemoir. Usage:
    python3 closure_recorder.py          # main split: writer fitted on the 60 train colonies, scored on the 47
    python3 closure_recorder.py swap     # replication: writer re-fitted on the 47, scored on the 60
Writes closure_recorder_<tag>.json, run_recorder_<tag>.log (frozen hashes), and prints the table."""
import hashlib
import json
import os
import sys
import time
from math import comb

import numpy as np

REC = "/Users/rohitfenn/Documents/addressability-recorders-2026-09-26"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, REC)
import rec_test as R  # noqa: E402

R.HERE = HERE                      # rec_test.load() reads {HERE}/intmemoir/s*
import rmix  # noqa: E402  (reads rec_fit.json: the PREREG4 writer, fitted on the main train split)
from fusion import branch_info  # noqa: E402
from path_test import signatures  # noqa: E402
from k1_scaling import clusters_eps  # noqa: E402

SWAP = "swap" in sys.argv[1:]
SMOKE = "smoke" in sys.argv[1:]          # disclosed smoke test: two TRAIN colonies, 5 replicates, no registered statistic
NS, REPS, GMAX = R.NS, (5 if SMOKE else 400), 6
TAG = "smoke" if SMOKE else ("swap" if SWAP else "main")
STAGES = ["w_inf", "w_fin", "read5", "corr", "read6"]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def log2_ball(r):
    """log2 of the number of ten-site tapes with at most r edited sites (two edited states); log-linear between
    integers. This is the room M(0, r) of the registration."""
    def lb(k):
        return float(np.log2(sum(comb(NS, j) * 2 ** j for j in range(int(k) + 1))))
    k = int(np.floor(r)); f = r - k
    if k >= NS:
        return lb(NS)
    return (1 - f) * lb(k) + f * lb(k + 1)


def sim_indep(c, params, rng, reps):
    """The PREREG4 writer on the true tree with every edit event labelled. Returns S (states) and E (event ids:
    0 none, negative = edited before the colony start, positive = node*NS + site + 1), both (reps, nodes, NS)."""
    lam, kap, q, p0, _ = params
    n = len(c["T"])
    S = np.zeros((reps, n, NS), np.int8); E = np.zeros((reps, n, NS), np.int32)
    init = rng.random((reps, NS)) < p0
    s = np.where(init, np.where(rng.random((reps, NS)) < q, 1, 2), 0).astype(np.int8)
    e = np.where(init, -(np.arange(NS) + 1), 0).astype(np.int32)

    def step(state, ids, Lam, node):
        ed = (state == 0) & (rng.random(state.shape) < 1 - np.exp(-Lam))
        new = np.where(ed, np.where(rng.random(state.shape) < q, 1, 2), state).astype(np.int8)
        nid = np.where(ed, node * NS + np.arange(NS) + 1, ids).astype(np.int32)
        return new, nid

    S[:, 0], E[:, 0] = step(s, e, kap * (c["ov"][0] @ lam), 0)
    for k in sorted(range(1, n), key=lambda k: c["depth"][k]):
        S[:, k], E[:, k] = step(S[:, c["par"][k]], E[:, c["par"][k]], kap * (c["ov"][k] @ lam), k)
    return S, E


def sim_corr(c, W, rng, reps):
    """rmix.simulate without its readout step: internal donors matched by start bin and duration, colony activity
    classes (LEAF_INTERNAL semantics). Returns states at all nodes."""
    n = len(c["T"])
    dcl = int(np.clip(c["depth"].max(), 3, 5) - 3)
    S = np.zeros((reps, n, NS), np.int8)
    cache = {}
    for r in range(reps):
        k = int(rng.choice(3, p=W["freq"][dcl]))
        for v in sorted(range(n), key=lambda v: c["depth"][v]):
            base = S[r, c["par"][v]].copy() if c["par"][v] >= 0 else np.zeros(NS, np.int8)
            if not (v == 0 and c["virtual"]):
                a, d = branch_info(c, v)
                key = (k, v)
                if key not in cache:
                    cache[key] = rmix.pool(W, k, "int", a, d, c["name"])
                P = cache[key]
                for s, al in P[rng.integers(len(P))]:
                    if base[s] == 0:
                        base[s] = al
            S[r, v] = base
    return S


def read_leaves(S, c, ro, rng):
    """The readout mixture (pi, eps_clean, eps_noisy) applied to the leaves, exactly as rmix.simulate does."""
    out = np.zeros_like(S); lv = S[:, c["leaves"]]
    noisy = rng.random(lv.shape[:2]) < ro["pi"]
    rate = np.where(noisy, ro["eps_noisy"], ro["eps_clean"])[..., None]
    flip = rng.random(lv.shape) < rate
    out[:, c["leaves"]] = np.where(flip, (lv + rng.integers(1, 3, lv.shape)) % 3, lv)
    return out


def signatures_ids(c, E, g):
    """Strict consensus of event ids over a lineage's leaves: a site is fixed only when every leaf carries the same
    event, so two lineages collide only by inheritance (infinite sites)."""
    out = []
    for k in range(len(c["T"])):
        if c["depth"][k] != g:
            continue
        L = E[c["clade"][k]]
        same = (L == L[0]).all(0) & (L[0] != 0)
        out.append(tuple(int(x) for x in np.where(same, L[0], 0)))
    return out


def main():
    t0 = time.time()
    cols = R.load()
    train = [c for c in cols if c["train"] != SWAP]; test = [c for c in cols if c["train"] == SWAP]
    if SMOKE:
        test = train[:2]
    with open(f"{HERE}/run_recorder_{TAG}.log", "a") as log:
        files = [os.path.abspath(__file__)] + [f"{REC}/{f}" for f in
                                               ("rec_test.py", "rmix.py", "fusion.py", "path_test.py", "k1_scaling.py", "rec_fit.json")]
        log.write("frozen sha256:\n" + "".join(f"{sha(f)}  {os.path.basename(f)}\n" for f in files))
        man = hashlib.sha256()
        for d in sorted(os.listdir(f"{HERE}/intmemoir")):
            for f in ("true_tree.nwk", "characters.txt"):
                p = f"{HERE}/intmemoir/{d}/{f}"
                if os.path.exists(p):
                    man.update(open(p, "rb").read())
        log.write(f"{man.hexdigest()}  intmemoir manifest (true_tree.nwk + characters.txt)\n{time.ctime()}\n")

    if SWAP:
        fitp = f"{HERE}/rec_fit_swap.json"
        if not os.path.exists(fitp):
            from scipy.optimize import minimize
            th0 = np.concatenate([np.log([0.003] * 4), np.zeros(9), np.zeros(10), np.full(10, -3.0), [-4.0]])
            res = minimize(R.negll, th0, args=(train,), method="L-BFGS-B", options=dict(maxiter=500))
            json.dump(dict(theta=res.x.tolist(), negll=float(res.fun), success=bool(res.success), message=str(res.message),
                           train=[c["name"] for c in train]), open(fitp, "w"), indent=1)
            print(f"swap writer fit: converged {res.success}; -loglik {res.fun:.1f} ({time.time()-t0:.0f}s)", flush=True)
        theta = json.load(open(fitp))["theta"]
    else:
        theta = json.load(open(f"{REC}/rec_fit.json"))["theta"]
    params = R.unpack(np.array(theta))
    W = rmix.build_writer(train)
    ro = W["readout"]
    print(f"{TAG}: train {len(train)} / test {len(test)}; readout mixture {ro}; class cuts {np.round(W['cut'], 4).tolist()} "
          f"({time.time()-t0:.0f}s)", flush=True)

    tot = {g: {s: np.zeros(REPS) for s in STAGES} for g in range(1, GMAX + 1)}
    obs_cnt = {g: dict(N=0, D=0, D1=0, r=0.0, nc=0) for g in range(1, GMAX + 1)}
    for ci, c in enumerate(test):
        obs = np.maximum(c["obs"], 0)
        rng = np.random.default_rng(20000 + ci + 1000 * int(SWAP))
        S, E = sim_indep(c, params, rng, REPS)
        S5 = read_leaves(S, c, ro, rng)
        Sc = sim_corr(c, W, rng, REPS)
        S6 = read_leaves(Sc, c, ro, rng)
        for g in range(1, GMAX + 1):
            so = signatures(c, obs, g)
            if not so:
                continue
            o = obs_cnt[g]
            o["N"] += len(so); o["D"] += len(set(so)); o["D1"] += clusters_eps(so, 1)
            o["r"] += sum(sum(1 for x in s if x) for s in so); o["nc"] += 1
            for r in range(REPS):
                tot[g]["w_inf"][r] += len(set(signatures_ids(c, E[r], g)))
                tot[g]["w_fin"][r] += len(set(signatures(c, S[r], g)))
                tot[g]["read5"][r] += len(set(signatures(c, S5[r], g)))
                tot[g]["corr"][r] += len(set(signatures(c, Sc[r], g)))
                tot[g]["read6"][r] += len(set(signatures(c, S6[r], g)))
        print(f"  {c['name']} ({ci+1}/{len(test)}) {time.time()-t0:.0f}s", flush=True)

    def L2(x):
        return float(np.log2(max(x, 1 + 1e-9)))

    res = dict(tag=TAG, reps=REPS, readout=ro, n_train=len(train), n_test=len(test), gens={})
    gated = []
    print(f"\n[{TAG}] g | colonies | N̄ | r̄ | log2 room | D̄_obs | w_inf | w_fin | read5 | corr | read6 | err5 | err6 | η_obs | η_pred5 | η_pred6")
    for g in range(1, GMAX + 1):
        o = obs_cnt[g]
        if o["nc"] == 0:
            continue
        nc = o["nc"]; Nbar = o["N"] / nc; Dobs = o["D"] / nc; Dobs1 = o["D1"] / nc; rbar = o["r"] / o["N"]
        M = log2_ball(rbar)
        m = {s: float(tot[g][s].mean() / nc) for s in STAGES}; sd = {s: float(tot[g][s].std() / nc) for s in STAGES}
        fac = dict(occupancy=L2(Nbar) / M, writer_speed=L2(m["w_inf"]) / L2(Nbar), collisions=L2(m["w_fin"]) / L2(m["w_inf"]),
                   reading5=L2(m["read5"]) / L2(m["w_fin"]), correlation=L2(m["corr"]) / L2(m["w_fin"]),
                   reading6=L2(m["read6"]) / L2(m["corr"]), writing_lean=L2(m["w_inf"]) / M)
        err5 = float(np.log(m["read5"] / Dobs)); err6 = float(np.log(m["read6"] / Dobs))
        eta = dict(obs=L2(Dobs) / M, obs_eps1=L2(Dobs1) / (M - np.log2(3)), pred5=L2(m["read5"]) / M, pred6=L2(m["read6"]) / M,
                   demand=L2(Nbar) / M)
        is_gated = o["N"] >= 50
        if is_gated:
            gated.append(g)
        res["gens"][g] = dict(n_colonies=nc, N=o["N"], Nbar=Nbar, rbar=rbar, log2_room=M, D_obs=Dobs, D_obs_eps1=Dobs1,
                              stages={s: dict(mean=m[s], sd=sd[s]) for s in STAGES}, factors=fac, err5=err5, err6=err6,
                              eta=eta, gated=is_gated)
        print(f"  {g} | {nc:3d} | {Nbar:5.2f} | {rbar:4.2f} | {M:5.2f} | {Dobs:5.2f} | {m['w_inf']:5.2f} | {m['w_fin']:5.2f} | "
              f"{m['read5']:5.2f} | {m['corr']:5.2f} | {m['read6']:5.2f} | {err5:+.3f} | {err6:+.3f} | {eta['obs']:.3f} | "
              f"{eta['pred5']:.3f} | {eta['pred6']:.3f}{'' if is_gated else '  (N<50)'}")
    G = res["gens"]
    print(f"\n[{TAG}] factors: g | occupancy | writer_speed | collisions | correlation | reading6 | reading5 | writing_lean")
    for g in G:
        f = G[g]["factors"]
        print(f"  {g} | {f['occupancy']:.3f} | {f['writer_speed']:.3f} | {f['collisions']:.3f} | {f['correlation']:.3f} | "
              f"{f['reading6']:.3f} | {f['reading5']:.3f} | {f['writing_lean']:.3f}")
    cl1 = all(abs(G[g]["err5"]) <= 0.15 for g in gated)
    cl2 = all(abs(G[g]["err6"]) <= 0.15 for g in gated)
    cl3 = (all(np.log(G[g]["factors"]["correlation"]) < 0 for g in gated if g >= 2)
           and all(abs(G[g]["err6"]) < abs(G[g]["err5"]) for g in gated if g >= 3))
    gd = max(gated) if gated else max(G)
    f = G[gd]["factors"]
    mags = [abs(np.log(f["writer_speed"])), abs(np.log(f["correlation"])), abs(np.log(f["reading6"])), abs(np.log(f["collisions"]))]
    cl4 = bool(mags[0] >= mags[1] >= mags[2] >= mags[3])
    pred_fail1 = (not cl1) and any(G[g]["err5"] > 0.15 for g in gated if g >= 3)
    verdict = ("NO GATED GENERATION" if not gated else "CLOSED" if cl1 else "NOT CLOSED" if not cl2
               else "CLOSURE LOCATED" if (pred_fail1 and cl3) else "PARTIAL")
    res.update(gated=gated, CL1=cl1, CL2=cl2, CL3=cl3, CL4=cl4, CL4_magnitudes=dict(writer_speed=mags[0], correlation=mags[1],
                                                                                   reading=mags[2], collisions=mags[3]),
               CL1_failed_as_predicted=pred_fail1, verdict=verdict, seconds=time.time() - t0)
    print(f"\n[{TAG}] gated generations {gated}; CL1 {cl1} (failed as predicted: {pred_fail1}); CL2 {cl2}; CL3 {cl3}; "
          f"CL4 {cl4} (|log| writer {mags[0]:.3f}, correlation {mags[1]:.3f}, reading {mags[2]:.3f}, collisions {mags[3]:.3f})")
    print(f"PREREG20 recorder verdict ({TAG}): {verdict}   ({time.time()-t0:.0f}s)")
    json.dump(res, open(f"{HERE}/closure_recorder_{TAG}.json", "w"), indent=1)


if __name__ == "__main__":
    main()
