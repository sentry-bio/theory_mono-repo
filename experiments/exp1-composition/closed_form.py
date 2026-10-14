"""POST HOC (written after PREREG16 was scored; cannot change its verdict).
Parameter-free second-moment predictions for the composition readers in PREREG16 arm C.

Exact facts used (JC69, iid uniform root, sites independent):
- Cov(1[x_u = a], 1[x_v = b]) = lambda^d * (4*delta_ab - 1)/16 for leaves u, v at path length d.
- For overlapping 4-mer windows at offset delta, Cov(I_a(w_u), I_b(w_v)) = 4^-8 [prod_{aligned}(1 + lambda^d K) - 1],
  K(x, y) = 4*delta_xy - 1; the product expands into modes j = number of aligned positions kept, each ~ lambda^(j d).
- Clade census covariances C_XY = sum_{u in X, v in Y} G(d(u, v)); margin = sum_k s_k X_k . Y_k.
- Mean = sum_k s_k tr C_{x_k y_k}  (exact).  Gaussian (Isserlis) variance =
  sum_{k,l} s_k s_l [tr(C_{x_k x_l} C_{y_k y_l}) + tr(C_{x_k y_l} C_{y_k x_l})].
- Letter-count margin over L sites: Var = L Var_site + L(L-1) P exactly, P = the Isserlis value per site, so
  L_eff,1 = Var_site / P as L grows; it equals 1 only if the single-site margin is Gaussian.
- Composition sums over ~L^2 window pairs, so its Gaussian variance is leading order (CLT), L-independent after
  standardisation.
"""
import json, math, glob, itertools
import numpy as np
lam = lambda x: math.sqrt(x / 2)
dig = np.array([[(a >> (2 * (3 - i))) & 3 for i in range(4)] for a in range(256)])
def Kmat(iu, iv): return 4.0 * (dig[:, iu][:, None] == dig[:, iv][None, :]) - 1.0
H = {j: np.zeros((256, 256)) for j in range(1, 5)}            # 4-mer modes, G4(d) = sum_j lambda^(j d) H_j
for delta in range(-3, 4):
    o = 4 - abs(delta)
    pairs = [(i + delta, i) if delta >= 0 else (i, i - delta) for i in range(o)]
    for j in range(1, o + 1):
        for S in itertools.combinations(pairs, j):
            M = np.ones((256, 256))
            for iu, iv in S: M = M * Kmat(iu, iv)
            H[j] += 256 * 4.0 ** -8 * M
H1 = {1: (np.eye(4) - 0.25) / 4}                               # per-site census, G1(d) = lambda^d Pi
def G(Hm, d, l, jmax=4): return sum(l ** (j * d) * Hm[j] for j in Hm if j <= jmax)
def stats(Hm, h, x, jmax=4):
    l = lam(x)
    within = sum((2 ** h if d == 0 else 2 ** h * 2 ** (d // 2 - 1)) * G(Hm, d, l, jmax) for d in [0] + [2 * j for j in range(1, h + 1)])
    sib, cross = 4 ** h * G(Hm, 2 * h + 2, l, jmax), 4 ** h * G(Hm, 2 * h + 3, l, jmax)
    def C(X, Y):
        if X == Y: return within
        return sib if {X, Y} in ({"A", "B"}, {"C", "D"}) else cross
    T = [("A", "B", 1), ("C", "D", 1), ("A", "C", -1), ("B", "D", -1)]
    E = sum(s * np.trace(C(a, b)) for a, b, s in T)
    V = sum(s * t * (np.sum(C(a, c) * C(b, d)) + np.sum(C(a, d) * C(b, c))) for a, b, s in T for c, d, t in T)
    return E, V
if __name__ == "__main__":
    rows = []
    for fn in sorted(glob.glob("wedge_comp_*.jsonl")):
        for r in map(json.loads, open(fn)):
            x, h, L = r["x"], r["h"], r["L"]
            E1, P = stats(H1, h, x)
            Em = 2 * 0.75 * 4 ** h * lam(x) ** (2 * h + 2) * (1 - lam(x))
            assert abs(E1 - Em) < 1e-9 * max(1, abs(Em))
            r_meas = Em / r["site_sd"]
            E4, V4 = stats(H, h, x); z4p = E4 / math.sqrt(V4)
            Ej = [stats(H, h, x, jmax=j)[0] for j in range(1, 5)]
            rows.append(dict(x=x, h=h, L=L,
                             Leff1_pred=r["site_sd"] ** 2 / P,
                             Leff1_meas=(L * r["site_sd"] / r["m1_sd"]) ** 2,
                             z1_pred_gauss=E1 / math.sqrt(P), z1_meas=r["m1_mean"] / r["m1_sd"],
                             z4_pred=z4p, z4_meas=r["m4_mean"] / r["m4_sd"], z_se=1 / math.sqrt(r["R"]),
                             Leff4_pred=(z4p / r_meas) ** 2, Leff4_meas=(r["m4_mean"] / r["m4_sd"] / r_meas) ** 2,
                             mean_share_by_mode=[(Ej[0]) / E4] + [(Ej[j] - Ej[j - 1]) / E4 for j in range(1, 4)]))
    json.dump(rows, open("posthoc_closed_form.json", "w"), indent=1)
    print(f"{'x':>4} {'h':>2} {'L':>6} | {'Leff1 pred':>10} {'meas':>6} | {'z4 pred':>7} {'meas':>7} ±{'se':>5} | {'Leff4 pred':>10} {'meas':>6} | mean share j=1..4")
    for q in rows:
        print(f"{q['x']:>4} {q['h']:>2} {q['L']:>6} | {q['Leff1_pred']:10.3f} {q['Leff1_meas']:6.3f} | {q['z4_pred']:7.3f} {q['z4_meas']:7.3f} ±{q['z_se']:.3f} | "
              f"{q['Leff4_pred']:10.2f} {q['Leff4_meas']:6.2f} | " + " ".join(f"{s:5.2f}" for s in q["mean_share_by_mode"]))
