"""Join the base map v1.0 catalogue to the GTDB r220 trees; build LCA machinery; audit labels."""
import gzip
import os
import re

import numpy as np

A = os.path.dirname(os.path.abspath(__file__))


def core(acc):
    m = re.search(r"GC[AF]_(\d{9})", acc)
    return m.group(1) if m else None


def parse_newick(path):
    s = open(path).read().strip().rstrip(";")
    parent, blen, name = [-1], [0.0], [""]
    stack, cur, i, n = [], 0, 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "(":
            parent.append(cur); blen.append(0.0); name.append("")
            stack.append(cur); cur = len(parent) - 1; i += 1
        elif ch == ",":
            cur = stack[-1]
            parent.append(cur); blen.append(0.0); name.append("")
            cur = len(parent) - 1; i += 1
        elif ch == ")":
            cur = stack.pop(); i += 1
        else:
            j = i
            if ch == "'":
                j = s.index("'", i + 1) + 1
                label = s[i + 1:j - 1]
            else:
                while j < n and s[j] not in ",():":
                    j += 1
                label = s[i:j]
            i = j
            if label and not name[cur]:
                name[cur] = label
            if i < n and s[i] == ":":
                j = i + 1
                while j < n and s[j] not in ",()":
                    j += 1
                blen[cur] = float(s[i + 1:j]); i = j
    # the first node pushed at "(" became the root's child chain; node 0 is a dummy root
    return np.array(parent), np.array(blen), name


def build(path):
    parent, blen, name = parse_newick(path)
    N = len(parent)
    children = [[] for _ in range(N)]
    for v in range(1, N):
        children[parent[v]].append(v)
    is_leaf = np.array([len(c) == 0 for c in children])
    depth = np.zeros(N)
    order = [0]
    euler, first = [], np.full(N, -1)
    edepth = []
    lvl = np.zeros(N, dtype=np.int32)
    st = [(0, 0)]
    while st:
        v, k = st.pop()
        if k == 0:
            first[v] = len(euler)
        euler.append(v); edepth.append(lvl[v])
        if k < len(children[v]):
            st.append((v, k + 1))
            c = children[v][k]
            depth[c] = depth[v] + blen[c]; lvl[c] = lvl[v] + 1
            st.append((c, 0))
    euler = np.array(euler); edepth = np.array(edepth)
    # sparse table on edepth for RMQ
    K = int(np.log2(len(euler))) + 1
    sp = [np.arange(len(euler))]
    for k in range(1, K):
        prev = sp[-1]; h = 1 << (k - 1)
        a, b = prev[:-h], prev[h:]
        sp.append(np.where(edepth[a] <= edepth[b], a, b))
    return dict(parent=parent, blen=blen, name=name, is_leaf=is_leaf, depth=depth,
                euler=euler, edepth=edepth, first=first, sp=sp)


def lca(T, u, v):
    a, b = np.minimum(T["first"][u], T["first"][v]), np.maximum(T["first"][u], T["first"][v])
    k = np.floor(np.log2(b - a + 1)).astype(int)
    out = np.empty(len(a), dtype=np.int64)
    for kk in np.unique(k):
        m = k == kk
        x, y = T["sp"][kk][a[m]], T["sp"][kk][b[m] - (1 << kk) + 1]
        out[m] = T["euler"][np.where(T["edepth"][x] <= T["edepth"][y], x, y)]
    return out


def patristic(T, u, v):
    return T["depth"][u] + T["depth"][v] - 2 * T["depth"][lca(T, u, v)]


def taxonomy():
    tax = {}
    for f in ("bac120_taxonomy_r220.tsv.gz", "ar53_taxonomy_r220.tsv.gz"):
        for line in gzip.open(f"{A}/{f}", "rt"):
            acc, t = line.rstrip("\n").split("\t")
            tax[core(acc)] = dict(x.split("__", 1) for x in t.split(";"))
    return tax


if __name__ == "__main__":
    ref = [l.rstrip("\n").split("\t") for l in open(f"{A}/reference.tsv")]
    hdr, ref = ref[0], ref[1:]
    Z = np.load(f"{A}/catalogue_coordinates.npz")
    zacc = Z["accession"]
    assert all(core(a) == core(r[0]) for a, r in zip(zacc[:1000], ref[:1000])), "row order differs"
    tax = taxonomy()
    out = {}
    for dom, f in (("bac", "bac120_r220.tree"), ("ar", "ar53_r220.tree")):
        T = build(f"{A}/{f}")
        leaf_core = {core(T["name"][v]): v for v in np.flatnonzero(T["is_leaf"])}
        rows, leaves = [], []
        for i, a in enumerate(zacc):
            c = core(a)
            if c in leaf_core:
                rows.append(i); leaves.append(leaf_core[c])
        out[dom] = (np.array(rows), np.array(leaves), T)
        print(f"{f}: {T['is_leaf'].sum():,} leaves; {len(rows):,} catalogue genomes on the tree; max root depth {T['depth'].max():.2f}")
    # label audit: catalogue genus/family vs GTDB r220 for genomes GTDB knows
    known = mism_g = mism_f = sp_g = 0
    bad = []
    for r in ref:
        t = tax.get(core(r[0]))
        g_sp = r[4].split(" ")[0] if r[4] else ""
        if g_sp and r[3] and g_sp.split("_")[0] != r[3].split("_")[0]:
            sp_g += 1
            if len(bad) < 8: bad.append((r[0], r[2], r[3], r[4]))
        if t is None:
            continue
        known += 1
        mism_g += t["g"] != r[3]
        mism_f += t["f"] != r[2]
    print(f"\nlabel audit: {known:,} catalogue genomes found in GTDB r220 taxonomy; "
          f"genus differs from r220: {mism_g:,}; family differs: {mism_f:,}")
    print(f"rows whose species name disagrees with their own genus column: {sp_g:,}; e.g.")
    for b in bad: print("   ", b)
    doms = {}
    for r in ref: doms[r[1]] = doms.get(r[1], 0) + 1
    print("domains:", doms)
