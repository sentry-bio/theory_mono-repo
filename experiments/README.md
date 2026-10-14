# Experiments

One folder per experiment. Each holds its registration (written before the data), the frozen scripts, a `run.log`
with clock times and SHA-256 hashes of the frozen files, the raw results (JSON), and a `RESULTS_*.md` that scores the
registered verdicts and reports readings separately. Copies of the registrations and results are indexed in
`../registrations/README.md`. Earlier experiments (PREREG00–16) ran in dated folders outside this repository; the
ledger names them.

| Folder | Registration | Verdict as registered | Data (fetched, not stored) |
|---|---|---|---|
| `exp1-composition/` | PREREG17 composition's worth as one claim, new seeds | NOT PREDICTED (length-ratio band); level 24/24 within 3 SE, decay and letter-count value held | synthetic |
| `gate-kegg/` | PREREG18 growth-class gate on the KEGG functional metric | S1 CERTIFIED POLYNOMIAL on v3.5's own sample; S2 indeterminate | KEGG pathway profiles (868 genomes); `kegg_profiles_868.npz` and `reference_manifest.csv` excluded |
| `testB/` | PREREG19 misspecification control; PREREG19b block structure against the site-permutation null | 19 INCONCLUSIVE; 19b BLOCK DISCRIMINATOR WORKS (mixing 94–100% blocked, heterotachy 4–6%) | synthetic |
| `closure/` | PREREG20 closure of the audit (recorder arm, Atlas arm) | CLOSURE LOCATED on both recorder splits with the sixth loss (correlated writing); Atlas arm reported (η ≈ 0.01, availability binds) | intMEMOIR processed data (analysed in place, excluded); GTDB r220 trees and taxonomy; Atlas base map v1.0 coordinates (symlinked, excluded) |
| `closure/mi/` | PREREG24 the audit in mutual information | NOT AS REGISTERED on both splits: chain ordered, the reading anomaly was the measure, closure fails on the recorder | intMEMOIR (as above) |
| `horizon21/` | PREREG21 composition's horizon with an ancestor-aware reader | HORIZON READ in bacteria (36 families); FAIL in archaea | Atlas kernels (excluded) |
| `horizon-A/` | PREREG15b four-letter tightness (scoring script and results only) | on the line for four letters; registered verdict not reached on one control cell | synthetic |
| `horizon22/` | PREREG22 two-reader rate-spectrum horizon | LAW CONFIRMED IN SIMULATION, V1–V5 | synthetic |
| `horizon23/` | PREREG23 rate-class test on GTDB r232 bac120 | NOT SUPPORTED AS REGISTERED (every cell unresolved; readings reported) | GTDB r232 bac120 MSA and tree (MD5-verified, deleted after hashing); the derived subsample alignment `work/sub.faa` excluded (CC BY-SA 4.0, 7.5 MB); IQ-TREE binary excluded |
| `horizon23b/` | PREREG23b the rate-tail law on vertebrate mitogenomes (four dated amendments) | NOT SUPPORTED AS REGISTERED (registered truth-set clause unsatisfiable by construction; secondary analyses unresolved); readings: parameter-free prediction within 0.025 at L ≤ 512, rate-weighted reader above unweighted by the predicted growing margin, a ~30% floor at full length | NCBI RefSeq release 237 mitochondrion (public domain), fetched by `fetch_mito.py`; alignment and tree built in scratch |
| `openai-math-lean/` | Lean comparator statements for the openai/math families that sit on this frame's ground (148, 229, 099) | reference material, not a registration | — |

Compute policy, recorded in each `run.log`: heavy jobs run on biosphereatlas in a single scratch directory under
`nice`, with memory capped; the scratch directory is deleted after the results are copied here and audited against
their hashes. Locally, IQ-TREE is run with `-mem 2G -nt 4` on an 8 GB machine.
