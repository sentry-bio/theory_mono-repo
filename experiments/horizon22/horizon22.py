"""PREREG22 — two-reader rate-spectrum horizon (synthetic, Jukes–Cantor quartets).

Subcommands
  sim      simulate t*(L) for both readers at one shape a           (writes JSON)
  predict  exact-curve predictions from RATE_TAIL_DERIVATION.md §2–5 (writes JSON)
  score    apply the registered verdict rules                        (writes JSON + prints)

Depth t is in expected substitutions per site at the mean site rate; tips hang at duration t below the two
internal nodes, which are joined by an internal branch of duration tau.  Readers: unweighted mismatch
four-point reader, and the oracle rate-weighted contrast reader with per-site weights s_i / v_i.
"""
import argparse, hashlib, json, math, sys, time
import numpy as np

# ----------------------------------------------------------------------------- model

def lam(r, ell):
    return np.exp(-4.0 * r * ell / 3.0)

def p_same(r, ell):
    return 0.25 + 0.75 * lam(r, ell)

def signal(r, t, tau):
    """s_i(t) = p(2t) - p(2t+tau) (exact)."""
    return p_same(r, 2 * t) - p_same(r, 2 * t + tau)

def variance(r, t, tau):
    """Var[1(A=B) - 1(A=C)] per site (exact, Z2xZ2 coordinates)."""
    p1 = p_same(r, 2 * t)
    p2 = p_same(r, 2 * t + tau)
    P0t, P1t = p_same(r, t), (1 - lam(r, t)) / 4
    P0s, P1s = p_same(r, t + tau), (1 - lam(r, t + tau)) / 4
    q = P0t ** 2 * P0s + 3 * P1t ** 2 * P1s
    return p1 * (1 - p1) + p2 * (1 - p2) - 2 * (q - p1 * p2)

def draw_rates(a, n, rng):
    if a == math.inf:
        return np.ones(n)
    return rng.gamma(shape=a, scale=1.0 / a, size=n)

# ----------------------------------------------------------------------------- simulation

def noise(lam_arr, rng):
    """JC noise in XOR coordinates: 0 w.p. lam + (1-lam)/4, else uniform over {1,2,3}."""
    u = rng.random(lam_arr.shape)
    keep = u < lam_arr
    other = rng.integers(0, 4, size=lam_arr.shape, dtype=np.int8)
    return np.where(keep, np.int8(0), other)

BATCH = 250  # amendment 2026-10-14 04:31 CEST: replicates are simulated in batches (memory), same statistics


def simulate_success(a, L, t, tau, reps, seed):
    """Return (success_unweighted, success_weighted) over `reps` quartets of L sites."""
    key = f"{seed}|{a}|{L}|{t:.9f}|{tau}"
    rng = np.random.default_rng(int(hashlib.sha256(key.encode()).hexdigest()[:16], 16))
    ok_u, ok_w, done = 0, 0, 0
    while done < reps:
        n = min(BATCH, reps - done)
        r = draw_rates(a, (n, L), rng)
        lt = lam(r, t)
        ltau = lam(r, tau)
        X = rng.integers(0, 4, size=(n, L), dtype=np.int8)
        Y = X ^ noise(ltau, rng)
        A = X ^ noise(lt, rng)
        B = X ^ noise(lt, rng)
        C = Y ^ noise(lt, rng)
        D = Y ^ noise(lt, rng)
        m = {
            "AB": (A != B), "CD": (C != D), "AC": (A != C),
            "BD": (B != D), "AD": (A != D), "BC": (B != C),
        }
        w_oracle = signal(r, t, tau) / variance(r, t, tau)
        for idx, w in enumerate((np.ones_like(w_oracle), w_oracle)):
            s = {k: (w * v).sum(axis=1) for k, v in m.items()}
            true = s["AB"] + s["CD"]
            alt1 = s["AC"] + s["BD"]
            alt2 = s["AD"] + s["BC"]
            ok = int(((true < alt1) & (true < alt2)).sum())
            if idx == 0:
                ok_u += ok
            else:
                ok_w += ok
        done += n
    return ok_u / reps, ok_w / reps

def bisect_tstar(a, L, tau, reps, seed, P0, which, t_lo=0.02, steps=12):
    """Largest t with success >= P0 for reader `which` (0 unweighted, 1 weighted)."""
    t_hi = 1.0
    # grow the bracket
    while simulate_success(a, L, t_hi, tau, reps, seed)[which] >= P0:
        t_hi *= 2.0
        if t_hi > 200:
            break
    lo, hi = t_lo, t_hi
    trace = []
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        succ = simulate_success(a, L, mid, tau, reps, seed)[which]
        trace.append((mid, succ))
        if succ >= P0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), trace

def cmd_sim(args):
    a = math.inf if args.a == "inf" else float(args.a)
    res = {"a": args.a, "tau": args.tau, "reps": args.reps, "P0": args.P0, "seed": args.seed,
           "smoke": args.smoke, "started": time.strftime("%Y-%m-%d %H:%M:%S %Z"), "cells": {}}
    for L in args.L:
        cell = {}
        for which, name in ((0, "unweighted"), (1, "weighted")):
            ts, trace = bisect_tstar(a, L, args.tau, args.reps, args.seed, args.P0, which)
            cell[name] = {"tstar": ts, "trace": trace}
            print(f"a={args.a} L={L} {name}: t*={ts:.4f}", flush=True)
        res["cells"][str(L)] = cell
    res["finished"] = time.strftime("%Y-%m-%d %H:%M:%S %Z")
    json.dump(res, open(args.out, "w"), indent=1)

# ----------------------------------------------------------------------------- prediction

def rate_sample(a, n=400000, seed=12345):
    rng = np.random.default_rng(seed)
    return draw_rates(a, n, rng)

def snr(a, L, t, tau, which, r):
    s = signal(r, t, tau)
    v = variance(r, t, tau)
    if which == 0:
        return math.sqrt(L) * s.mean() / math.sqrt(v.mean())
    return math.sqrt(L * (s * s / v).mean())

def solve_t(a, L, tau, which, kappa, r, lo=1e-4, hi=400.0):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if snr(a, L, mid, tau, which, r) >= kappa:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)

def cmd_predict(args):
    sims = {s["a"]: s for s in (json.load(open(f)) for f in args.sim)}
    fit = sims[args.fit_a]
    out = {"fit_cell": {"a": args.fit_a, "L": args.fit_L}, "kappa": {}, "pred": {}}
    for which, name in ((0, "unweighted"), (1, "weighted")):
        a_fit = math.inf if args.fit_a == "inf" else float(args.fit_a)
        r_fit = rate_sample(a_fit)
        tstar_fit = fit["cells"][str(args.fit_L)][name]["tstar"]
        kappa = snr(a_fit, args.fit_L, tstar_fit, fit["tau"], which, r_fit)
        out["kappa"][name] = kappa
        for a_str, sim in sims.items():
            a = math.inf if a_str == "inf" else float(a_str)
            r = rate_sample(a)
            out["pred"].setdefault(a_str, {})[name] = {
                L: solve_t(a, int(L), sim["tau"], which, kappa, r) for L in sim["cells"]}
    json.dump(out, open(args.out, "w"), indent=1)
    print(json.dumps(out["kappa"]))

# ----------------------------------------------------------------------------- scoring

def local_slope(Ls, ts):
    x, y = np.log(np.array(Ls, float)), np.log(np.array(ts, float))
    return float(np.polyfit(x, y, 1)[0])

def cmd_score(args):
    sims = {s["a"]: s for s in (json.load(open(f)) for f in args.sim)}
    pred = json.load(open(args.pred))
    fitL = str(pred["fit_cell"]["L"]); fitA = pred["fit_cell"]["a"]
    asym = {"0.5": (1 / 3, 0.4), "1.0": (0.25, 1 / 3), "2.0": (1 / 6, 0.25)}
    report = {"verdicts": {}, "readings": {}}
    # V1/V2 exact-curve form, per reader, finite a
    for which, name in ((0, "unweighted"), (1, "weighted")):
        errs = {}
        for a_str, sim in sims.items():
            if a_str == "inf":
                continue
            for L, cell in sim["cells"].items():
                if a_str == fitA and L == fitL:
                    continue
                obs = cell[name]["tstar"]; pr = pred["pred"][a_str][name][L]
                errs[f"{a_str}|{L}"] = (obs - pr) / pr
        worst = max(abs(e) for e in errs.values())
        report["verdicts"][f"V{1 + which}_form_{name}"] = {"pass": worst <= 0.10, "max_rel_err": worst, "rel_err": errs}
    # V3 local slope vs exact-curve local slope (top two octaves), finite a
    v3 = {}
    for a_str, sim in sims.items():
        if a_str == "inf":
            continue
        Ls = sorted(int(L) for L in sim["cells"])[-3:]
        for name in ("unweighted", "weighted"):
            s_obs = local_slope(Ls, [sim["cells"][str(L)][name]["tstar"] for L in Ls])
            s_pr = local_slope(Ls, [pred["pred"][a_str][name][str(L)] for L in Ls])
            v3[f"{a_str}|{name}"] = {"obs": s_obs, "pred_exact": s_pr,
                                     "asymptote": asym[a_str][0 if name == "unweighted" else 1]}
    report["verdicts"]["V3_slopes"] = {"pass": all(abs(v["obs"] - v["pred_exact"]) <= 0.03 for v in v3.values()), "cells": v3}
    # V4 ordering and growth of the ratio, finite a
    v4 = {}
    for a_str, sim in sims.items():
        if a_str == "inf":
            continue
        Ls = sorted(int(L) for L in sim["cells"])
        ratios = [sim["cells"][str(L)]["weighted"]["tstar"] / sim["cells"][str(L)]["unweighted"]["tstar"] for L in Ls]
        v4[a_str] = {"ratios": dict(zip(map(str, Ls), ratios)),
                     "all_gt_one": all(x > 1 for x in ratios), "grows": ratios[-1] > ratios[0]}
    report["verdicts"]["V4_ordering"] = {"pass": all(v["all_gt_one"] and v["grows"] for v in v4.values()), "cells": v4}
    # V5 uniform-rate control: log law, slope 3/16 in ln L, readers agree
    if "inf" in sims:
        sim = sims["inf"]; Ls = sorted(int(L) for L in sim["cells"])
        v5 = {}
        for name in ("unweighted", "weighted"):
            x = np.log(np.array(Ls, float)); y = np.array([sim["cells"][str(L)][name]["tstar"] for L in Ls])
            v5[name] = float(np.polyfit(x, y, 1)[0])
        agree = max(abs(sim["cells"][str(L)]["weighted"]["tstar"] / sim["cells"][str(L)]["unweighted"]["tstar"] - 1) for L in Ls)
        report["verdicts"]["V5_uniform"] = {"pass": all(abs(s / 0.1875 - 1) <= 0.15 for s in v5.values()) and agree <= 0.05,
                                            "slopes": v5, "target": 0.1875, "max_reader_disagreement": agree}
    report["kappa"] = pred["kappa"]
    json.dump(report, open(args.out, "w"), indent=1)
    for k, v in report["verdicts"].items():
        print(k, "PASS" if v["pass"] else "FAIL")

# ----------------------------------------------------------------------------- cli

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sim"); s.add_argument("--a", required=True); s.add_argument("--L", type=int, nargs="+", required=True)
    s.add_argument("--reps", type=int, default=2000); s.add_argument("--tau", type=float, default=1.0)
    s.add_argument("--P0", type=float, default=0.90); s.add_argument("--seed", type=int, default=22)
    s.add_argument("--smoke", action="store_true"); s.add_argument("--out", required=True)
    p = sub.add_parser("predict"); p.add_argument("--sim", nargs="+", required=True); p.add_argument("--fit-a", dest="fit_a", default="0.5")
    p.add_argument("--fit-L", dest="fit_L", type=int, default=256); p.add_argument("--out", required=True)
    c = sub.add_parser("score"); c.add_argument("--sim", nargs="+", required=True); c.add_argument("--pred", required=True); c.add_argument("--out", required=True)
    args = ap.parse_args()
    {"sim": cmd_sim, "predict": cmd_predict, "score": cmd_score}[args.cmd](args)
