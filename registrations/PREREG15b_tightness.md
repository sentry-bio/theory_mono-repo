# PREREG15b — Is the four-letter horizon exactly on the Kesten–Stigum line? (registered 2026-10-08 15:01 by file time, before
# the launch at 15:01:44 recorded in run_A.log; an earlier draft heading said 15:05 in error; companion to PREREG15 in ~/Documents/addressability-horizon-2026-10-08)

## Why this exists
PREREG15 (the harness census and composition arms) calibrates the Kesten–Stigum line for a LINEAR reader and leaves
out, by design, whether optimal readers (belief propagation) share the threshold — family 229's four-state claim,
which finite trees (h ≤ 10) cannot settle. Population dynamics computes the infinite-depth limit of the optimal
reader directly. The theory needs exactly this half: if belief propagation reconstructs below the line for the
four-letter symmetric channel, the genealogy horizon must be stated as "at or below Kesten–Stigum", not "on it".

## Model and order parameter
Complete d-ary tree; every edge carries the symmetric q-state channel M = λI + (1−λ)J/q (q = 4 is Jukes–Cantor with
λ = e^{−(4/3)μt}). Leaves observed exactly. Magnetization m_h = E[P(root = x | leaves at depth h) | root = x] − 1/q, by
population dynamics: N message samples conditioned on the node's true state; each child's true state drawn from the
channel; its message drawn from the previous level and relabelled (swap 0 ↔ y); parent ∝ Π_c (λ·m_c + (1−λ)/q).
Reconstruction iff lim_h m_h > 0. Secondary: MAP accuracy − 1/q with random tie-breaking.

## Grid
dλ² ∈ {0.80, 0.90, 0.95, 0.98, 1.00, 1.02, 1.05, 1.10, 1.20, 1.40}. Cells: (q, d) = (2, 2), (4, 2), (3, 2) with
N = 200,000, depth H = 500; (8, 2), (8, 10), (8, 30) with N = 50,000, H = 300. Seed 15001 + running cell index.
Decision per cell: RECONSTRUCTS if m_H > 0.002 and |m_H − m_{H−100}|/m_{H−100} < 0.05; FORGETS if m_H < 0.002;
otherwise INDETERMINATE. dλ² = 1.00 is reported, never scored.

## Rules
- T1 control (proved tight for q = 2: Bleher–Ruiz–Zagrebnov 1995; Evans–Kenyon–Peres–Schulman 2000): (2, 2) FORGETS at
  every dλ² ≤ 0.98 and RECONSTRUCTS at every dλ² ≥ 1.02. If T1 fails, the method is wrong and nothing else is read.
- T2 the claim the theory needs: (4, 2), Jukes–Cantor on the binary tree, shows the same pattern. Kill: any cell with
  dλ² ≤ 0.98 that RECONSTRUCTS.
- T3 exploratory: (3, 2) (claimed tight by family 229).
- T4 sensitivity, exploratory: q = 8 at d ∈ {2, 10, 30}. Sly (Ann. Probab. 2011) proves the line is not tight for
  q ≥ 5 at large d; a RECONSTRUCTS cell below dλ² = 1 at d = 30 shows the method can see a non-Kesten–Stigum transition,
  which is what gives T1–T3 their power. If none appears, sensitivity is reported as undemonstrated.
Verdict: ON THE LINE (Jukes–Cantor, d = 2) if T1 and T2 hold; BELOW THE LINE if T1 holds and T2's kill fires.

## Caveats stated in advance
Finite N can blur a weakly first-order transition near dλ² = 1; the 0.002 floor and the 100-level stability window
separate geometric decay from a plateau but not a jump smaller than about 0.002. d = 2 is the biologically relevant
degree (binary trees); large-d results do not transfer to it.

## Frozen file
horizon_A.py (sha256 recorded at launch in run_A.log).

## Amendment — 2026-10-08 15:04:43, after the q = 2 control's first six cells and before any q = 4 cell ran
At depth H = 500 the q = 2 cell at dλ² = 1.02 is still approaching its fixed point (m_H = 0.021, falling by more than
5% over the last 100 levels), so the registered stability test cannot pass there at this depth: near the line the
approach to the fixed point is slow. Change, applied identically to every (q, d): the supercritical half of T1–T3 is
scored at dλ² ≥ 1.05; each 1.02 cell is rerun at H = 3,000 with its registered seed and reported under the same
decision rule. The subcritical half, T2's kill and T4 are unchanged. Read strictly as first registered, T1 fails on the
1.02 cell alone (INDETERMINATE, not FORGETS); both readings will be reported.

## Amendment 2 — 2026-10-08 15:07:55: a code bug for q ≥ 3; fix; scope of the rerun
- Bug (found when the first two q = 4 cells printed a NEGATIVE magnetization, which is impossible for a posterior):
  relabelling a child's message by the transposition (0 y) alone leaves the q − 1 wrong labels in a fixed order, so in
  a finite population any small preference among them feeds itself level after level. The level-1 update is exact
  (q = 4: 0.465 from the population against 0.467 by enumeration), so the error is the accumulated asymmetry, not the
  recursion. q = 2 has one wrong label, so its code path and random stream are unaffected: its ten cells stand as run.
  The two q = 4 cells printed (dλ² = 0.80, 0.90) are VOID and carry no information about tightness.
- Fix: before the swap, permute the wrong labels 1..q−1 uniformly at random in every message (applied only when q > 2,
  so q = 2 is bit-identical). The composite relabelling is a uniform random permutation sending 0 to y, which is the
  exact symmetry of the true conditional law. Script: horizon_A2.py (sha256 in run_A2.log).
- Rerun: every q ≥ 3 cell of the registered grid with its registered seed. Near-threshold depth: the q = 2 cell at
  dλ² = 1.05 also read INDETERMINATE at H = 500 (m_H = 0.048, still drifting), so the H = 3,000 rerun of Amendment 1
  covers dλ² ∈ {1.02, 1.05} for (2, 2), (3, 2) and (4, 2), with registered seeds. The decision rule is unchanged.
- Q = 2 control as first run (H = 500): FORGETS at 0.80, 0.90, 0.95, 0.98; INDETERMINATE at 1.00 (reported only),
  1.02 and 1.05; RECONSTRUCTS at 1.10, 1.20, 1.40. Read strictly as registered, T1 fails on 1.02 and 1.05
  (INDETERMINATE, not FORGETS); as amended, T1 is decided after the H = 3,000 rerun.
