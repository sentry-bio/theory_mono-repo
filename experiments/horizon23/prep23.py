"""PREREG23 step 1–2 prep: parse the GTDB tree, subsample taxa, prune, subset the alignment.

Usage: python3 -I prep23.py --tree data/bac120.tree.gz --msa data/bac120_msa_reps.faa.gz --T 1500 --seed 23 --out work
Writes: work/pruned.nwk, work/sub.faa (IQ-TREE input), work/sub_cols.json (kept columns), work/prep_summary.json
"""
import argparse, gzip, json, random, re, sys, time
import numpy as np

# ------------------------------------------------------------------ Newick

class Node:
    __slots__ = ("name", "length", "children", "parent")
    def __init__(self, name="", length=0.0):
        self.name, self.length, self.children, self.parent = name, length, [], None

def parse_newick(s):
    """Minimal robust Newick parser: quoted labels, internal labels, branch lengths, comments stripped."""
    s = re.sub(r"\[[^\]]*\]", "", s).strip()
    if s.endswith(";"):
        s = s[:-1]
    i, n = 0, len(s)
    root = Node()
    stack = [root]
    cur = root
    def read_label(i):
        if i < n and s[i] == "'":
            j = s.index("'", i + 1)
            while j + 1 < n and s[j + 1] == "'":
                j = s.index("'", j + 2)
            return s[i + 1:j].replace("''", "'"), j + 1
        j = i
        while j < n and s[j] not in ",:();":
            j += 1
        return s[i:j].strip(), j
    while i < n:
        c = s[i]
        if c == "(":
            child = Node(); child.parent = cur; cur.children.append(child)
            stack.append(cur); cur = child; i += 1
        elif c == ",":
            cur = stack[-1]
            child = Node(); child.parent = cur; cur.children.append(child); cur = child; i += 1
        elif c == ")":
            cur = stack.pop(); i += 1
            label, i = read_label(i)
            cur.name = label
        elif c == ":":
            i += 1
            j = i
            while j < n and s[j] not in ",();":
                j += 1
            cur.length = float(s[i:j]); i = j
        elif c in " \n\t\r":
            i += 1
        else:
            label, i = read_label(i)
            cur.name = label
    return root

def tips(node):
    out = []
    st = [node]
    while st:
        x = st.pop()
        if x.children:
            st.extend(x.children)
        else:
            out.append(x)
    return out

def prune_to(root, keep):
    """Keep only tips in `keep`; drop empty subtrees; collapse unary nodes (lengths summed)."""
    def rec(node):
        if not node.children:
            return node if node.name in keep else None
        new = [c for c in (rec(ch) for ch in node.children) if c is not None]
        if not new:
            return None
        if len(new) == 1:
            child = new[0]
            child.length += node.length
            child.parent = node.parent
            return child
        node.children = new
        for c in new:
            c.parent = node
        return node
    r = rec(root)
    # root may have become unary-collapsed child; ensure a proper root with >=2 children
    while r is not None and len(r.children) == 1:
        c = r.children[0]; c.length += r.length; c.parent = None; r = c
    return r

def to_newick(node):
    def rec(x):
        if x.children:  # internal labels (GTDB support/taxonomy strings) are dropped: IQ-TREE rejects them
            inner = ",".join(rec(c) for c in x.children)
            return f"({inner}):{x.length:.10g}"
        return f"{quote(x.name)}:{x.length:.10g}"
    def quote(name):
        if name == "":
            return ""
        if re.search(r"[ ,:;()'\[\]]", name):
            return "'" + name.replace("'", "''") + "'"
        return name
    return rec(node) + ";"

# ------------------------------------------------------------------ FASTA

def read_fasta_subset(path, want):
    seqs = {}
    opener = gzip.open if path.endswith(".gz") else open
    name, buf, keep = None, [], False
    with opener(path, "rt") as f:
        for line in f:
            if line.startswith(">"):
                if keep and name is not None:
                    seqs[name] = "".join(buf)
                name = line[1:].split()[0]
                keep = name in want
                buf = []
            elif keep:
                buf.append(line.strip())
        if keep and name is not None:
            seqs[name] = "".join(buf)
    return seqs

def fasta_names(path):
    names = []
    opener = gzip.open if path.endswith(".gz") else open
    with opener(path, "rt") as f:
        for line in f:
            if line.startswith(">"):
                names.append(line[1:].split()[0])
    return names

# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True); ap.add_argument("--msa", required=True)
    ap.add_argument("--T", type=int, default=1500); ap.add_argument("--seed", type=int, default=23)
    ap.add_argument("--out", default="work")
    a = ap.parse_args()
    t0 = time.time()
    opener = gzip.open if a.tree.endswith(".gz") else open
    with opener(a.tree, "rt") as f:
        root = parse_newick(f.read())
    tree_tips = [t.name for t in tips(root)]
    msa_names = set(fasta_names(a.msa))
    common = sorted(set(tree_tips) & msa_names)
    print(f"tree tips {len(tree_tips)}, msa seqs {len(msa_names)}, common {len(common)}", flush=True)
    rng = random.Random(a.seed)
    chosen = sorted(rng.sample(common, a.T))
    pruned = prune_to(root, set(chosen))
    ptips = [t.name for t in tips(pruned)]
    assert sorted(ptips) == chosen, "prune mismatch"
    seqs = read_fasta_subset(a.msa, set(chosen))
    L0 = len(next(iter(seqs.values())))
    assert all(len(s) == L0 for s in seqs.values()), "ragged alignment"
    arr = np.array([list(seqs[n]) for n in chosen])
    bad = np.isin(arr, list("-?X.*"))
    keep_cols = np.where(bad.mean(axis=0) <= 0.5)[0]
    sub = arr[:, keep_cols]
    with open(f"{a.out}/pruned.nwk", "w") as f:
        f.write(to_newick(pruned) + "\n")
    with open(f"{a.out}/sub.faa", "w") as f:
        for n, row in zip(chosen, sub):
            f.write(f">{n}\n{''.join(row)}\n")
    json.dump({"kept_columns": keep_cols.tolist()}, open(f"{a.out}/sub_cols.json", "w"))
    summary = {"tree_tips": len(tree_tips), "msa_seqs": len(msa_names), "common": len(common), "T": a.T,
               "seed": a.seed, "L0": int(L0), "L_max": int(len(keep_cols)),
               "internal_nodes_pruned": sum(1 for _ in iter_internal(pruned)),
               "elapsed_s": round(time.time() - t0, 1)}
    json.dump(summary, open(f"{a.out}/prep_summary.json", "w"), indent=1)
    print(json.dumps(summary), flush=True)

def iter_internal(node):
    st = [node]
    while st:
        x = st.pop()
        if x.children:
            yield x
            st.extend(x.children)

if __name__ == "__main__":
    main()
