"""PREREG23b step 1b: concatenate the 13 per-gene alignments in standard order, drop columns that are gaps or
ambiguous (- ? N .) in more than 50% of sequences, write work/concat.fa and work/concat_summary.json."""
import argparse, json
import numpy as np

GENES = ["ND1", "ND2", "COX1", "COX2", "ATP8", "ATP6", "COX3", "ND3", "ND4L", "ND4", "ND5", "ND6", "CYTB"]
BAD = set("-?N.")


def read_fasta(path):
    seqs, name, buf = {}, None, []
    for line in open(path):
        if line.startswith(">"):
            if name is not None:
                seqs[name] = "".join(buf)
            name = line[1:].split()[0]; buf = []
        else:
            buf.append(line.strip().upper())
    if name is not None:
        seqs[name] = "".join(buf)
    return seqs


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--scratch", required=True); a = ap.parse_args()
    S = a.scratch
    alns = {g: read_fasta(f"{S}/work/aln_{g}.fa") for g in GENES}
    names = sorted(set.intersection(*(set(v) for v in alns.values())))
    bounds, parts = {}, []
    pos = 0
    for g in GENES:
        L = len(next(iter(alns[g].values())))
        assert all(len(alns[g][n]) == L for n in names), g
        bounds[g] = (pos, pos + L); pos += L
    arr = np.array([list("".join(alns[g][n] for g in GENES)) for n in names])
    bad = np.isin(arr, list(BAD))
    keep = np.where(bad.mean(axis=0) <= 0.5)[0]
    sub = arr[:, keep]
    with open(f"{S}/work/concat.fa", "w") as out:
        for n, row in zip(names, sub):
            out.write(f">{n}\n{''.join(row)}\n")
    gene_of_col = np.zeros(pos, dtype=np.int16)
    for i, g in enumerate(GENES):
        gene_of_col[bounds[g][0]:bounds[g][1]] = i
    summary = dict(taxa=len(names), raw_columns=int(pos), kept_columns=int(len(keep)), gene_bounds=bounds,
                   kept_gene_of_column=gene_of_col[keep].tolist())
    json.dump(summary, open(f"{S}/work/concat_summary.json", "w"))
    print(json.dumps({k: v for k, v in summary.items() if k != "kept_gene_of_column"}), flush=True)


if __name__ == "__main__":
    main()
