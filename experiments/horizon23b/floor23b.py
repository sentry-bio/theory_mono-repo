"""PREREG23b post-hoc reading (15 October 2026, not registered): where the full-length floor sits.
Does the internal edge covary with depth, and what characterises the quartets a four-point reader never recovers?
Reads the S2 secondary analysis (256 quartets, 40 subsets, 200 predicted replicates). Usage: python3 floor23b.py ."""
import json, sys, numpy as np
D = sys.argv[1] if len(sys.argv) > 1 else '.'
q = json.load(open(f'{D}/work/quartets_S2.json'))['quartets']
r = json.load(open(f'{D}/work/reads_S2.json')); p = json.load(open(f'{D}/work/pred_S2.json'))
ns = r['subsets']; reps = p['reps']
rq = r['quartets']; pq = {round(x['t'], 9): x for x in p['quartets']}
BINS = np.logspace(np.log10(0.05), np.log10(3.0), 9)
assert all(abs(a['t'] - b['t']) < 1e-9 for a, b in zip(q, rq))
t = np.array([x['t'] for x in q]); tau = np.array([x['tau'] for x in q])
tips = np.array([x['branches'][:4] for x in q])
F = {k: np.array([x['full'][k] for x in rq]) for k in ['U', 'W', 'S', 'U_RY', 'W_RY']}
P = {k: np.array([pq[round(x['t'], 9)]['full'][k] for x in q]) / reps for k in ['U', 'W', 'U_RY', 'W_RY']}
print("tau quantiles 10/25/50/75/90:", np.round(np.quantile(tau, [.1, .25, .5, .75, .9]), 4))
print("corr(t,tau)=%.3f  corr(log t,log tau)=%.3f  corr(t, tau/t)=%.3f" % (
    np.corrcoef(t, tau)[0, 1], np.corrcoef(np.log(t), np.log(tau))[0, 1], np.corrcoef(t, tau / t)[0, 1]))
b = np.searchsorted(BINS, t, side='right') - 1
print("bin  n   t_mean  tau_mean  tau/t   fullU predU  fullW predW  U_RY  W_RY predWRY")
for k in sorted(set(b)):
    m = b == k
    print(f"{k:3d} {m.sum():3d}  {t[m].mean():.3f}  {tau[m].mean():.4f}  {(tau[m]/t[m]).mean():.3f}   "
          f"{F['U'][m].mean():.3f} {P['U'][m].mean():.3f}  {F['W'][m].mean():.3f} {P['W'][m].mean():.3f}  "
          f"{F['U_RY'][m].mean():.3f} {F['W_RY'][m].mean():.3f} {P['W_RY'][m].mean():.3f}")
unrec = F['U'] == 0
print("\nunrecovered at full length (U):", int(unrec.sum()), "of", len(q))
for lab, m in [("recovered", ~unrec), ("unrecovered", unrec)]:
    print(f"  {lab:12s} median t {np.median(t[m]):.3f}  median tau {np.median(tau[m]):.4f}  median tau/t {np.median(tau[m]/t[m]):.3f}  "
          f"tip max/min {np.median(tips[m].max(1)/tips[m].min(1)):.2f}  predU {P['U'][m].mean():.3f}")
print("U fails & W recovers:", int(((F['U'] == 0) & (F['W'] == 1)).sum()),
      "| W fails & U recovers:", int(((F['W'] == 0) & (F['U'] == 1)).sum()),
      "| both fail:", int(((F['U'] == 0) & (F['W'] == 0)).sum()),
      "| W_RY fails:", int((F['W_RY'] == 0).sum()),
      "| all four fail:", int(((F['U'] == 0) & (F['W'] == 0) & (F['U_RY'] == 0) & (F['W_RY'] == 0)).sum()))
print("quartets the model itself expects to fail (predU<0.5):", int((P['U'] < 0.5).sum()),
      "of which unrecovered:", int(((P['U'] < 0.5) & unrec).sum()))
print("\nfull-length shortfall by reader (pooled):")
for k in ['U', 'W', 'U_RY', 'W_RY']:
    print(f"  {k:5s} pred {P[k].mean():.3f} obs {F[k].mean():.3f} shortfall {P[k].mean()-F[k].mean():.3f}")
print("\nfull-length shortfall by tertile of internal edge length:")
qt = np.quantile(tau, [1/3, 2/3])
for lo, hi, lab in [(0, qt[0], 'short'), (qt[0], qt[1], 'mid'), (qt[1], 9, 'long')]:
    m = (tau >= lo) & (tau < hi)
    cells = "  ".join(f"{k} {P[k][m].mean()-F[k][m].mean():.3f}" for k in ['U', 'W', 'U_RY', 'W_RY'])
    tm = np.median(t[m]); sh = m & (t < tm); dp = m & (t >= tm)
    print(f"  {lab:5s} tau[{lo:.3f},{hi:.3f}) n={m.sum():3d}: {cells} | U shallow half obs {F['U'][sh].mean():.3f} pred {P['U'][sh].mean():.3f}; deep half obs {F['U'][dp].mean():.3f} pred {P['U'][dp].mean():.3f}")
nv = np.array([x['n_valid'] for x in rq]); print("\nn_valid min/median/max", nv.min(), np.median(nv), nv.max())
