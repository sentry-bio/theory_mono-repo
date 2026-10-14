# PREREG15b — result (scored 2026-10-08 by score_A.py; registration, amendments and run logs in
# ~/Documents/addressability-theory-2026-10-08/horizon-A; this file sits in the worktree because a guard keeps this
# background session's new files out of the shared checkout)

## Verdict
- As registered: NOT REACHED. T1's supercritical half fails on one cell, (q = 2, dλ² = 1.05), which reads INDETERMINATE at
  H = 500 and at H = 3,000. Its magnetization holds at 0.048–0.054 over levels 2,500–3,000 with no decay; the registered
  stability rule (< 5% change over 100 levels) is tighter than the population's own fluctuation at that level.
- Substantive reading: ON THE LINE for the four-letter (Jukes–Cantor) channel on binary trees. Every T2 cell passes, T3
  passes, and T4 shows the method detects reconstruction below the line where it is known to exist.

## Cells (m_H = magnetization at the last level)
| Cell | Below the line (0.80 / 0.90 / 0.95 / 0.98) | At the line (1.00, reported only) | Above the line |
| --- | --- | --- | --- |
| q = 2, d = 2 (control) | forgets at all four | m = 0.0026, decaying | 1.02 reconstructs at H = 3,000 (m ≈ 0.02); 1.05 INDETERMINATE (m ≈ 0.05, steady); 1.10–1.40 reconstruct |
| q = 4, d = 2 (Jukes–Cantor) | forgets at all four | m = 0.011, decaying | reconstructs at 1.02 (m ≈ 0.06), 1.05 (≈ 0.12), 1.10, 1.20, 1.40; same at H = 3,000 |
| q = 3, d = 2 | forgets at all four | m = 0.005, decaying | reconstructs at 1.05 (H = 3,000), 1.10–1.40; 1.02 at H = 3,000 INDETERMINATE (m ≈ 0.04, steady) |
| q = 8, d = 2 | forgets at 0.80–0.95; 0.98 INDETERMINATE (m still falling at H = 300) | reconstructs, m = 0.10 | reconstructs everywhere |
| q = 8, d = 10 | forgets at 0.80–0.90; 0.95 INDETERMINATE; reconstructs at 0.98 | reconstructs | reconstructs everywhere |
| q = 8, d = 30 | forgets at 0.80–0.90; reconstructs at 0.95 and 0.98 | reconstructs | reconstructs everywhere |

## Rules
- T1 (q = 2 control): subcritical half PASS; supercritical half FAIL as first registered (1.02 and 1.05 INDETERMINATE at
  H = 500) and FAIL as amended (1.05 INDETERMINATE at H = 3,000).
- T2 (q = 4): PASS as first registered and as amended; the kill (reconstruction below the line) does not fire.
- T3 (q = 3, exploratory): PASS.
- T4 (sensitivity, exploratory): demonstrated — reconstruction below the line at d = 10 (0.98) and d = 30 (0.95, 0.98),
  where Sly (2011) proves the line is not tight for q >= 5 at large degree.

## Readings (not verdicts)
- The four-letter onset is continuous: the magnetization grows roughly linearly from the line (about 3 × (dλ² − 1) near it),
  the signature of a transition exactly at Kesten–Stigum.
- q = 8 at d = 2 already holds m = 0.10 at the line itself, unlike q ≤ 4 (m ≤ 0.011, decaying): a discontinuous onset at or
  just below the line. Not registered; a candidate follow-up.
- Population size bounds what this can see: a jump in magnetization smaller than about 0.002 at the line would be missed.
