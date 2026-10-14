"""PREREG24: the audit in mutual information on the intMEMOIR recorder.

Reuses closure_recorder.py's simulators and data loading unchanged. Usage (from closure/mi):
    python3 mi_closure.py            # main split (writer fitted on 60 train, scored on 47 test)
    python3 mi_closure.py swap       # replication
    python3 mi_closure.py smoke      # disclosed smoke test: two TRAIN colonies, 5 replicates, 20 permutations
Writes mi_closure_<tag>.json and appends to run.log.
"""
import hashlib, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))          # closure/
import closure_recorder as C                        # noqa: E402  (module-level: REC imports, SWAP/SMOKE/REPS/TAG)
R, rmix = C.R, C.rmix
from path_test import signatures                    # noqa: E402

NS, REPS, GMAX, TAG, SWAP, SMOKE = C.NS, C.REPS, C.GMAX, C.TAG, C.SWAP, C.SMOKE
NPERM = 20 if SMOKE else 200
LOG2 = np.log(2)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def mi_bits(labels, records):
    """Plug-in mutual information (bits) between integer labels and record rows (2-D int array)."""
    _, rec = np.unique(records, axis=0, return_inverse=True)
    rec = rec.reshape(-1)
    lab = np.asarray(labels)
    n = len(lab)
    _, li = np.unique(lab, return_inverse=True)
    li = li.reshape(-1)
    joint = li.astype(np.int64) * (rec.max() + 1) + rec
    def H(z):
        _, cnt = np.unique(z, return_counts=True)
        p = cnt / n
        return float(-(p * np.log2(p)).sum())
    Hl, Hr, Hj = H(li), H(rec), H(joint)
    K = (len(np.unique(li)), len(np.unique(rec)), len(np.unique(joint)))
    mi = Hl + Hr - Hj
    mm = mi + ((K[0] - 1) + (K[1] - 1) - (K[2] - 1)) / (2 * n * LOG2)   # Miller–Madow
    return mi, mm, Hl


def leaf_sets(c, g):
    """Lineage nodes at depth g and, per lineage, the leaf indices below it."""
    nodes = [k for k in range(len(c["T"])) if c["depth"][k] == g]
    leaves = [c["clade"][k] for k in nodes]
    return nodes, leaves


def mi_stage(X, lineage_leaves):
    """X: (reps, nodes, NS) stage records. Pools replicates; returns I(ℓ; X) in bits (plug-in, Miller–Madow)."""
    labs, recs = [], []
    for li, lv in enumerate(lineage_leaves):
        block = X[:, lv, :].reshape(-1, X.shape[2])
        recs.append(block); labs.append(np.full(len(block), li))
    mi, mm, _ = mi_bits(np.concatenate(labs), np.concatenate(recs))
    return mi, mm


POW3 = 3 ** np.arange(NS)


def readout_mi_exact(X, lineage_leaves, ro):
    """Amendment: I(ℓ; X_read) computed analytically from the pooled-replicate empirical p̂(x | ℓ) of the
    pre-readout record X and the registered readout mixture (π, ε_noisy, ε_clean; flips uniform over the two
    other states), applied site by site to the 3^NS-state vector."""
    def apply_channel(p, eps):
        T = np.full((3, 3), eps / 2); np.fill_diagonal(T, 1 - eps)
        q = p.reshape([3] * NS)
        for s in range(NS):
            q = np.moveaxis(np.tensordot(q, T, axes=([s], [0])), -1, s)
        return q.reshape(-1)
    weights, dists = [], []
    for lv in lineage_leaves:
        block = X[:, lv, :].reshape(-1, NS).astype(np.int64)
        codes = block @ POW3
        p = np.bincount(codes, minlength=3 ** NS).astype(np.float64); p /= p.sum()
        py = ro["pi"] * apply_channel(p, ro["eps_noisy"]) + (1 - ro["pi"]) * apply_channel(p, ro["eps_clean"])
        weights.append(len(lv)); dists.append(py)
    w = np.array(weights, float); w /= w.sum()
    P = np.stack(dists)  # lineages × states
    def H(v):
        v = v[v > 0]
        return float(-(v * np.log2(v)).sum())
    return H(w @ P) - float(sum(wi * H(pi) for wi, pi in zip(w, P))), P, w


def mi_observed_model(obs, lineage_leaves, P, w):
    """Amendment (ii): model-critic estimator of the observed information, the average log-likelihood ratio of
    the real leaf records under the model's p(y | ℓ) against the leaf-weighted mixture."""
    mix = w @ P
    vals = []
    for li, lv in enumerate(lineage_leaves):
        codes = obs[lv].astype(np.int64) @ POW3
        vals.extend(np.log2(P[li, codes] / mix[codes]).tolist())
    return float(np.mean(vals))


def mi_observed(obs, lineage_leaves, rng):
    labs, recs = [], []
    for li, lv in enumerate(lineage_leaves):
        recs.append(obs[lv]); labs.append(np.full(len(lv), li))
    labs = np.concatenate(labs); recs = np.concatenate(recs)
    mi, mm, Hl = mi_bits(labs, recs)
    null = np.array([mi_bits(rng.permutation(labs), recs)[0] for _ in range(NPERM)])
    return dict(plugin=mi, mm=mm, null_mean=float(null.mean()), null_sd=float(null.std()),
                above_null=max(mi - float(null.mean()), 0.0), H_label=Hl, n_leaves=int(len(labs)))


def main():
    t0 = time.time()
    cols = R.load()
    train = [c for c in cols if c["train"] != SWAP]; test = [c for c in cols if c["train"] == SWAP]
    if SMOKE:
        test = train[:2]
    with open(f"{HERE}/run.log", "a") as log:
        log.write(f"--- {TAG} run: {time.strftime('%Y-%m-%d %H:%M:%S %Z')} ---\nfrozen sha256:\n")
        for f in (os.path.abspath(__file__), f"{os.path.dirname(HERE)}/closure_recorder.py", f"{HERE}/PREREG24_mi_closure.md"):
            log.write(f"{sha(f)}  {os.path.basename(f)}\n")
    theta = json.load(open(f"{os.path.dirname(HERE)}/rec_fit_swap.json" if SWAP else f"{C.REC}/rec_fit.json"))["theta"]
    params = R.unpack(np.array(theta))
    W = rmix.build_writer(train); ro = W["readout"]
    print(f"{TAG}: train {len(train)} / test {len(test)}; reps {REPS}; perms {NPERM} ({time.time()-t0:.0f}s)", flush=True)

    acc = {g: dict(nc=0, N=0, r=0.0, I={}, obs=[]) for g in range(1, GMAX + 1)}
    stages = ["inf", "dist", "read5", "corr", "read6"]
    for g in acc:
        acc[g]["I"] = {s: [] for s in stages}
    for ci, c in enumerate(test):
        obs = np.maximum(c["obs"], 0)
        rng = np.random.default_rng(24000 + ci + 1000 * int(SWAP))
        S, E = C.sim_indep(c, params, rng, REPS)
        S5 = C.read_leaves(S, c, ro, rng)
        Sc = C.sim_corr(c, W, rng, REPS)
        S6 = C.read_leaves(Sc, c, ro, rng)
        for g in range(1, GMAX + 1):
            nodes, lv = leaf_sets(c, g)
            if not nodes:
                continue
            so = signatures(c, obs, g)
            a = acc[g]
            a["nc"] += 1; a["N"] += len(so); a["r"] += sum(sum(1 for x in s if x) for s in so)
            for s, X in (("inf", E), ("dist", S), ("corr", Sc)):
                a["I"][s].append(mi_stage(X, lv)[0])
            # amendment (i): readout stages analytic through the registered channel; plug-in/MM reported
            i5, P5, w5 = readout_mi_exact(S, lv, ro)
            i6, P6, w6 = readout_mi_exact(Sc, lv, ro)
            a["I"]["read5"].append(i5); a["I"]["read6"].append(i6)
            for s, X in (("read5_plugin", S5), ("read6_plugin", S6)):
                mi, mm = mi_stage(X, lv)
                a["I"].setdefault(s, []).append(mi); a["I"].setdefault(s + "_mm", []).append(mm)
            # amendment (ii): observed information by the model critic (scored); shuffle-null plug-in (reported)
            o = mi_observed(obs, lv, rng)
            o["model6"] = mi_observed_model(obs, lv, P6, w6); o["model5"] = mi_observed_model(obs, lv, P5, w5)
            a["obs"].append(o)
        print(f"  {c['name']} ({ci+1}/{len(test)}) {time.time()-t0:.0f}s", flush=True)

    prev = None
    pj = f"{os.path.dirname(HERE)}/closure_recorder_{'swap' if SWAP else 'main'}.json"
    if os.path.exists(pj) and not SMOKE:
        prev = json.load(open(pj))["gens"]
    res = dict(tag=TAG, reps=REPS, nperm=NPERM, n_train=len(train), n_test=len(test), gens={})
    print(f"\n[{TAG}] g | nc | N | log2M | I_inf | I_dist | I_read5 | I_corr | I_read6 | I_obs(model6) | fill | coll | read | corrF | read6F | η_pred5 | η_pred6 | η_obs | err6")
    for g, a in acc.items():
        if a["nc"] == 0:
            continue
        M = C.log2_ball(a["r"] / a["N"])
        I = {s: float(np.mean(v)) for s, v in a["I"].items()}
        Iobs = float(np.mean([o["model6"] for o in a["obs"]]))          # scored (amendment ii)
        Iobs5 = float(np.mean([o["model5"] for o in a["obs"]]))
        Iobs_null = float(np.mean([o["above_null"] for o in a["obs"]]))  # reported
        Iobs_plugin = float(np.mean([o["plugin"] for o in a["obs"]])); Iobs_mm = float(np.mean([o["mm"] for o in a["obs"]]))
        def ratio(x, y):
            return float(x / y) if y > 0 else None
        fac = dict(fill=I["inf"] / M, collisions=ratio(I["dist"], I["inf"]), reading=ratio(I["read5"], I["dist"]),
                   correlation=ratio(I["corr"], I["dist"]), reading6=ratio(I["read6"], I["corr"]))
        eta = dict(pred5=I["read5"] / M, pred6=I["read6"] / M, obs=Iobs / M, obs_model5=Iobs5 / M,
                   obs_above_null=Iobs_null / M, obs_plugin=Iobs_plugin / M, obs_mm=Iobs_mm / M)
        err6 = float(np.log(eta["pred6"] / eta["obs"])) if eta["obs"] > 0 else None
        err5 = float(np.log(eta["pred5"] / eta["obs_model5"])) if eta["obs_model5"] > 0 else None
        gated = a["N"] >= 50
        row = dict(n_colonies=a["nc"], N=a["N"], log2_room=M, I=I, I_obs_model6=Iobs, I_obs_model5=Iobs5,
                   I_obs_above_null=Iobs_null, I_obs_plugin=Iobs_plugin, I_obs_mm=Iobs_mm,
                   factors=fac, eta=eta, err5=err5, err6=err6, gated=gated)
        if prev and str(g) in prev:
            row["count_based"] = dict(reading5=prev[str(g)]["factors"]["reading5"], reading6=prev[str(g)]["factors"]["reading6"],
                                      eta_obs=prev[str(g)]["eta"]["obs"])
        res["gens"][g] = row
        print(f"  {g} | {a['nc']:3d} | {a['N']:4d} | {M:5.2f} | {I['inf']:5.3f} | {I['dist']:5.3f} | {I['read5']:5.3f} | {I['corr']:5.3f} | {I['read6']:5.3f} | {Iobs:5.3f} | "
              f"{fac['fill']:.3f} | {fac['collisions'] or 0:.3f} | {fac['reading'] or 0:.3f} | {fac['correlation'] or 0:.3f} | {fac['reading6'] or 0:.3f} | "
              f"{eta['pred5']:.3f} | {eta['pred6']:.3f} | {eta['obs']:.3f} | {err6 if err6 is None else round(err6, 3)}{'' if gated else '  (N<50)'}")
    if not SMOKE:
        G = res["gens"]; gated = [g for g in G if G[g]["gated"]]
        mi1 = all((G[g]["factors"][f] or 0) <= 1.02 for g in gated for f in ("collisions", "reading", "correlation", "reading6"))
        mi2 = all((G[g]["factors"]["reading"] < 1.0) for g in gated if G[g].get("count_based", {}).get("reading5", 0) > 1.0) and \
              all((G[g]["factors"]["reading6"] < 1.0) for g in gated if G[g].get("count_based", {}).get("reading6", 0) > 1.0)
        mi3 = all(G[g]["err6"] is not None and abs(G[g]["err6"]) <= 0.15 for g in gated)
        mi4 = all("count_based" in G[g] and G[g]["eta"]["obs"] <= G[g]["count_based"]["eta_obs"] for g in gated)
        res["verdicts"] = dict(MI1_chain_ordered=mi1, MI2_symptom_resolves=mi2, MI3_closure=mi3, MI4_consistency=mi4, gated=gated,
                               overall="AUDIT CLOSES IN INFORMATION" if (mi1 and mi2 and mi3 and mi4) else "NOT AS REGISTERED")
        print(f"\n[{TAG}] verdicts: {res['verdicts']}")
    json.dump(res, open(f"{HERE}/mi_closure_{TAG}.json", "w"), indent=1)
    print(f"done {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
