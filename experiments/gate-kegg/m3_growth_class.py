#!/usr/bin/env python3
"""M3 growth-class gate: exponential vs polynomial, by model comparison.

E1 Arm C finding: the meter's occupancy slope returns a substantially positive
value on polynomial hosts at realistic n (3D grid, n=1728 -> 0.322, vs 0.594
for a genuine hyperbolic host). A single slope therefore cannot enforce
Corollary 4.3.

A first attempt at a size-scaling gate failed: randomly subsampling a fixed
matrix thins points without shrinking the space, so the slope does not decay.

The correct discriminator needs no subsampling. It is a model comparison on the
SAME ball-occupancy curve the meter already computes:

    exponential host:  P(rho) ~ exp(h rho)   =>  log P linear in rho
    polynomial host:   P(rho) ~ rho^d        =>  log P linear in log rho

Fit both, compare adjusted R^2. The winner names the growth class. Only when
the exponential model wins may the slope be reported as a packing entropy;
when the polynomial model wins, h_pack is 0 by Corollary 4.3 and the point
value is a finite-window artifact.
"""
import math
import numpy as np


def build_bary_tree_graph(b, depth):
    parents = [-1]
    frontier = [0]
    node_depth = [0]
    for d in range(depth):
        new_frontier = []
        for u in frontier:
            for _ in range(b):
                parents.append(u)
                node_depth.append(d+1)
                new_frontier.append(len(parents)-1)
        frontier = new_frontier
    n = len(parents)
    adj = [[] for _ in range(n)]
    for v, u in enumerate(parents):
        if u >= 0:
            adj[u].append(v); adj[v].append(u)
    return adj, np.array(node_depth), np.array(parents)


def bfs_all_pairs(adj):
    from collections import deque
    n = len(adj)
    D = np.full((n, n), np.inf)
    for s in range(n):
        D[s, s] = 0
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for v in adj[u]:
                if D[s, v] == np.inf:
                    D[s, v] = D[s, u] + 1
                    dq.append(v)
    return D


def euclidean_grid(side, dim=2):
    """Product-space null: a dim-dimensional integer grid graph (polynomial growth)."""
    import itertools
    coords = list(itertools.product(range(side), repeat=dim))
    idx = {c: i for i, c in enumerate(coords)}
    n = len(coords)
    adj = [[] for _ in range(n)]
    for c in coords:
        i = idx[c]
        for d in range(dim):
            cu = list(c); cu[d] += 1
            if cu[d] < side:
                j = idx[tuple(cu)]
                adj[i].append(j); adj[j].append(i)
    return adj

# ---------------------------------------------------------------------------
# M1: beta from the generator directly (ground truth, no metric involved)
# M2: c, radius (hyperboloid distance from root) vs generative depth R
# ---------------------------------------------------------------------------


def euclidean_random_tree(n, dim, rng):
    pos = rng.normal(size=(n, dim)).cumsum(axis=0)
    parent = np.zeros(n, dtype=int)
    for i in range(1, n):
        d = ((pos[:i] - pos[i])**2).sum(axis=1)
        parent[i] = int(np.argmin(d))
    adj = [[] for _ in range(n)]
    for i in range(1, n):
        p = parent[i]; adj[p].append(i); adj[i].append(p)
    return adj


def build_exact_radius_hyperbolic(b, depth, c_true, kappa, rng, max_points=20000):
    """Positions with EXACT radius r = c_true * generation (no boost-composition
    drift): angle assigned uniformly at random per point, independent of tree
    topology. This isolates M2/M3 estimator behavior from embedding distortion
    (which build_bary_hyperbolic_tree above shows is substantial at fixed,
    theory-scaled edge length -- see chat). Not tree-additive by design (no
    quartet-defect claim is made for this generator); it is a clean positive
    control for the radial-growth estimators only.

    Uses the TRUE b^g point count at every generation (no artificial per-
    generation cap -- that would bias the measured growth rate downward by
    under-representing high generations relative to the true combinatorial
    process). Caller is responsible for choosing (b, depth) so the total
    point count stays tractable; max_points is a hard safety ceiling that
    raises rather than silently truncating, since silent truncation would
    corrupt the ground-truth growth rate being tested.
    """
    total = sum(b ** g for g in range(depth + 1))
    if total > max_points:
        raise ValueError(
            f"b={b}, depth={depth} gives {total} points > max_points={max_points}; "
            "reduce depth for this b rather than truncating generations (that "
            "would bias the ground-truth growth rate)."
        )
    node_depth_list = [np.full(b ** g, g) for g in range(depth + 1)]
    node_depth = np.concatenate(node_depth_list).astype(float)
    n = node_depth.size
    theta = rng.uniform(0, 2 * math.pi, size=n)
    r = c_true * node_depth  # exact by construction
    sk = math.sqrt(kappa)
    # law of cosines in H^2_kappa
    R = r[:, None]
    Th = theta[:, None]
    cosh_r = np.cosh(sk * R)
    sinh_r = np.sinh(sk * R)
    cross = cosh_r @ cosh_r.T - (sinh_r @ sinh_r.T) * np.cos(Th - Th.T)
    cross = np.clip(cross, 1.0, None)
    D = np.arccosh(cross) / sk
    np.fill_diagonal(D, 0.0)
    D = (D + D.T) / 2.0
    return D, node_depth


def occupancy_curve(D, root_index=0, min_count=3, max_fraction=0.5, points=40):
    """Ball occupancy P(rho) from one center -- same window policy as the meter."""
    d = np.sort(D[root_index])
    n = d.size
    max_count = min(n - 1, int(math.floor(max_fraction * n)))
    if max_count - min_count < 3:
        return None
    want = np.unique(np.linspace(min_count, max_count,
                                 num=min(points, max_count), dtype=int))
    radii = d[np.clip(want - 1, 0, n - 1)]
    occ = np.searchsorted(d, radii, side="right")
    keep = radii > 0
    radii, occ = radii[keep], occ[keep]
    ur, ui = np.unique(radii, return_index=True)
    return ur, occ[ui]


def _adj_r2(x, y):
    A = np.column_stack([np.ones_like(x), x])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ coef
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    if ss_tot <= 0:
        return 1.0, float(coef[1])
    r2 = 1 - ss_res / ss_tot
    k = x.size
    adj = 1 - (1 - r2) * (k - 1) / max(1, k - 2)
    return float(adj), float(coef[1])


def growth_class(D, root_index=0, margin=0.01):
    """Return dict with exponential/polynomial fit quality and a verdict."""
    cur = occupancy_curve(D, root_index=root_index)
    if cur is None:
        return dict(verdict="indeterminate")
    rho, P = cur
    logP = np.log(P.astype(float))
    r2_exp, slope_exp = _adj_r2(rho.astype(float), logP)          # log P vs rho
    r2_poly, slope_poly = _adj_r2(np.log(rho.astype(float)), logP)  # log P vs log rho
    if r2_exp > r2_poly + margin:
        verdict = "exponential"
    elif r2_poly > r2_exp + margin:
        verdict = "polynomial(h_pack~0)"
    else:
        verdict = "indeterminate"
    return dict(verdict=verdict, r2_exp=r2_exp, r2_poly=r2_poly,
                h_slope=slope_exp, poly_dim=slope_poly, n_radii=int(rho.size))


if __name__ == "__main__":
    print("=" * 88)
    print("M3 GROWTH-CLASS GATE   (adjusted R^2: log P vs rho   [EXP]   |   log P vs log rho  [POLY])")
    print("=" * 88)
    print(f"{'space':26s}{'n':>6s}{'h_slope':>9s}{'R2_exp':>9s}{'R2_poly':>9s}{'polyD':>7s}  verdict")
    print("-" * 88)

    cases = []
    for b, depth in ((2, 9), (3, 6), (4, 5)):
        adj, nd, par = build_bary_tree_graph(b, depth)
        cases.append((f"tree b={b} d={depth} [EXP]", bfs_all_pairs(adj), "EXP"))
    for kappa in (0.5, 1.0, 2.0):
        rng = np.random.default_rng(5)
        c_true = math.log(3) / math.sqrt(kappa)
        D, nd = build_exact_radius_hyperbolic(3, 6, c_true, kappa, rng)
        cases.append((f"H2 k={kappa} [EXP]", D, "EXP"))
    for dim, side in ((2, 20), (2, 28), (2, 40), (3, 10), (3, 12)):
        adj = euclidean_grid(side, dim=dim)
        cases.append((f"{dim}D grid s={side} [POLY]", bfs_all_pairs(adj), "POLY"))
    for n_nodes in (800, 1500):
        rng = np.random.default_rng(3)
        adj = euclidean_random_tree(n_nodes, 2, rng)
        cases.append((f"euclid MST n={n_nodes} [POLY]", bfs_all_pairs(adj), "POLY"))

    correct = total = 0
    for name, D, truth in cases:
        g = growth_class(D, root_index=0)
        ok = (truth == "EXP" and g["verdict"] == "exponential") or \
             (truth == "POLY" and g["verdict"] == "polynomial(h_pack~0)")
        correct += int(ok); total += 1
        print(f"{name:26s}{D.shape[0]:6d}{g['h_slope']:9.4f}{g['r2_exp']:9.4f}"
              f"{g['r2_poly']:9.4f}{g['poly_dim']:7.2f}  {g['verdict']:22s}"
              f"{'OK ' if ok else 'MISS'}")
    print("-" * 88)
    print(f"Gate classified {correct}/{total} hosts correctly.")
