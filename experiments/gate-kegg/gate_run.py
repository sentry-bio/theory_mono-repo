"""PREREG18 runner: K1 certification, then the gate on S1, S2 and their Gaussian nulls. Writes gate_results.json."""
import collections, csv, io, json, re, sys, time
from contextlib import redirect_stdout
import numpy as np
from scipy.spatial.distance import pdist, squareform
import m3_growth_class as m3
from volume_entropy import delta_hyperbolicity

t0 = time.time()
# ---- K1: the frozen gate's own certification (its __main__), captured
buf = io.StringIO()
with redirect_stdout(buf):
    import runpy
    runpy.run_module("m3_growth_class", run_name="__main__")
cert = buf.getvalue()
m = re.search(r"Gate classified (\d+)/(\d+) hosts correctly", cert)
k1 = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
print(f"K1 certification: {k1[0]}/{k1[1]}  ({time.time()-t0:.0f}s)", flush=True)

# ---- data
z = np.load("kegg_profiles_868.npz", allow_pickle=True)
acc, P = z["accessions"], z["profiles"].astype(np.float64)
def num(a):
    mm = re.search(r"GC[AF]_(\d+)", str(a)); return mm.group(1) if mm else None
tax = {}
with open("reference_manifest.csv") as f:
    for r in csv.DictReader(f):
        tax[num(r["accession"])] = r
rows = [(i, tax[num(a)]) for i, a in enumerate(acc) if num(a) in tax]

def sample_S1():
    rng = np.random.default_rng(0)
    byphy = collections.defaultdict(list)
    for i, t in rows:
        byphy[t["phylum"]].append(i)
    out = []
    for phy, v in byphy.items():
        idx = rng.choice(len(v), min(len(v), 120), replace=False)
        out += [v[j] for j in idx]
    rng.shuffle(out)
    return np.array(out[:5000])

def sample_S2():
    rng = np.random.default_rng(18002)
    return rng.choice(np.array([i for i, _ in rows]), size=1935, replace=False)

def angular(X):
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    D = np.arccos(np.clip(Xn @ Xn.T, -1, 1)) / np.pi
    np.fill_diagonal(D, 0.0)
    return (D + D.T) / 2

def mds_dim(D):
    n = D.shape[0]; J = np.eye(n) - 1.0 / n
    w = np.clip(np.linalg.eigvalsh(-0.5 * J @ (D ** 2) @ J)[::-1], 0, None)
    return max(2, int(round(w.sum() ** 2 / (w ** 2).sum())))

def usable(D, c):
    cur = m3.occupancy_curve(D, root_index=c)
    if cur is None:
        return False
    rho, occ = cur
    return rho.size >= 20 and occ.max() / max(occ.min(), 1) >= 30

def run_gate(D, centres, label):
    res = []
    for c in centres:
        if not usable(D, c):
            res.append(dict(centre=int(c), usable=False)); continue
        g = m3.growth_class(D, root_index=int(c))
        g["centre"] = int(c); g["usable"] = True; res.append(g)
    us = [r for r in res if r["usable"]]
    ne = sum(r["verdict"] == "exponential" for r in us); npo = sum(r["verdict"].startswith("polynomial") for r in us)
    print(f"{label}: usable {len(us)}/{len(centres)}  exponential {ne}  polynomial {npo}  indeterminate {len(us)-ne-npo}  "
          f"h_slope median {np.median([r['h_slope'] for r in us]) if us else float('nan'):.4f}  ({time.time()-t0:.0f}s)", flush=True)
    return res, len(us), ne, npo

out = dict(K1=k1, samples={})
for name, idx in (("S1", sample_S1()), ("S2", sample_S2())):
    X = P[idx]; nz = X.sum(1) > 0; X, idx = X[nz], idx[nz]
    D = angular(X); n = len(idx)
    rng = np.random.default_rng(18001)
    medoid = int(np.argmin(D.sum(1)))
    centres = [medoid] + [int(c) for c in rng.choice(np.delete(np.arange(n), medoid), size=24, replace=False)]
    dim = mds_dim(D)
    rngn = np.random.default_rng(18003)
    Dnull = squareform(pdist(rngn.standard_normal((n, dim))))
    data_res, nu, ne, npo = run_gate(D, centres, f"{name} data (n={n}, dim={dim})")
    null_res, nun, nen, npon = run_gate(Dnull, centres, f"{name} null")
    delta_ratio = delta_hyperbolicity(D) / delta_hyperbolicity(Dnull)
    k2 = nu >= 15 and nun >= 15
    k3 = nu > 0 and ne / nu >= 0.8 and npo / nu <= 0.1
    k4 = nun > 0 and npon / nun >= 0.8
    kpoly = nu > 0 and npo / nu >= 0.8
    k1ok = k1[0] == k1[1] and k1[1] > 0
    verdict = ("CERTIFIED EXPONENTIAL" if (k1ok and k2 and k3 and k4) else
               "CERTIFIED POLYNOMIAL" if (k1ok and k2 and k4 and kpoly) else "INDETERMINATE")
    print(f"{name}: δ-ratio data/null = {delta_ratio:.3f};  K2 {k2}  K3 {k3}  K4 {k4}  -> {verdict}", flush=True)
    out["samples"][name] = dict(n=int(n), dim=int(dim), centres=centres, data=data_res, null=null_res,
                                delta_ratio=float(delta_ratio), K2=k2, K3=k3, K4=k4, verdict=verdict)
json.dump(out, open("gate_results.json", "w"), indent=1)
print("GATE DONE")
