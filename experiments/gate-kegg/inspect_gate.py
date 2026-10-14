"""Post-run inspection of gate_results.json (read-only): per-centre fits, radius windows, and the S1 sample check."""
import json, csv, re, collections
import numpy as np

r = json.load(open("gate_results.json"))
print("K1", r["K1"])
for s in ("S1", "S2"):
    d = r["samples"][s]
    print(f"\n== {s}: n={d['n']} dim={d['dim']} delta_ratio={d['delta_ratio']:.3f} verdict={d['verdict']}")
    for lab in ("data", "null"):
        rows = [x for x in d[lab] if x.get("usable")]
        print(f"-- {lab}: keys {sorted(rows[0].keys())}")
        for x in rows:
            flat = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in x.items()
                    if not isinstance(v, (list, dict))}
            print("   ", flat)

z = np.load("kegg_profiles_868.npz", allow_pickle=True)
acc = z["accessions"]
def num(a):
    m = re.search(r"GC[AF]_(\d+)", str(a)); return m.group(1) if m else None
tax = {}
with open("reference_manifest.csv") as f:
    for row in csv.DictReader(f):
        tax[num(row["accession"])] = row
cnt = collections.Counter(tax[num(a)]["phylum"] for a in acc if num(a) in tax)
print("\nphyla", len(cnt), "stratified n (<=120/phylum) =", sum(min(c, 120) for c in cnt.values()))
print("phyla with >=120:", sum(c >= 120 for c in cnt.values()), " smallest:", cnt.most_common()[-5:])
dom = collections.Counter(tax[num(a)]["domain"] for a in acc if num(a) in tax)
print("domains", dom)
