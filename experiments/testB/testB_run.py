"""PREREG19 runner. Usage: python3 testB_run.py GEN D SEED   (GEN in G H T Cstar) -> appends to testB_cells.jsonl
One call runs all L for that (GEN, D, SEED), reusing nothing across L (fresh sequences per L, same seed stream)."""
import json, sys, time
import numpy as np
from sim_core import yule_tree, rescale_tree_depth, exact_patristic_matrix, evolve_jc69
from measures import hamming_matrix, jc_correct, block_capacity, sample_quartets, quartet_accuracy, quartet_topology
from hgt_core import apply_hgt
from misspec_core import evolve_gamma, evolve_hky, evolve_heterotachy

N_TIPS, N_QUARTETS = 256, 3000
L_VALUES = [50_000, 100_000, 200_000, 400_000, 800_000]
BASE_TREE = yule_tree(N_TIPS, seed=42)
QUARTETS = sample_quartets(N_TIPS, N_QUARTETS, seed=7)
WINDOWS = 20


def generate(gen, tree, L, seed):
    if gen == "G":
        return evolve_gamma(tree, L, 100 + seed), {}
    if gen == "H":
        return evolve_hky(tree, L, 200 + seed), {}
    if gen == "T":
        return evolve_heterotachy(tree, L, 300 + seed)
    if gen == "Cstar":
        seqs = evolve_jc69(tree, L=L, seed=seed)
        seqs, events = apply_hgt(seqs, transfer_rate=0.30, transfer_fraction=0.30, seed=seed + 1000)
        return seqs, dict(n_events=len(events))
    raise ValueError(gen)


def window_discriminator(seqs, D_true, wrong_quartets):
    """For each wrongly decided quartet: fraction of 20 windows voting its majority topology."""
    if not wrong_quartets:
        return None, 0
    n, L = seqs.shape
    edges = np.linspace(0, L, WINDOWS + 1).astype(int)
    votes = {q: [] for q in wrong_quartets}
    for w in range(WINDOWS):
        p = hamming_matrix(seqs[:, edges[w]:edges[w + 1]])
        d, sat = jc_correct(p)
        for q in wrong_quartets:
            a, b, c, dd = q
            pairs = [(a, b), (c, dd), (a, c), (b, dd), (a, dd), (b, c)]
            if any(sat[x] for x in pairs):
                continue
            t = quartet_topology(d, a, b, c, dd)
            if t != -1:
                votes[q].append(t)
    pm = []
    for q, v in votes.items():
        if len(v) >= 10:
            pm.append(np.bincount(v, minlength=3).max() / len(v))
    return (float(np.mean(pm)) if pm else None), len(pm)


if __name__ == "__main__":
    gen, D, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
    tree = rescale_tree_depth(BASE_TREE, target_root_to_tip=D)
    D_true = exact_patristic_matrix(tree)
    Ls = [200_000, 800_000] if gen == "Cstar" else L_VALUES
    with open("testB_cells.jsonl", "a") as f:
        for L in Ls:
            t0 = time.time()
            seqs, extra = generate(gen, tree, L, seed)
            p_obs = hamming_matrix(seqs)
            d_jc, saturated = jc_correct(p_obs)
            res = quartet_accuracy(D_true, d_jc, QUARTETS, obs_valid_mask=~saturated)
            bc = block_capacity(p_obs, eps=0.01)
            rec = dict(gen=gen, D=D, L=L, seed=seed, acc_decided=res["accuracy_of_decided"],
                       frac_undecidable=res["fraction_undecidable"], n_wrong=res["n_wrong"], n_correct=res["n_correct"],
                       block_witness=bc["n_eps_separated_witness"], sec=time.time() - t0, **{k: v for k, v in extra.items() if k != "tipsA" and k != "tipsB"})
            if L == 800_000:
                wrong = []
                for (a, b, c, dd) in QUARTETS:
                    tt = quartet_topology(D_true, a, b, c, dd)
                    if tt == -1:
                        continue
                    pairs = [(a, b), (c, dd), (a, c), (b, dd), (a, dd), (b, c)]
                    if any(saturated[x] for x in pairs):
                        continue
                    ot = quartet_topology(d_jc, a, b, c, dd)
                    if ot != -1 and ot != tt:
                        wrong.append((int(a), int(b), int(c), int(dd)))
                    if len(wrong) >= 200:
                        break
                pm, npm = window_discriminator(seqs, D_true, wrong)
                rec.update(p_major=pm, n_wrong_scored=npm)
            f.write(json.dumps(rec) + "\n"); f.flush()
            print(rec, flush=True)
    print("CELL DONE", gen, D, seed)
