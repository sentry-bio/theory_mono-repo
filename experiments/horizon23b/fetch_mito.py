"""PREREG23b step 0: download RefSeq mitochondrion release, extract the 13 protein-coding genes of complete
vertebrate mitogenomes, subsample 1,500 stratified by class (seed 23). Runs inside /fast/scratch_h23b.

Usage: venv/bin/python fetch_mito.py --scratch /fast/scratch_h23b [--skip-download]
Writes data/genes/<GENE>.fa, data/taxonomy.tsv, data/fetch_summary.json
"""
import argparse, gzip, hashlib, json, os, random, statistics, sys, time, urllib.request
from collections import defaultdict
from Bio import SeqIO

URL = "https://ftp.ncbi.nlm.nih.gov/refseq/release/mitochondrion/mitochondrion.1.genomic.gbff.gz"
GENES = ["ND1", "ND2", "COX1", "COX2", "ATP8", "ATP6", "COX3", "ND3", "ND4L", "ND4", "ND5", "ND6", "CYTB"]
SYN = {"COI": "COX1", "CO1": "COX1", "COXI": "COX1", "COII": "COX2", "CO2": "COX2", "COXII": "COX2", "COIII": "COX3",
       "CO3": "COX3", "COXIII": "COX3", "ATPASE6": "ATP6", "ATPASE8": "ATP8", "COB": "CYTB", "CYB": "CYTB",
       "NADH1": "ND1", "NADH2": "ND2", "NADH3": "ND3", "NADH4": "ND4", "NADH4L": "ND4L", "NADH5": "ND5", "NADH6": "ND6"}
CLASSES = ["Mammalia", "Aves", "Lepidosauria", "Testudines", "Crocodylia", "Amphibia", "Actinopteri",
           "Chondrichthyes", "Cladistia", "Dipnomorpha", "Coelacanthimorpha", "Hyperoartia", "Myxini"]
SEED, T, CAP = 23, 1500, 300


def norm_gene(q):
    for key in ("gene", "product"):
        for v in q.get(key, []):
            g = v.upper().replace(" ", "").replace("-", "").replace("_", "")
            g = g.replace("CYTOCHROMEB", "CYTB").replace("CYTOCHROMECOXIDASESUBUNIT", "COX")
            g = g.replace("NADHDEHYDROGENASESUBUNIT", "ND").replace("ATPSYNTHASEF0SUBUNIT", "ATP")
            g = g.replace("ATPSYNTHASESUBUNIT", "ATP").replace("NADHDEHYDROGENASE", "ND")
            g = SYN.get(g, g)
            if g in GENES:
                return g
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True); ap.add_argument("--skip-download", action="store_true")
    a = ap.parse_args()
    S = a.scratch; D = f"{S}/data"; os.makedirs(f"{D}/genes", exist_ok=True)
    gz = f"{D}/mitochondrion.1.genomic.gbff.gz"
    t0 = time.time()
    if not a.skip_download:
        urllib.request.urlretrieve(URL, gz)
    h = hashlib.md5(open(gz, "rb").read()).hexdigest()
    print(f"downloaded {os.path.getsize(gz)} bytes md5 {h} ({time.time()-t0:.0f}s)", flush=True)
    recs = {}; tax = {}; n_all = n_vert = n_complete = 0
    with gzip.open(gz, "rt") as f:
        for rec in SeqIO.parse(f, "genbank"):
            n_all += 1
            lin = rec.annotations.get("taxonomy", [])
            if "Vertebrata" not in lin:
                continue
            n_vert += 1
            if "complete genome" not in rec.description.lower():
                continue
            n_complete += 1
            genes = {}
            for ft in rec.features:
                if ft.type != "CDS":
                    continue
                g = norm_gene(ft.qualifiers)
                if g and g not in genes:
                    try:
                        genes[g] = str(ft.extract(rec.seq)).upper()
                    except Exception:
                        pass
            if all(g in genes for g in GENES):
                recs[rec.id] = genes
                cls = next((c for c in CLASSES if c in lin), "other")
                tax[rec.id] = dict(organism=rec.annotations.get("organism", ""), cls=cls, lineage=";".join(lin))
            if n_all % 5000 == 0:
                print(f"  parsed {n_all} records, kept {len(recs)} ({time.time()-t0:.0f}s)", flush=True)
    print(f"records {n_all}, vertebrate {n_vert}, complete {n_complete}, with all 13 genes {len(recs)}", flush=True)
    # length filter: a gene shorter than 70% of its median length drops the record
    med = {g: statistics.median(len(r[g]) for r in recs.values()) for g in GENES}
    keep = {k: v for k, v in recs.items() if all(len(v[g]) >= 0.7 * med[g] for g in GENES)}
    print(f"after length filter {len(keep)}", flush=True)
    # stratified subsample: cap per class, then fill to T proportionally (seed 23)
    rng = random.Random(SEED)
    byc = defaultdict(list)
    for k in sorted(keep):
        byc[tax[k]["cls"]].append(k)
    chosen = []
    for c in sorted(byc):
        lst = byc[c][:]; rng.shuffle(lst); chosen.extend(lst[:CAP])
    if len(chosen) > T:
        rng.shuffle(chosen); chosen = sorted(chosen[:T])
    else:
        chosen = sorted(chosen)
    counts = defaultdict(int)
    for k in chosen:
        counts[tax[k]["cls"]] += 1
    for g in GENES:
        with open(f"{D}/genes/{g}.fa", "w") as out:
            for k in chosen:
                out.write(f">{k}\n{keep[k][g]}\n")
    with open(f"{D}/taxonomy.tsv", "w") as out:
        out.write("accession\tclass\torganism\tlineage\n")
        for k in chosen:
            t = tax[k]; out.write(f"{k}\t{t['cls']}\t{t['organism']}\t{t['lineage']}\n")
    summary = dict(url=URL, md5=h, bytes=os.path.getsize(gz), records=n_all, vertebrate=n_vert, complete=n_complete,
                   with_13_genes=len(recs), after_length_filter=len(keep), chosen=len(chosen), seed=SEED, cap=CAP,
                   class_counts=dict(sorted(counts.items())), median_gene_len=med, elapsed_s=round(time.time() - t0))
    json.dump(summary, open(f"{D}/fetch_summary.json", "w"), indent=1)
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
