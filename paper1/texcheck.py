"""Static checks for a LaTeX file: environment balance, unresolved \\ref and \\cite, brace balance."""
import re
import sys
from collections import Counter

for f in sys.argv[1:]:
    t = open(f).read()
    cb, ce = Counter(re.findall(r"\\begin\{(\w+)\}", t)), Counter(re.findall(r"\\end\{(\w+)\}", t))
    bad = {k: (cb[k], ce[k]) for k in set(cb) | set(ce) if cb[k] != ce[k]}
    labels = set(re.findall(r"\\label\{([^}]+)\}", t))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", t))
    cites = {c.strip() for s in re.findall(r"\\cite\{([^}]+)\}", t) for c in s.split(",")}
    bibs = set(re.findall(r"\\bibitem\{([^}]+)\}", t))
    print(f, "| lines", t.count("\n"), "| env mismatch", bad, "| missing refs", refs - labels,
          "| missing bibs", cites - bibs, "| unused bibs", len(bibs - cites), "| brace balance", t.count("{") - t.count("}"))
