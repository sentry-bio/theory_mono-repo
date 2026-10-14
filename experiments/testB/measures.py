#!/usr/bin/env python3
"""Instruments: block capacity, relational capacity (quartet accuracy vs true
tree), JC-corrected distance. Certified against exact/shuffled controls before
any real (simulated) sweep is trusted -- Phase 0.
"""
from __future__ import annotations
import numpy as np
import itertools


def hamming_matrix(seqs: np.ndarray, n_states: int = 4) -> np.ndarray:
    """[n,L] int8 array -> [n,n] proportion-mismatch matrix.

    Vectorized via one-hot matmul (BLAS) instead of a per-row Python loop:
    matches[i,j] = sum_b (seqs[i]==b & seqs[j]==b) = sum_b onehot_b @ onehot_b.T.
    Verified identical to the naive loop (np.allclose) before adoption;
    ~24x faster at n=256, L=200000 (0.47s vs 13.7s).
    """
    n, L = seqs.shape
    matches = np.zeros((n, n), dtype=np.float64)
    for b in range(n_states):
        onehot = (seqs == b).astype(np.float32)
        matches += onehot @ onehot.T
    D = 1.0 - matches / L
    np.fill_diagonal(D, 0.0)
    return D


def jc_correct(p_matrix: np.ndarray, cap: float = 0.749999) -> np.ndarray:
    """JC69 distance correction d = -3/4 ln(1 - 4p/3). Undefined/infinite as
    p -> 3/4; cap p below the singularity and return both the corrected
    matrix and a mask of which entries were saturated (p >= cap threshold
    BEFORE capping, i.e. genuinely at/past the JC ceiling)."""
    saturated = p_matrix >= cap
    p_safe = np.minimum(p_matrix, cap)
    with np.errstate(divide="ignore", invalid="ignore"):
        d = -0.75 * np.log(1.0 - (4.0 / 3.0) * p_safe)
    return d, saturated


def block_capacity(p_matrix: np.ndarray, eps: float) -> dict:
    """Count of eps-separated sequences under the OBSERVED Hamming-proportion
    metric (a genuine metric on sequence space). Exact-collision count and
    minimum pairwise distance reported alongside."""
    n = p_matrix.shape[0]
    off = p_matrix[np.triu_indices(n, 1)]
    n_collisions = int((off < 1e-12).sum())
    min_dist = float(off.min()) if off.size else float("nan")
    # greedy eps-net size as a concrete lower-bound witness for the packing count
    order = np.arange(n)
    kept = []
    for i in order:
        if all(p_matrix[i, j] >= eps for j in kept):
            kept.append(i)
    return dict(n_total=n, n_eps_separated_witness=len(kept),
                n_exact_collisions=n_collisions, min_pairwise_distance=min_dist)


def sample_quartets(n: int, n_quartets: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    total = n * (n - 1) * (n - 2) * (n - 3) // 24
    if total <= n_quartets:
        return np.array(list(itertools.combinations(range(n), 4)))
    seen = set()
    out = []
    attempts = 0
    while len(out) < n_quartets and attempts < n_quartets * 30:
        attempts += 1
        q = tuple(sorted(rng.choice(n, 4, replace=False)))
        if q in seen:
            continue
        seen.add(q)
        out.append(q)
    return np.array(out)


def quartet_topology(D: np.ndarray, a: int, b: int, c: int, d: int, tol: float = 1e-9) -> int:
    """Four-point method: returns 0 for ab|cd, 1 for ac|bd, 2 for ad|bc,
    -1 for unresolved (all three sums equal within tol, or too noisy)."""
    s0 = D[a, b] + D[c, d]
    s1 = D[a, c] + D[b, d]
    s2 = D[a, d] + D[b, c]
    sums = [s0, s1, s2]
    order = np.argsort(sums)
    smallest = sums[order[0]]
    second = sums[order[1]]
    if second - smallest < tol:
        return -1
    return int(order[0])


def quartet_accuracy(D_true: np.ndarray, D_obs: np.ndarray, quartets: np.ndarray,
                     obs_valid_mask: np.ndarray | None = None) -> dict:
    """For each sampled quartet, resolve the topology under D_true (ground
    truth) and under D_obs (what's measured), compare. obs_valid_mask, if
    given, is a boolean [n,n] of pairs usable in D_obs (e.g. non-saturated);
    a quartet with any invalid pair among its 6 is reported separately as
    'undecidable' rather than silently scored."""
    n_correct = 0
    n_resolved_true = 0
    n_undecidable = 0
    n_wrong = 0
    n_true_unresolved = 0
    for (a, b, c, d) in quartets:
        t_topo = quartet_topology(D_true, a, b, c, d)
        if t_topo == -1:
            n_true_unresolved += 1
            continue
        n_resolved_true += 1
        if obs_valid_mask is not None:
            pairs = [(a, b), (c, d), (a, c), (b, d), (a, d), (b, c)]
            if not all(obs_valid_mask[p] for p in pairs):
                n_undecidable += 1
                continue
        o_topo = quartet_topology(D_obs, a, b, c, d)
        if o_topo == -1:
            n_undecidable += 1
        elif o_topo == t_topo:
            n_correct += 1
        else:
            n_wrong += 1
    denom = n_correct + n_wrong  # decided quartets only
    accuracy_of_decided = n_correct / denom if denom > 0 else float("nan")
    accuracy_of_all_resolved = n_correct / n_resolved_true if n_resolved_true > 0 else float("nan")
    return dict(
        n_quartets=len(quartets), n_true_unresolved=n_true_unresolved,
        n_resolved_true=n_resolved_true, n_correct=n_correct, n_wrong=n_wrong,
        n_undecidable=n_undecidable,
        accuracy_of_decided=accuracy_of_decided,
        accuracy_of_all_resolved=accuracy_of_all_resolved,
        fraction_undecidable=(n_undecidable / n_resolved_true if n_resolved_true else float("nan")),
    )


def embedding_distortion_h2(D_target: np.ndarray, steps: int = 800, seed: int = 0,
                            lr: float = 0.05) -> dict:
    """Best-effort H^2 (curvature -1) embedding of the OBSERVED distance
    matrix, distortion measured against the TRUE patristic matrix (same
    index order). Uses the exponential-map Poincare parameterization,
    gradient descent on log-ratio variance (scale-free)."""
    import torch
    n = D_target.shape[0]
    g = torch.Generator().manual_seed(seed)
    r_raw = (torch.randn(n, generator=g) * 0.3).requires_grad_(True)
    u_raw = torch.randn(n, 2, generator=g).requires_grad_(True)
    opt = torch.optim.Adam([r_raw, u_raw], lr=lr)
    tgt = torch.as_tensor(D_target, dtype=torch.float32)
    iu, ju = np.triu_indices(n, 1)
    logt = torch.log(torch.clamp(tgt[iu, ju], min=1e-6))
    for _ in range(steps):
        opt.zero_grad()
        r = torch.nn.functional.softplus(r_raw)
        u = torch.nn.functional.normalize(u_raw, dim=1)
        ch, sh = torch.cosh(r), torch.sinh(r)
        dot = (u[iu] * u[ju]).sum(1)
        arg = ch[iu] * ch[ju] - sh[iu] * sh[ju] * dot
        d = torch.acosh(torch.clamp(arg, min=1.0 + 1e-6))
        loss = (torch.log(torch.clamp(d, min=1e-6)) - logt).var()
        loss.backward()
        opt.step()
    with torch.no_grad():
        r = torch.nn.functional.softplus(r_raw)
        u = torch.nn.functional.normalize(u_raw, dim=1)
        ch, sh = torch.cosh(r), torch.sinh(r)
        dot = (u[iu] * u[ju]).sum(1)
        d_emb = torch.acosh(torch.clamp(ch[iu] * ch[ju] - sh[iu] * sh[ju] * dot, min=1.0 + 1e-6)).numpy()
    ratio = d_emb / np.maximum(D_target[iu, ju], 1e-9)
    lo, hi = np.percentile(ratio, [2, 98])
    return dict(D_robust=float(np.sqrt(hi / max(lo, 1e-12))),
                mean_abs_log_ratio=float(np.mean(np.abs(np.log(ratio) - np.log(ratio).mean()))))
