#!/usr/bin/env python3
"""Does Test C's HGT-driven accuracy drop recover with more L, at FIXED f
(the way Test A's saturation drop did)? If it plateaus: genuine floor,
confirming the balloon signature. If it keeps rising toward 1: reticulation
is also just an information problem, and the balloon has no instantiation
here after all -- the most consequential possible negative result.

Reasoning for the prediction: transfer_fraction is a FIXED PROPORTION of L
(0.3), not an absolute site count. So growing L sharpens both the vertical
signal (70% of sites) and the donor-consistent signal (30% of sites)
proportionally -- the competition between them should NOT resolve in favor
of either as L grows, unlike Test A where the whole signal was uniformly
weak and averaging fixed it.
"""
import json
import time
import numpy as np
from sim_core import yule_tree, rescale_tree_depth, exact_patristic_matrix, evolve_jc69
from measures import hamming_matrix, jc_correct, sample_quartets, quartet_accuracy
from hgt_core import apply_hgt

N_TIPS = 256
N_QUARTETS = 3000
SEEDS = [0, 1, 2]
D_TREE = 1.0
F_FIXED = [0.15, 0.3]
L_VALUES = [50000, 100000, 200000, 400000, 800000]
TRANSFER_FRACTION = 0.3

BASE_TREE = yule_tree(N_TIPS, seed=42)
TREE = rescale_tree_depth(BASE_TREE, target_root_to_tip=D_TREE)
D_TRUE = exact_patristic_matrix(TREE)
QUARTETS = sample_quartets(N_TIPS, N_QUARTETS, seed=7)


def run_cell(f, L, seed):
    seqs = evolve_jc69(TREE, L=L, seed=seed)
    seqs_hgt, events = apply_hgt(seqs, transfer_rate=f, transfer_fraction=TRANSFER_FRACTION,
                                 seed=seed + 1000)
    p_obs = hamming_matrix(seqs_hgt)
    d_jc, saturated = jc_correct(p_obs)
    res = quartet_accuracy(D_TRUE, d_jc, QUARTETS, obs_valid_mask=~saturated)
    return dict(f=f, L=L, seed=seed,
                acc_decided=res["accuracy_of_decided"],
                frac_undecidable=res["fraction_undecidable"])


if __name__ == "__main__":
    print(f"Floor check: does acc_decided recover with L at fixed f (reticulation), "
          f"the way it did for saturation in Test A?")
    rows = []
    t0 = time.time()
    for f in F_FIXED:
        for L in L_VALUES:
            for seed in SEEDS:
                rows.append(run_cell(f, L, seed))
        print(f"  f={f} done  [{time.time()-t0:.0f}s elapsed]")

    json.dump(rows, open("testC_floor_results.json", "w"), indent=1)

    print("\n" + "=" * 60)
    for f in F_FIXED:
        print(f"\nf={f}:")
        for L in L_VALUES:
            vals = [r["acc_decided"] for r in rows if r["f"] == f and r["L"] == L]
            print(f"  L={L:7d}  acc_decided={np.mean(vals):.4f} (+/-{np.std(vals):.4f})")

        Ls = np.array(L_VALUES, dtype=float)
        accs = np.array([np.mean([r["acc_decided"] for r in rows if r["f"] == f and r["L"] == L])
                         for L in L_VALUES])
        x = 1.0 / np.sqrt(Ls)
        A = np.column_stack([np.ones_like(x), x])
        c = np.linalg.lstsq(A, accs, rcond=None)[0]
        print(f"  extrapolated asymptote (1-c/sqrt(L) fit): {c[0]:.4f}"
              f"  [predict FLOOR well below 1.0 if genuine balloon]")
