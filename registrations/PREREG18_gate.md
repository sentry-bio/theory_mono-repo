# PREREG18 — the growth-class gate on the native functional metric (registered 2026-10-09, before the gate was pointed
# at any genome)

## What this decides
v3.5 §2 claims descent occupies exponential room, read from a functional representation that is not a sequence tree,
at *classifier strength* (δ-ratio 0.32 against a Euclidean null). It names one run that graduates that to *certified*:
the growth-class gate on the KEGG functional metric. This registration is that run. Kill line, as v3.5 states it: the
metric is certified polynomial against a matched null.

## Instrument (frozen copy: m3_growth_class.py from Zenodo_v2, unchanged)
growth_class(D, root_index, margin = 0.01): from one centre, the ball-occupancy curve P(ρ) over 40 radii between the
3rd and the ⌊n/2⌋-th nearest neighbour; adjusted R² of log P against ρ (exponential) versus log P against log ρ
(polynomial); verdict "exponential" if R²_exp > R²_poly + 0.01, "polynomial(h_pack~0)" if the reverse, else
"indeterminate". Its own certification (13 of 13: b-ary trees and H² read exponential; grids and Euclidean minimum
spanning trees read polynomial) is re-run here first (K1).

## Data and samples
kegg_profiles_868.npz: 29,303 genomes × 868 KEGG pathway dimensions, each profile L1-normalised, all with GTDB-style
taxonomy in reference_manifest.csv (21,378 bacteria, 5,402 archaea, 2,523 eukaryotes; 52 phyla). Distance = angular
distance arccos(⟨u, v⟩ / ‖u‖‖v‖) / π on L2-normalised profiles, as in run_native_functional.py.
- S1 (primary): the stratified sample run_native_functional.py defines — up to 120 genomes per phylum, seed 0, capped
  at 5,000 — recomputed on this file.
- S2 (secondary): 1,935 genomes drawn uniformly at random, seed 18002, matching the n v3.5 reports.
v3.5's 1,935-genome sample is not reproducible from the files at hand; S1 is the registered claim and S2 the n-matched
check. Centres: the medoid of each sample plus 24 genomes drawn at random (seed 18001), 25 per sample.

## Null
For each sample, a Gaussian cloud of the same n in the sample's classical-MDS dimension (participation ratio of the
double-centred squared-distance spectrum, as run_native_functional.py computes it), seed 18003, with Euclidean
distance; the same 25 centres by index. A gate that cannot read this cloud as polynomial has no power at this
dimension, and the verdict is INDETERMINATE regardless of what the data read.

## Rules
- K1 instrument: the frozen gate re-certifies 13 of 13 on this machine. If not, nothing below is read.
- K2 refusal: a centre is usable only if its occupancy curve has ≥ 20 radii and its occupancy spans a factor ≥ 30
  (at least 1.5 decades). A sample is scored only with ≥ 15 usable centres.
- K3 data: ≥ 80% of usable centres read "exponential" and ≤ 10% read "polynomial".
- K4 null: ≥ 80% of usable null centres read "polynomial".
- K5 (reported): the h_slope distribution over centres; the δ-ratio (delta_hyperbolicity of the data against the
  Euclidean null, volume_entropy.py) to compare with v3.5's 0.32; the MDS dimension.
Verdict for S1: CERTIFIED EXPONENTIAL if K1–K4 hold; CERTIFIED POLYNOMIAL if K1, K2, K4 hold and ≥ 80% of usable
centres read polynomial; INDETERMINATE otherwise. S2 is reported with the same rules as a replication.

## What a pass licenses in EAG v4
§2's occupancy claim moves from classifier-level to certified Layer I, with the sample named and the null stated. It
licenses nothing about which exponential host, and nothing about saturation.

## Caveats stated in advance
Angular distance is bounded (≤ 1), so ball growth from any centre saturates at n; the gate's window (3rd to n/2-th
neighbour) is designed for that, but a bounded metric at high intrinsic dimension concentrates distances, which is
exactly what K4 checks. The gate is a model comparison on one curve per centre, not a sample-size scaling test;
the two agreed on all 13 certification hosts. Centres are genomes, not a generative root; the curve from a leaf
of an exponential tree is still exponential, but with a shorter window than from the root.

## Frozen files (sha256 in run.log at launch)
m3_growth_class.py, volume_entropy.py, gate_run.py, kegg_profiles_868.npz, reference_manifest.csv.
