"""List the latest IQ-TREE 2 release assets (read-only query of the public release API)."""
import json, urllib.request
with urllib.request.urlopen("https://api.github.com/repos/iqtree/iqtree2/releases/latest", timeout=30) as r:
    d = json.load(r)
print(d["tag_name"])
for a in d["assets"]:
    print(a["name"], a["size"], a["browser_download_url"])
