"""PREREG15b scorer: T1-T4 as registered, as amended (Amendments 1-2), and the substantive reading of near-threshold cells.
q = 2 cells come from the first run (unaffected by the q >= 3 bug); every q >= 3 cell and every H = 3,000 cell from the rerun.
Reads the run outputs in ~/Documents/addressability-theory-2026-10-08/horizon-A; writes nothing."""
import json

D = "/Users/rohitfenn/Documents/addressability-theory-2026-10-08/horizon-A"
first = json.load(open(f"{D}/horizon_A_results.json"))
rerun = json.load(open(f"{D}/horizon_A2_results.json"))
cells = {}
for r in first:
    if r["q"] == 2:
        cells[(r["q"], r["d"], r["dlam2"], r["H"])] = r
for r in rerun:
    cells[(r["q"], r["d"], r["dlam2"], r["H"])] = r
SUB, SUP_STRICT, SUP_AMENDED = [0.80, 0.90, 0.95, 0.98], [1.02, 1.05, 1.10, 1.20, 1.40], [1.05, 1.10, 1.20, 1.40]


def verdict(q, d, x, H):
    r = cells.get((q, d, x, H))
    return None if r is None else r["verdict"]


def near(q, d, x):
    r = cells.get((q, d, x, 3000))
    if r is None:
        return "not run"
    tail = [m for h, m, _ in r["traj"] if h >= 2500]
    return f"H=3000 {r['verdict']}; m over levels 2500-3000 in [{min(tail):.4f}, {max(tail):.4f}]"


for q, d, H in [(2, 2, 500), (4, 2, 500), (3, 2, 500)]:
    sub = {x: verdict(q, d, x, H) for x in SUB}
    strict = {x: verdict(q, d, x, H) for x in SUP_STRICT}
    amended = {x: (verdict(q, d, x, 3000) if x in (1.02, 1.05) else verdict(q, d, x, H)) for x in SUP_AMENDED}
    kill = any(v == "RECONSTRUCTS" for v in sub.values())
    ok_sub = all(v == "FORGETS" for v in sub.values())
    ok_strict = all(v == "RECONSTRUCTS" for v in strict.values())
    ok_amended = all(v == "RECONSTRUCTS" for v in amended.values())
    print(f"\n(q={q}, d={d}) below the line: {sub}")
    print(f"   above, as first registered (H=500, from 1.02): {strict} -> {'PASS' if ok_strict else 'FAIL'}")
    print(f"   above, as amended (from 1.05; 1.02/1.05 at H=3000): {amended} -> {'PASS' if ok_amended else 'FAIL'}")
    print(f"   near-threshold substance: 1.02 {near(q, d, 1.02)}; 1.05 {near(q, d, 1.05)}")
    print(f"   subcritical half {'PASS' if ok_sub else 'FAIL'}; kill (reconstructs below the line) {'FIRES' if kill else 'does not fire'}")
print("\nT4 sensitivity (q = 8):")
for d in (2, 10, 30):
    row = {x: verdict(8, d, x, 300) for x in [0.80, 0.90, 0.95, 0.98, 1.00, 1.02, 1.05, 1.10, 1.20, 1.40]}
    below = [x for x in (0.80, 0.90, 0.95, 0.98) if row[x] == "RECONSTRUCTS"]
    print(f"   d={d}: {row}  -> reconstructs below the line at {below if below else 'none'}")
