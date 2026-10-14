"""PREREG19b: block structure of wrongly decided quartets against the exact exchangeable-sites null.

Usage: python3 testB_perm.py GEN D SEED    (GEN in T Cstar; L = 800,000)  -> appends one line to testB_perm.jsonl
       python3 testB_perm.py score         -> scores the registered rule from testB_perm.jsonl
The quartet reader is the registered one (JC-corrected four-point on the full alignment). For a quartet it decides
wrongly, the per-site margin m_s = δ_T(s) − δ_W(s) (raw mismatch pair-sums of the true and the chosen split) is
summed over 20 contiguous windows; φ = sample variance of the 20 sums / its expectation under a random partition of
the sites (hypergeometric, with the K/(K−1) partition factor), so φ ~ χ²₁₉/19 under exchangeable sites."""
import json
import sys
import time

import numpy as np

from sim_core import yule_tree, rescale_tree_depth, exact_patristic_matrix, evolve_jc69
from measures import hamming_matrix, jc_correct, sample_quartets, quartet_topology
from hgt_core import apply_hgt
from misspec_core import evolve_heterotachy

N_TIPS, N_Q, L, WINDOWS, MAXQ = 256, 3000, 800_000, 20, 200
PHI95 = 30.1435 / 19                                   # 95th percentile of chi-square(19) / 19
SPLITS = {0: ((0, 1), (2, 3)), 1: ((0, 2), (1, 3)), 2: ((0, 3), (1, 2))}   # measures.quartet_topology's convention


def generate(gen, tree, seed):
    if gen == "T":
        return evolve_heterotachy(tree, L, 300 + seed)[0]
    if gen == "Cstar":
        seqs = evolve_jc69(tree, L=L, seed=seed)
        return apply_hgt(seqs, transfer_rate=0.30, transfer_fraction=0.30, seed=seed + 1000)[0]
    raise ValueError(gen)


def phi_of(seqs, tips, t_true, t_wrong):
    def delta(split):
        (i, j), (k, l) = split
        return (seqs[tips[i]] != seqs[tips[j]]).astype(np.int8) + (seqs[tips[k]] != seqs[tips[l]]).astype(np.int8)
    m = delta(SPLITS[t_true]).astype(np.float64) - delta(SPLITS[t_wrong])
    edges = np.linspace(0, L, WINDOWS + 1).astype(int)
    sums = np.array([m[edges[w]:edges[w + 1]].sum() for w in range(WINDOWS)])
    w = L // WINDOWS
    var_obs = sums.var(ddof=1)
    var_null = w * m.var() * (L - w) / (L - 1) * WINDOWS / (WINDOWS - 1)
    return (float(var_obs / var_null) if var_null > 0 else float("nan")), float(m.sum())


def score():
    rows = [json.loads(l) for l in open("testB_perm.jsonl")]
    out = {}
    for gen in ("Cstar", "T"):
        for D in (1.0, 2.0):
            cells = [r for r in rows if r["gen"] == gen and r["D"] == D and r["frac_blocked"] is not None]
            fb = float(np.mean([r["frac_blocked"] for r in cells])) if cells else None
            nq = int(sum(r["n_wrong_scored"] for r in cells))
            med = float(np.median([x for r in cells for x in r["phi"]])) if cells else None
            out[f"{gen}|{D}"] = dict(n_seeds=len(cells), frac_blocked=fb, n_quartets=nq, phi_median=med)
            print(f"{gen:6s} D={D}: seeds {len(cells)}  BLOCKED fraction {fb}  median φ {med}  (wrong quartets {nq})")
    ok_c = all(out[f"Cstar|{D}"]["frac_blocked"] is not None and out[f"Cstar|{D}"]["frac_blocked"] >= 0.70 for D in (1.0, 2.0))
    ok_t = all(out[f"T|{D}"]["frac_blocked"] is not None and out[f"T|{D}"]["frac_blocked"] <= 0.30 for D in (1.0, 2.0))
    verdict = "BLOCK DISCRIMINATOR WORKS" if (ok_c and ok_t) else "FAILS"
    print("PREREG19b verdict:", verdict)
    json.dump(dict(cells=out, verdict=verdict, rule="Cstar >= 0.70 and T <= 0.30 BLOCKED at both depths; phi > chi2_19/19 95th pct"),
              open("testB_perm_score.json", "w"), indent=1)


if __name__ == "__main__":
    if sys.argv[1] == "score":
        score(); sys.exit(0)
    gen, D, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    t0 = time.time()
    tree = rescale_tree_depth(yule_tree(N_TIPS, seed=42), target_root_to_tip=D)
    D_true = exact_patristic_matrix(tree)
    Q = sample_quartets(N_TIPS, N_Q, seed=7)
    seqs = generate(gen, tree, seed)
    d_jc, sat = jc_correct(hamming_matrix(seqs))
    phis, margins = [], []
    for (a, b, c, d) in Q:
        tt = quartet_topology(D_true, a, b, c, d)
        if tt == -1:
            continue
        pairs = [(a, b), (c, d), (a, c), (b, d), (a, d), (b, c)]
        if any(sat[x] for x in pairs):
            continue
        ot = quartet_topology(d_jc, a, b, c, d)
        if ot != -1 and ot != tt:
            phi, mg = phi_of(seqs, [int(a), int(b), int(c), int(d)], tt, ot)
            phis.append(phi); margins.append(mg)
        if len(phis) >= MAXQ:
            break
    phis = np.array(phis)
    rec = dict(gen=gen, D=D, seed=seed, L=L, n_wrong_scored=int(len(phis)),
               frac_blocked=(float((phis > PHI95).mean()) if len(phis) else None),
               phi_median=(float(np.median(phis)) if len(phis) else None),
               margin_median=(float(np.median(margins)) if margins else None),
               phi=[round(float(x), 3) for x in phis], sec=time.time() - t0)
    with open("testB_perm.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    print({k: v for k, v in rec.items() if k != "phi"}, flush=True)
