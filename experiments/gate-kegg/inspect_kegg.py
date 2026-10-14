"""Inspect the KEGG profile matrix and the reference manifest (no statistic of the gate is computed)."""
import collections, csv, re
import numpy as np

z = np.load("kegg_profiles_868.npz", allow_pickle=True)
print("npz keys:", list(z.keys()))
acc, P = z["accessions"], z["profiles"]
print("profiles:", P.shape, P.dtype, "nonzero rows:", int((P.sum(1) > 0).sum()),
      "row-sum quantiles 5/50/95:", np.percentile(P.sum(1), [5, 50, 95]).round(1))
print("accession examples:", list(acc[:3]))
rows = list(csv.DictReader(open("reference_manifest.csv")))
print("manifest rows:", len(rows), "columns:", list(rows[0].keys())[:16])


def num(a):
    m = re.search(r"GC[AF]_(\d+)", str(a))
    return m.group(1) if m else None


tax = {num(r["accession"]): r for r in rows if num(r["accession"])}
hit = [a for a in acc if num(a) in tax]
print("profiles with taxonomy:", len(hit), "of", len(acc))
print("domains:", dict(collections.Counter(tax[num(a)]["domain"] for a in hit)))
print("phyla:", len({tax[num(a)]["phylum"] for a in hit}), " families:", len({tax[num(a)]["family"] for a in hit}),
      " genera:", len({tax[num(a)]["genus"] for a in hit}))
