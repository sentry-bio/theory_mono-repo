"""PREREG16 simulator. Usage: python3 wedge_sim.py id            -> wedge_id.jsonl
                              python3 wedge_sim.py comp X H      -> wedge_comp_X_H.jsonl"""
import sys, json, math, time
import numpy as np
lam = lambda x: math.sqrt(x / 2)
def evolve(parent, l, rng):
    child = parent.copy(); m = rng.random(parent.shape, dtype=np.float32) >= l
    child[m] = rng.integers(0, 4, size=int(m.sum()), dtype=np.int8); return child
def clade_leaves(root, h, l, rng):
    lvl = root[None, :]
    for _ in range(h): lvl = evolve(np.repeat(lvl, 2, axis=0), l, rng)
    return lvl
def quartet_leaves(h, x, n, rng):
    l = lam(x); root = rng.integers(0, 4, size=n, dtype=np.int8)
    P = evolve(root[None], math.sqrt(l), rng)[0]; Q = evolve(root[None], math.sqrt(l), rng)[0]
    roots = [evolve(P[None], l, rng)[0], evolve(P[None], l, rng)[0], evolve(Q[None], l, rng)[0], evolve(Q[None], l, rng)[0]]
    return [clade_leaves(r, h, l, rng) for r in roots]
def census(lv):
    k = lv.shape[0]; return np.stack([(lv == a).sum(axis=0) for a in range(4)], axis=1).astype(np.float64) - k / 4
def margin(sA, sB, sC, sD):
    d = lambda u, v: (u * v).sum(axis=-1); return d(sA, sB) + d(sC, sD) - d(sA, sC) - d(sB, sD)

def all_distinct(leaves):
    v = np.ascontiguousarray(leaves).view(np.dtype((np.void, leaves.shape[1])))
    return np.unique(v).size == leaves.shape[0]
def run_id():
    with open("wedge_id.jsonl", "w") as f:
        for h in range(2, 11):
            for x in [0.6, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5]:
                rng = np.random.default_rng(16000 + 100 * h + int(round(100 * x))); Ls = []; t0 = time.time()
                for _ in range(200):
                    lv = np.concatenate(quartet_leaves(h, x, 160, rng), axis=0)
                    lo, hi = 0, 160
                    if not all_distinct(lv): Ls.append(None); continue
                    while hi - lo > 1:
                        mid = (lo + hi) // 2
                        if all_distinct(lv[:, :mid]): hi = mid
                        else: lo = mid
                    Ls.append(hi)
                ok = [l for l in Ls if l is not None]
                rec = dict(h=h, x=x, reps=200, failed_at_160=len(Ls) - len(ok),
                           L_id95=float(np.percentile(ok, 95)) if len(ok) == 200 else None, L_id_median=float(np.median(ok)),
                           sec=time.time() - t0)
                f.write(json.dumps(rec) + "\n"); f.flush(); print(rec, flush=True)

def kmer_std(lv):
    a = lv.astype(np.int64); code = a[:, :-3] * 64 + a[:, 1:-2] * 16 + a[:, 2:-1] * 4 + a[:, 3:]
    k, w = code.shape; off = (np.arange(k) * 256)[:, None]
    cnt = np.bincount((code + off).ravel(), minlength=256 * k).reshape(k, 256).astype(np.float64)
    e = w / 256; return (cnt - e) / math.sqrt(e)
def run_comp(x, h):
    with open(f"wedge_comp_{x}_{h}.jsonl", "w") as f:
        for L in [5000, 40000]:
            rng = np.random.default_rng(26000 + 100 * h + int(round(100 * x)) + L // 1000)
            R = 1500; m1, m4, s1, s2, nsite = [], [], 0.0, 0.0, 0; distinct4 = 0; t0 = time.time()
            for _ in range(R):
                cl = quartet_leaves(h, x, L, rng)
                cs = [census(c) for c in cl]
                ms = margin(*cs); s1 += ms.sum(); s2 += (ms * ms).sum(); nsite += ms.size
                m1.append(margin(*[c.sum(axis=0) for c in cs]))
                k4 = [kmer_std(c) for c in cl]
                m4.append(margin(*[k.sum(axis=0) for k in k4]))
                allk = np.concatenate(k4, axis=0); distinct4 += np.unique(allk, axis=0).shape[0] == allk.shape[0]
            m1, m4 = np.array(m1), np.array(m4); mu_s = s1 / nsite; sd_s = math.sqrt(s2 / nsite - mu_s ** 2)
            rec = dict(h=h, x=x, L=L, R=R, site_mean=mu_s, site_sd=sd_s, n_sites=nsite,
                       m1_mean=float(m1.mean()), m1_sd=float(m1.std(ddof=1)),
                       m4_mean=float(m4.mean()), m4_sd=float(m4.std(ddof=1)),
                       frac_reps_all_leaves_distinct_4mer=distinct4 / R, sec=time.time() - t0)
            f.write(json.dumps(rec) + "\n"); f.flush(); print(rec, flush=True)
if __name__ == "__main__":
    run_id() if sys.argv[1] == "id" else run_comp(float(sys.argv[2]), int(sys.argv[3]))
