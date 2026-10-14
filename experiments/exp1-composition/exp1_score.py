"""PREREG17 scorer: C1-C5 as registered. Reads exp1_comp_*.jsonl, closed_form.py, p15_var_site_over_P.json. Writes exp1_score.json."""
import glob, json, math, importlib.util
spec = importlib.util.spec_from_file_location("cf", "closed_form.py"); cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)
P15 = json.load(open("p15_var_site_over_P.json"))
RULE = {(0.8, 2), (1.0, 2), (1.0, 3), (1.0, 4), (1.25, 2), (1.25, 3), (1.25, 4), (1.25, 6), (1.5, 2), (1.5, 3), (1.5, 4), (1.5, 6)}
cells = {}
for fn in sorted(glob.glob("exp1_comp_*.jsonl")):
    for r in map(json.loads, open(fn)):
        cells[(r["x"], r["h"], r["L"])] = r
rows = []
for (x, h, L), r in sorted(cells.items()):
    E1, P = cf.stats(cf.H1, h, x); E4, V4 = cf.stats(cf.H, h, x)
    rows.append(dict(x=x, h=h, L=L, R=r["R"], rule=(x, h) in RULE,
                     z4_pred=E4 / math.sqrt(V4), z4_meas=r["m4_mean"] / r["m4_sd"], se=1 / math.sqrt(r["R"]),
                     z1_pred=E1 / math.sqrt(P), z1_meas=r["m1_mean"] / r["m1_sd"],
                     Leff1_meas=(L * r["site_sd"] / r["m1_sd"]) ** 2, Leff1_pred_P15=P15.get(f"{x}|{h}"),
                     distinct=r["frac_reps_all_leaves_distinct_4mer"]))
by = {(q["x"], q["h"], q["L"]): q for q in rows}
# C1
rule_cells = [q for q in rows if q["rule"]]
dev = [abs(q["z4_meas"] - q["z4_pred"]) / q["se"] for q in rule_cells]
c1 = sum(d <= 3 for d in dev) >= 22 and all(d <= 5 for d in dev)
# C2
pairs = sorted({(q["x"], q["h"]) for q in rule_cells})
r4 = {p: by[(p[0], p[1], 40000)]["z4_meas"] / by[(p[0], p[1], 5000)]["z4_meas"] for p in pairs}
r1 = {p: by[(p[0], p[1], 40000)]["Leff1_meas"] / by[(p[0], p[1], 5000)]["Leff1_meas"] for p in pairs}
c2 = sum(0.8 <= v <= 1.25 for v in r4.values()) >= 10 and sum(0.8 <= v <= 1.25 for v in r1.values()) >= 10
# C3: measured z4/z1 decreasing in h at L = 40k (one inversion < 2 SE allowed)
def decreasing(x, hs):
    vals = [(h, by[(x, h, 40000)]) for h in hs]
    inv = 0
    for (h1, a), (h2, b) in zip(vals, vals[1:]):
        ra, rb = a["z4_meas"] / a["z1_meas"], b["z4_meas"] / b["z1_meas"]
        if rb >= ra:
            inv += 1
            se_ratio = ra * math.sqrt((a["se"] / a["z4_meas"]) ** 2 + (a["se"] / a["z1_meas"]) ** 2)
            if rb - ra >= 2 * se_ratio:
                return False
    return inv <= 1
c3 = decreasing(1.25, [2, 3, 4, 6]) and decreasing(1.5, [2, 3, 4, 6]) and decreasing(1.0, [2, 3, 4])
# C4
c4_hits = {p: abs(by[(p[0], p[1], 40000)]["Leff1_meas"] / P15[f"{p[0]}|{p[1]}"] - 1) <= 0.20 for p in pairs}
c4 = sum(c4_hits.values()) >= 10 and all(c4_hits[p] for p in pairs if p[0] == 1.5)
print(f"{'x':>5} {'h':>2} {'L':>6} {'R':>5} rule | {'z4 pred':>8} {'meas':>8} {'dev/SE':>6} | {'z1 pred':>7} {'meas':>7} | {'Leff1':>6} {'P15':>5} | distinct")
for q in rows:
    print(f"{q['x']:>5} {q['h']:>2} {q['L']:>6} {q['R']:>5} {'*' if q['rule'] else ' '}    | {q['z4_pred']:8.4f} {q['z4_meas']:8.4f} {abs(q['z4_meas']-q['z4_pred'])/q['se']:6.2f} | "
          f"{q['z1_pred']:7.4f} {q['z1_meas']:7.4f} | {q['Leff1_meas']:6.2f} {q['Leff1_pred_P15'] if q['Leff1_pred_P15'] else float('nan'):5.2f} | {q['distinct']:.3f}")
print(f"\nC1 4-mer closed form: {sum(d <= 3 for d in dev)}/{len(dev)} within 3 SE, max {max(dev):.2f} SE -> {'PASS' if c1 else 'FAIL'}")
print(f"C2 length independence: z4 ratios {sum(0.8 <= v <= 1.25 for v in r4.values())}/12 in range; Leff1 ratios {sum(0.8 <= v <= 1.25 for v in r1.values())}/12 -> {'PASS' if c2 else 'FAIL'}")
print(f"C3 decay toward letter counts (x = 1.0, 1.25, 1.5): {'PASS' if c3 else 'FAIL'}")
print(f"C4 letter-count level = PREREG15's Var_site/P: {sum(c4_hits.values())}/12 within 20% (x = 1.5 all: {all(c4_hits[p] for p in pairs if p[0] == 1.5)}) -> {'PASS' if c4 else 'FAIL'}")
print(f"C5 identity kept (reported): min fraction distinct = {min(q['distinct'] for q in rows):.3f}")
verdict = "COMPOSITION WORTH PREDICTED" if (c1 and c2 and c3 and c4) else "NOT PREDICTED"
print(f"\nPREREG17 verdict: {verdict}")
json.dump(dict(rows=rows, C1=c1, C2=c2, C3=c3, C4=c4, z4_ratio_40k_5k={str(k): v for k, v in r4.items()}, Leff1_ratio={str(k): v for k, v in r1.items()},
               C4_hits={str(k): v for k, v in c4_hits.items()}, verdict=verdict), open("exp1_score.json", "w"), indent=1)
