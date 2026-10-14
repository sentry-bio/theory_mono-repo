#!/usr/bin/env python3
"""Core: tree generation, JC69 sequence evolution, exact patristic distances.

All ground truth (tree, patristic distances, root-to-tip depth) is EXACT by
construction. No inference step touches these. Only the sequence-derived
measurements (Hamming distance, JC-corrected distance, quartet resolution)
are estimated from data, which is where saturation is expected to bite.
"""
from __future__ import annotations
import numpy as np
from dataclasses import dataclass


@dataclass
class Tree:
    n_tips: int
    n_nodes: int          # total nodes including internal
    parent: np.ndarray     # [n_nodes], -1 for root
    branch_len: np.ndarray  # [n_nodes], branch length above node (root=0)
    tip_ids: np.ndarray     # indices of tip nodes
    node_depth: np.ndarray  # root-to-node cumulative branch length (EXACT)


def yule_tree(n_tips: int, seed: int, ultrametric: bool = True) -> Tree:
    """Yule (pure-birth) process, standard coalescent-style construction:
    start with n_tips independent lineages, repeatedly join two random
    lineages (uniform, memoryless waiting times ~ Exp(k) at k active
    lineages), producing a binary tree. Ultrametric by construction (each
    tip's root-to-tip depth is the sum of the waiting times along its path,
    which are shared with its sibling structure) -- here we build it as a
    coalescent (looking backward) which gives an ultrametric tree exactly.
    """
    rng = np.random.default_rng(seed)
    # active lineages: list of (node_id, current_depth_from_root_so_far=None)
    # We build backward from tips (depth 0) toward the root, accumulating
    # elapsed time, then invert to get root-to-node depth.
    n_max_nodes = 2 * n_tips - 1
    parent = np.full(n_max_nodes, -1, dtype=np.int64)
    branch_len = np.zeros(n_max_nodes, dtype=np.float64)
    tip_ids = np.arange(n_tips)

    active = list(range(n_tips))
    node_time_from_tips = np.zeros(n_max_nodes, dtype=np.float64)  # elapsed since tip-sampling
    next_id = n_tips
    t = 0.0
    while len(active) > 1:
        k = len(active)
        # Yule: total rate k * birth_rate; birth_rate=1 => coalescent-like waiting time
        wait = rng.exponential(1.0 / k)
        t += wait
        i, j = rng.choice(len(active), size=2, replace=False)
        a, b = active[i], active[j]
        new_node = next_id
        next_id += 1
        parent[a] = new_node
        parent[b] = new_node
        branch_len[a] = t - node_time_from_tips[a]
        branch_len[b] = t - node_time_from_tips[b]
        node_time_from_tips[new_node] = t
        # remove a,b, add new_node
        active = [x for idx, x in enumerate(active) if idx not in (i, j)]
        active.append(new_node)
    root = active[0]
    total_depth = t  # time from tips to root
    # root-to-node depth = total_depth - node_time_from_tips (since tips are at t=0,
    # root is at t=total_depth measured backward; forward root-to-tip is total_depth)
    node_depth = total_depth - node_time_from_tips
    node_depth[root] = 0.0
    n_nodes = next_id
    return Tree(n_tips=n_tips, n_nodes=n_nodes, parent=parent[:n_nodes],
                branch_len=branch_len[:n_nodes], tip_ids=tip_ids,
                node_depth=node_depth[:n_nodes])


def perfect_binary_tree(n_tips: int, depth_per_level: float) -> Tree:
    """Perfect binary tree control: exactly log2(n_tips) levels, equal branch
    lengths. n_tips must be a power of 2."""
    assert (n_tips & (n_tips - 1)) == 0, "n_tips must be a power of 2"
    levels = int(np.log2(n_tips))
    n_nodes = 2 * n_tips - 1
    parent = np.full(n_nodes, -1, dtype=np.int64)
    branch_len = np.zeros(n_nodes, dtype=np.float64)
    node_depth = np.zeros(n_nodes, dtype=np.float64)
    # level-order: root=0
    # node i (0-indexed complete binary tree) has children 2i+1, 2i+2
    for i in range(n_nodes):
        c1, c2 = 2 * i + 1, 2 * i + 2
        if c1 < n_nodes:
            parent[c1] = i
            branch_len[c1] = depth_per_level
            node_depth[c1] = node_depth[i] + depth_per_level
        if c2 < n_nodes:
            parent[c2] = i
            branch_len[c2] = depth_per_level
            node_depth[c2] = node_depth[i] + depth_per_level
    tip_start = n_nodes - n_tips
    tip_ids = np.arange(tip_start, n_nodes)
    return Tree(n_tips=n_tips, n_nodes=n_nodes, parent=parent,
                branch_len=branch_len, tip_ids=tip_ids, node_depth=node_depth)


def rescale_tree_depth(tree: Tree, target_root_to_tip: float) -> Tree:
    """Rescale all branch lengths so mean root-to-tip depth = target D."""
    mean_depth = tree.node_depth[tree.tip_ids].mean()
    if mean_depth <= 0:
        raise ValueError("degenerate tree depth")
    scale = target_root_to_tip / mean_depth
    new = Tree(n_tips=tree.n_tips, n_nodes=tree.n_nodes,
               parent=tree.parent.copy(),
               branch_len=tree.branch_len * scale,
               tip_ids=tree.tip_ids.copy(),
               node_depth=tree.node_depth * scale)
    return new


def exact_patristic_matrix(tree: Tree) -> np.ndarray:
    """Exact pairwise patristic (sum-of-branch-lengths) distance among tips.
    O(n_tips^2 * avg_path_len) via ancestor-chain LCA -- fine at n=512."""
    n = tree.n_tips
    # ancestor chains with cumulative depth
    ancestors = []
    for tid in tree.tip_ids:
        chain = {}
        cur = int(tid)
        while cur != -1:
            chain[cur] = tree.node_depth[cur]
            cur = int(tree.parent[cur]) if tree.parent[cur] != -1 else -1
        ancestors.append(chain)
    D = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        di = tree.node_depth[tree.tip_ids[i]]
        for j in range(i + 1, n):
            dj = tree.node_depth[tree.tip_ids[j]]
            common = set(ancestors[i]) & set(ancestors[j])
            lca_depth = max(ancestors[i][c] for c in common)
            d = (di - lca_depth) + (dj - lca_depth)
            D[i, j] = D[j, i] = d
    return D


def evolve_jc69(tree: Tree, L: int, seed: int) -> np.ndarray:
    """Evolve sequences of length L along the tree under JC69 (rate=1,
    branch_len in expected substitutions/site). Returns [n_tips, L] array of
    bases in {0,1,2,3}, root random uniform.

    JC69 transition prob given branch length t (expected subs/site):
      P(same) = 1/4 + 3/4 * exp(-4t/3)
      P(diff, each of 3) = 1/4 - 1/4 * exp(-4t/3)
    """
    rng = np.random.default_rng(seed)
    n = tree.n_nodes
    seqs = np.zeros((n, L), dtype=np.int8)
    root_candidates = np.where(tree.parent == -1)[0]
    root = int(root_candidates[0])
    seqs[root] = rng.integers(0, 4, size=L)

    # process in an order where parent is always evolved before child:
    # sort nodes by node_depth (root=0 is smallest)
    order = np.argsort(tree.node_depth)
    for node in order:
        node = int(node)
        if node == root:
            continue
        p = int(tree.parent[node])
        t = float(tree.branch_len[node])
        p_same = 0.25 + 0.75 * np.exp(-4.0 * t / 3.0)
        p_diff_each = (1.0 - p_same) / 3.0
        # for each site, with prob p_same keep parent base, else uniform among other 3
        change = rng.random(L) >= p_same
        parent_bases = seqs[p]
        new_bases = parent_bases.copy()
        n_change = int(change.sum())
        if n_change > 0:
            # pick uniformly among the 3 other bases
            offset = rng.integers(1, 4, size=n_change)
            new_bases[change] = (parent_bases[change] + offset) % 4
        seqs[node] = new_bases
    return seqs[tree.tip_ids]


def evolve_infinite_sites(tree: Tree, L_effective_max: int, seed: int) -> np.ndarray:
    """Infinite-sites control: every substitution event hits a FRESH site,
    never reused, never reverted -- irreversible presence/absence. Because
    sites are never reused, a tip's mutation SET is exactly the multiset of
    mutation-count-increments accumulated along its root path; we don't need
    to materialize site identities at all. Represent each node's state as an
    integer INTERVAL [birth_id, next_id) into a global, monotonically
    increasing site counter: node inherits parent's interval boundaries plus
    its own new sites appended. Two tips share mutation s iff s < the mutation
    count at their LCA. This reduces the whole computation to per-node scalar
    counts (root-to-node cumulative new-site count) -- O(n_nodes), no sets.
    Returns tip pairwise symmetric-difference-based distance directly is done
    by the caller from these cumulative counts and the tree structure; here we
    return, for each tip, its own cumulative mutation count and, implicitly,
    the LCA structure is available via the tree itself (ancestors chain).
    """
    rng = np.random.default_rng(seed)
    n = tree.n_nodes
    root_candidates = np.where(tree.parent == -1)[0]
    root = int(root_candidates[0])
    # cumulative mutation COUNT from root to each node (integer valued;
    # deterministic given the branch's Poisson draw)
    cum_count = np.zeros(n, dtype=np.int64)
    order = np.argsort(tree.node_depth)
    for node in order:
        node = int(node)
        if node == root:
            continue
        p = int(tree.parent[node])
        t = float(tree.branch_len[node])
        n_new = rng.poisson(t * L_effective_max) if L_effective_max else rng.poisson(t)
        cum_count[node] = cum_count[p] + n_new
    return cum_count  # per-node; caller indexes tree.tip_ids and uses ancestor LCA counts


def infinite_sites_pairwise_distance(tree: Tree, cum_count: np.ndarray) -> np.ndarray:
    """Symmetric-difference distance between tips under the infinite-sites
    model, computed from cumulative counts + exact ancestor chains (no sets
    ever materialized). Two tips i,j: mutations unique to i = cum[i]-cum[lca],
    unique to j = cum[j]-cum[lca]; union = cum[i]+cum[j]-2*cum[lca]. Distance
    = symmetric-difference / union (Jaccard distance on mutation sets),
    which is exactly what infsites_distance() computed from the binary
    matrix, but derived in O(n^2) scalar ops instead of O(n^2 * n_sites).
    """
    n = tree.n_tips
    ancestors = []
    for tid in tree.tip_ids:
        chain = {}
        cur = int(tid)
        while cur != -1:
            chain[cur] = cum_count[cur]
            cur = int(tree.parent[cur]) if tree.parent[cur] != -1 else -1
        ancestors.append(chain)
    D = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        ci = cum_count[tree.tip_ids[i]]
        for j in range(i + 1, n):
            cj = cum_count[tree.tip_ids[j]]
            common = set(ancestors[i]) & set(ancestors[j])
            # LCA = deepest common ancestor = the one with MAX cumulative count
            # among common ancestors (counts increase monotonically root->tip)
            lca_count = max(ancestors[i][c] for c in common)
            # i's total mutation-site count = ci (all sites root->i, all
            # distinct); shared with j = lca_count (sites up to their LCA);
            # inclusion-exclusion: union = ci + cj - lca_count,
            # symmetric difference = (ci-lca_count)+(cj-lca_count) = ci+cj-2*lca_count
            union = ci + cj - lca_count
            sym_diff = ci + cj - 2 * lca_count
            D[i, j] = D[j, i] = (sym_diff / union) if union > 0 else 0.0
    return D


if __name__ == "__main__":
    t = yule_tree(16, seed=0)
    print("yule tree: n_tips", t.n_tips, "n_nodes", t.n_nodes)
    print("tip depths:", t.node_depth[t.tip_ids])
    print("ultrametric (all tip depths equal)?", np.allclose(t.node_depth[t.tip_ids], t.node_depth[t.tip_ids[0]]))
