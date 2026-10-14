"""PREREG19 generators: sequence evolution under three models the JC reader does not assume. No transfer anywhere.
All three share sim_core's tree conventions (parent, branch_len, node_depth; root = the node with parent -1)."""
from __future__ import annotations
import numpy as np
from scipy.linalg import expm


def _order(tree):
    root = int(np.where(tree.parent == -1)[0][0])
    return root, [int(n) for n in np.argsort(tree.node_depth) if int(n) != root]


def _jc_step(parent_bases, t_site, rng):
    """JC69 with a per-site branch length t_site (array of length L)."""
    p_same = 0.25 + 0.75 * np.exp(-4.0 * t_site / 3.0)
    change = rng.random(parent_bases.shape[0]) >= p_same
    new = parent_bases.copy()
    k = int(change.sum())
    if k:
        new[change] = (parent_bases[change] + rng.integers(1, 4, size=k)) % 4
    return new


def evolve_gamma(tree, L, seed, alpha=0.5):
    """JC69 with per-site rates r_s ~ Gamma(alpha, mean 1), shared across the tree."""
    rng = np.random.default_rng(seed)
    rates = rng.gamma(alpha, 1.0 / alpha, size=L)
    root, order = _order(tree)
    seqs = np.zeros((tree.n_nodes, L), dtype=np.int8)
    seqs[root] = rng.integers(0, 4, size=L)
    for node in order:
        seqs[node] = _jc_step(seqs[int(tree.parent[node])], float(tree.branch_len[node]) * rates, rng)
    return seqs[tree.tip_ids]


def hky_P(t, pi, kappa):
    """HKY85 transition matrix for branch length t (expected substitutions per site, mean-rate normalised).
    Base order A, C, G, T; transitions A<->G, C<->T."""
    pi = np.asarray(pi, float)
    Q = np.zeros((4, 4))
    for i in range(4):
        for j in range(4):
            if i == j:
                continue
            ti = (i, j) in ((0, 2), (2, 0), (1, 3), (3, 1))
            Q[i, j] = (kappa if ti else 1.0) * pi[j]
    Q[np.diag_indices(4)] = -Q.sum(1)
    mu = -(pi * np.diag(Q)).sum()                       # mean rate; normalise to one substitution per unit t
    return expm(Q * t / mu)


def evolve_hky(tree, L, seed, pi=(0.15, 0.35, 0.35, 0.15), kappa=4.0):
    """HKY85 with skewed equilibrium frequencies; root drawn from pi."""
    rng = np.random.default_rng(seed)
    pi = np.asarray(pi, float)
    root, order = _order(tree)
    seqs = np.zeros((tree.n_nodes, L), dtype=np.int8)
    seqs[root] = rng.choice(4, size=L, p=pi)
    cache = {}
    for node in order:
        t = float(tree.branch_len[node])
        if t not in cache:
            cache[t] = hky_P(t, pi, kappa)
        P = cache[t]
        parent = seqs[int(tree.parent[node])]
        child = np.empty(L, dtype=np.int8)
        for b in range(4):
            m = parent == b
            k = int(m.sum())
            if k:
                child[m] = rng.choice(4, size=k, p=P[b])
        seqs[node] = child
    return seqs[tree.tip_ids]


def descendants(tree, node):
    """Tip indices (positions in tree.tip_ids) below `node`, inclusive if node is a tip."""
    kids = {}
    for c, p in enumerate(tree.parent):
        if p >= 0:
            kids.setdefault(int(p), []).append(int(c))
    stack, tips = [int(node)], []
    tip_pos = {int(t): i for i, t in enumerate(tree.tip_ids)}
    while stack:
        v = stack.pop()
        if v in tip_pos:
            tips.append(tip_pos[v])
        stack.extend(kids.get(v, []))
    return sorted(tips)


def two_clades(tree, max_tips=None):
    """The two largest disjoint clades with at most max_tips tips (default n_tips/4, i.e. 64 on the registered 256-tip
    tree), chosen from the tree alone. Returns node ids."""
    if max_tips is None:
        max_tips = max(2, tree.n_tips // 4)
    sizes = {}
    for v in range(tree.n_nodes):
        sizes[v] = len(descendants(tree, v))
    cands = sorted([v for v in sizes if 2 <= sizes[v] <= max_tips], key=lambda v: -sizes[v])
    A = cands[0]
    tipsA = set(descendants(tree, A))
    for v in cands[1:]:
        if not (set(descendants(tree, v)) & tipsA):
            return A, v
    raise RuntimeError("no disjoint second clade")


def evolve_heterotachy(tree, L, seed, speedup=4.0):
    """JC69 with two equal site classes: class 1 is `speedup`× faster on every branch inside clade A, class 2 inside
    clade B (clades from two_clades). Site rates average to one over the tree only approximately; the point is the
    site-by-lineage interaction, which breaks additivity for the JC reader."""
    rng = np.random.default_rng(seed)
    A, B = two_clades(tree)
    inA = np.zeros(tree.n_nodes, bool); inB = np.zeros(tree.n_nodes, bool)
    kids = {}
    for c, p in enumerate(tree.parent):
        if p >= 0:
            kids.setdefault(int(p), []).append(int(c))
    for root_node, mask in ((A, inA), (B, inB)):
        stack = list(kids.get(int(root_node), []))
        while stack:
            v = stack.pop(); mask[v] = True; stack.extend(kids.get(v, []))
    cls = rng.random(L) < 0.5
    root, order = _order(tree)
    seqs = np.zeros((tree.n_nodes, L), dtype=np.int8)
    seqs[root] = rng.integers(0, 4, size=L)
    for node in order:
        t = np.full(L, float(tree.branch_len[node]))
        if inA[node]:
            t[cls] *= speedup
        if inB[node]:
            t[~cls] *= speedup
        seqs[node] = _jc_step(seqs[int(tree.parent[node])], t, rng)
    return seqs[tree.tip_ids], dict(cladeA=int(A), cladeB=int(B), tipsA=descendants(tree, A), tipsB=descendants(tree, B))
