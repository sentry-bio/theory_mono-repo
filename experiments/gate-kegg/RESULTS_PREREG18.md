# PREREG18 — results (run 2026-10-09 01:21 CEST on the frozen files; scored by the registered rules)

## Verdicts
- **S1** (stratified, ≤ 120 genomes per phylum, seed 0; n = 1,935): **CERTIFIED POLYNOMIAL.**
  K1 13/13. K2 25/25 centres usable (data and null). K3 FAIL: 1/25 exponential (4%), 21/25 polynomial (84%),
  3 indeterminate. K4 PASS: null 24/25 polynomial. Polynomial ≥ 80% with K1, K2, K4 → CERTIFIED POLYNOMIAL.
- **S2** (uniform random 1,935, seed 18002): **INDETERMINATE.**
  K3 FAIL: 5/25 exponential, 18/25 polynomial (72%), 2 indeterminate. K4 PASS: 25/25. Polynomial 72% < 80%.
- K5 (reported): S1 MDS dimension 2, δ-ratio 0.323, h_slope median 48.0 (null 2.55), fitted polynomial exponent
  median 2.4 (null 1.75). S2 MDS dimension 5, δ-ratio 0.578, h_slope median 75.4 (null 2.16), exponent median 3.3
  (null 4.2).

v3.5 §2's kill line, as it states it ("the metric is certified polynomial against a matched null"), has fired on
v3.5's own sample.

## Checks that the analysis was done right (post-run, read-only; inspect_gate.py)
1. S1 is v3.5's sample exactly. The file holds 52 phyla; Σ min(count, 120) = 1,935 = the n v3.5 reports, and the
   δ-ratio 0.323 is v3.5's 0.32. The registration's remark that v3.5's sample was not reproducible from the files at
   hand is withdrawn: it is the stratified sample, and this run is on it.
2. The miss is not marginal. Data: R²_poly 0.87–0.99 against R²_exp 0.74–0.96, median margin ≈ 0.06 against a 0.01
   rule; the one exponential centre (61) fits both forms poorly (0.78 vs 0.56). Null: R²_poly 0.96–0.999.
3. Every centre had 39–40 radii and an occupancy span ≥ 30; the refusal rule never triggered.
4. The instrument re-certified 13/13 on this machine before being pointed at a genome. Hashes in run.log.

## Readings (separate from the verdicts)
- The classifier-level claim of v3.5 §2 replicates exactly: the pathway metric satisfies the four-point condition
  better than a Euclidean cloud (δ-ratio 0.32).
- The certified claim does not go through. Ball occupancy from genome centres grows as a power of the radius
  (exponent ≈ 2–4), on v3.5's own sample and on a random one. "Descent occupies exponential room" cannot be stated at
  Layer I for the KEGG pathway representation.
- Exponential room stays certified where it was certified: on sequence (the Atlas base map; Paper I's h_pack on the
  sequence medium). An 868-coordinate L1-normalised pathway profile is a reader's image of a genome, and a coarse
  reader can return a polynomial image of an exponential room — the audit's reading factor, in the same direction as
  PREREG16's wedge (composition-level readers lose genealogy first). This is a post-hoc reading, not a rescue: EAG v4
  §2 must carry the functional claim at classifier strength only, name this gate result, and locate the
  exponential-room claim on the sequence medium.
- S1's MDS dimension of 2 is the participation ratio of a spectrum dominated by the domain split; the Gaussian null
  at that dimension is the registered null, and the gate had power on it (24/25 polynomial).

## What this changes
EAG v4 §2: one paragraph rewritten as above. Experiments table row 2: CERTIFIED POLYNOMIAL (kill line fired).
One-page theory, status table: "exponential room certified" → sequence medium only; functional metric: hyperbolic
at classifier strength, growth certified polynomial.

Files: gate_results.json (per-centre fits), gate_run.log, run.log (sha256 of the frozen files), inspect_gate.py.
