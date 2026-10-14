"""PREREG19 scorer: B1 per (generator, D), B2 primary verdict, B3 discriminator, B4 reported."""
import json
import numpy as np

rows = [json.loads(l) for l in open("testB_cells.jsonl")]
Ls = [50_000, 100_000, 200_000, 400_000, 800_000]


def acc(gen, D, L):
    v = [r["acc_decided"] for r in rows if r["gen"] == gen and r["D"] == D and r["L"] == L]
    return float(np.mean(v)) if v else float("nan"), len(v)


verdicts = {}
print("B1: decided accuracy vs L (mean over seeds)")
print(f"{'gen':>5} {'D':>4} | " + " ".join(f"{L:>8d}" for L in Ls) + " |   Δ(800k−50k)  verdict   undecid(800k)  witness(800k)")
for gen in ["G", "H", "T"]:
    for D in [1.0, 2.0]:
        a = {L: acc(gen, D, L)[0] for L in Ls}
        delta = a[800_000] - a[50_000]
        v = "RECOVERS" if (delta >= 0.02 or a[800_000] >= 0.98) else ("FLOOR" if (delta < 0.005 and a[800_000] < 0.98) else "INDETERMINATE")
        verdicts[(gen, D)] = v
        und = np.mean([r["frac_undecidable"] for r in rows if r["gen"] == gen and r["D"] == D and r["L"] == 800_000] or [float("nan")])
        wit = np.mean([r["block_witness"] for r in rows if r["gen"] == gen and r["D"] == D and r["L"] == 800_000] or [float("nan")])
        print(f"{gen:>5} {D:>4} | " + " ".join(f"{a[L]:8.4f}" for L in Ls) + f" |   {delta:+.4f}     {v:13s} {und:.4f}        {wit:.1f}")
b2 = "DIAGNOSTIC SPECIFIC" if all(v == "RECOVERS" for v in verdicts.values()) else ("NOT SPECIFIC" if any(v == "FLOOR" for v in verdicts.values()) else "INCONCLUSIVE")
print(f"\nB2 primary verdict: {b2}")
# B3
def pmaj(gen, D):
    v = [r["p_major"] for r in rows if r["gen"] == gen and r["D"] == D and r["L"] == 800_000 and r.get("p_major") is not None]
    return (float(np.mean(v)), len(v)) if v else (None, 0)
pc, nc = pmaj("Cstar", 1.0)
print(f"\nB3 discriminator: C* mean p_major = {pc if pc is not None else 'n/a'} (n = {nc}); prediction ≤ 0.85")
floored = [(g, D) for (g, D), v in verdicts.items() if v == "FLOOR"]
ok_c = pc is not None and pc <= 0.85
ok_m = True
for g, D in floored:
    pm, n = pmaj(g, D)
    print(f"   floored {g} D={D}: mean p_major = {pm if pm is not None else 'n/a'} (n = {n}); prediction ≥ 0.95")
    ok_m &= (pm is not None and pm >= 0.95)
for g in ["G", "H", "T"]:
    for D in [1.0, 2.0]:
        if (g, D) not in floored:
            pm, n = pmaj(g, D)
            print(f"   (reported) {g} D={D}: mean p_major = {pm if pm is not None else 'n/a'} (n = {n})")
b3 = "DISCRIMINATOR WORKS" if (ok_c and ok_m) else "DISCRIMINATOR FAILS"
print(f"B3 verdict: {b3}{'  (misspecified half vacuous: nothing floored)' if not floored else ''}")
json.dump(dict(B1={f"{g}|{D}": v for (g, D), v in verdicts.items()}, B2=b2, B3=b3, p_major_Cstar=pc), open("testB_score.json", "w"), indent=1)
