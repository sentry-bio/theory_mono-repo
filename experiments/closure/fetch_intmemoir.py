"""Re-fetch the processed intMEMOIR colonies (characters + true trees) from the public repository.
Source: github.com/raphael-group/intmemoir-processed-data (no licence file; analysed in place, not redistributed)."""
import json, os, time, urllib.request

API = "https://api.github.com/repos/raphael-group/intmemoir-processed-data/git/trees/main?recursive=1"
RAW = "https://raw.githubusercontent.com/raphael-group/intmemoir-processed-data/main/"
os.makedirs("intmemoir", exist_ok=True)
tree = json.load(urllib.request.urlopen(urllib.request.Request(API, headers={"User-Agent": "closure-test"})))["tree"]
paths = [t["path"] for t in tree if t["type"] == "blob" and t["path"].startswith("processed_intmemoir_data/")]
print("files in repo:", len(paths), "examples:", paths[:4])
n = 0
for p in paths:
    out = os.path.join("intmemoir", p.split("processed_intmemoir_data/", 1)[1])
    os.makedirs(os.path.dirname(out) or "intmemoir", exist_ok=True)
    if os.path.exists(out):
        continue
    try:
        urllib.request.urlretrieve(RAW + p, out); n += 1
    except Exception as e:
        print("miss", p, e)
    if n % 60 == 0 and n:
        time.sleep(1)
print("fetched", n)
cols = sorted(d for d in os.listdir("intmemoir") if os.path.isdir(os.path.join("intmemoir", d)))
print("colonies:", len(cols), "with tree:", sum(os.path.exists(os.path.join("intmemoir", c, "true_tree.nwk")) for c in cols))
