"""
Geometry estimator -- TWO complementary tools:

  delta_hyperbolicity(D)  -- VERDICT: is the metric tree-like / hyperbolic?
      Sampled Gromov 4-point delta, normalized by median distance. Range-
      INDEPENDENT (a local 4-point property), so it works even when there are
      few radial shells -- exactly where ball-growth fails.
          tree-like  -> delta_norm small (~0.04)
          Euclidean  -> delta_norm large (~0.10), grows with dimension

  volume_b(D, unit)       -- QUANTITY: effective branching b = exp(h_vol),
      from the exponential growth rate of N(R). Accurate once geometry is
      confirmed hyperbolic (recovers true b to a few %).

geometry_report() combines them: delta gives the call, volume_b the number.
"""

import numpy as np

DELTA_HYP = 0.060   # delta_norm below this => HYPERBOLIC
DELTA_EUC = 0.085   # delta_norm above this => EUCLIDEAN ; between => INDETERMINATE


def delta_hyperbolicity(D, n_quads=80000, seed=0):
    rng = np.random.default_rng(seed)
    n = D.shape[0]
    med = np.median(D[D > 0])
    q = rng.integers(0, n, size=(n_quads, 4))
    x, y, u, v = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    S = np.sort(np.stack([D[x, y] + D[u, v],
                          D[x, u] + D[y, v],
                          D[x, v] + D[y, u]]), axis=0)
    delta = (S[2] - S[1]) / 2.0
    return float(np.mean(delta) / med)


def volume_b(D, unit, n_R=30):
    d = D[D > 0] / unit
    lo, hi = np.percentile(d, 2), np.percentile(d, 80)
    Rs = np.linspace(lo, hi, n_R)
    Dn = D / unit
    N = np.array([(Dn <= R).sum(axis=1).mean() for R in Rs])
    keep = (N >= 3) & (N <= 0.6 * N.max())
    if keep.sum() < 8:
        return float("nan")
    h_vol = np.polyfit(Rs[keep], np.log(N[keep]), 1)[0]
    return float(np.exp(h_vol))


def geometry_report(D, unit=1.0, seed=0):
    delta = delta_hyperbolicity(D, seed=seed)
    if delta < DELTA_HYP:
        verdict = "HYPERBOLIC"
    elif delta > DELTA_EUC:
        verdict = "EUCLIDEAN"
    else:
        verdict = "INDETERMINATE"
    b = volume_b(D, unit) if verdict == "HYPERBOLIC" else float("nan")
    return {"verdict": verdict, "delta": delta, "b": b}
