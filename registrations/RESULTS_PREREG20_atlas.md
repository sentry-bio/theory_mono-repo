# PREREG20 — Atlas arm (reported decomposition; no verdict, as registered). Run 2026-10-09 02:11–02:59 CEST
# (bacteria, 2,906 s; archaea 143 s); closure/atlas/closure_atlas_{bac,ar}.json; the amendment of 02:08 (maximal
# secant for the unsaturated kernel; analytic room) applied before the run.

## Check that the machinery is A-curve's
The pooled log error of the fitted family image, log(Σ_obs/Σ_fam) by ε = 0.4 … 2.0, is −0.002 / −0.016 / −0.041 /
−0.060 / −0.081 / −0.100 / −0.121 for the 262 bacterial test genera (5,384 genomes, 36 families) — A-curve's own
numbers to three decimals — and 0.000 / −0.006 / −0.048 / −0.072 / −0.111 / −0.147 / −0.175 for the 35 archaeal
genera (517 genomes), A-arch's. Same genus subsets, same rng stream, same kernels.

## The chain by resolution (pooled over genera; factors are means over genera of ratios of log₂ counts)
Bacteria (d = 135; median genus radius r = 5.97, median pair depth τ = 0.22):
| ε | Σ_obs | Σ_fam (kept) | Σ_lin (written) | n | occupancy | availability | writing | retention | residual | η_obs |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.40 | 5372 | 5383.8 | 5371.4 | 5384 | 0.008 | 0.622 | 0.999 | 1.001 | 0.999 | 0.0082 |
| 0.60 | 5293 | 5380.5 | 5336.4 | 5384 | 0.010 | 0.579 | 0.996 | 1.004 | 0.994 | 0.0097 |
| 0.79 | 5151 | 5364.9 | 5283.6 | 5384 | 0.011 | 0.547 | 0.992 | 1.008 | 0.984 | 0.0109 |
| 1.00 | 4993 | 5304.3 | 5205.0 | 5384 | 0.013 | 0.519 | 0.985 | 1.011 | 0.974 | 0.0123 |
| 1.25 | 4772 | 5177.1 | 5084.3 | 5384 | 0.015 | 0.493 | 0.974 | 1.012 | 0.962 | 0.0138 |
| 1.60 | 4457 | 4927.2 | 4866.2 | 5384 | 0.018 | 0.467 | 0.955 | 1.012 | 0.953 | 0.0162 |
| 2.00 | 4094 | 4618.6 | 4569.3 | 5384 | 0.025 | 0.458 | 0.927 | 1.012 | 0.943 | 0.0196 |
Archaea (d = 136; r = 5.06, τ = 0.19): occupancy 0.008 → 0.024; availability 0.35 → 0.31; writing 0.999 → 0.798;
retention 1.001 → 1.044; residual 1.000 → 0.922; η_obs 0.0076 → 0.0177.

Definitions as registered and amended: occupancy = log₂ n / log₂ M with log₂ M = d·log₂(r/ε); availability = the
family covariance's ellipsoid room over the ball's; writing = log₂ Σ_lin / log₂ n (the ε-resolution loss on the
unsaturated image, maximal-secant kernel); retention = log₂ Σ_fam / log₂ Σ_lin; residual = log₂ Σ_obs / log₂ Σ_fam
(A-curve's log error, as a factor). Collisions between genera are 1 by construction (not in AC1).

## Readings
1. The Atlas's η on the one operational definition is 0.008–0.02 at genus depth: a genus of ≤ 30 genomes asks for
   about five bits of identity from a room of 200–500 bits (135 dimensions at radius ≈ 6 against ε = 0.4–2). This is
   the efficiency table's "slack by construction", now a number: the composition medium is used to one or two percent
   of its room where genera live.
2. The largest loss below the demand is availability, 0.62 → 0.46 (bacteria) and 0.35 → 0.31 (archaea): roughly half
   of the family ellipsoid's axes are thinner than the reader's resolution, so half the room's dimensions are not
   available to the process at all. The archaeal process is confined to a third of the room's dimensions.
3. Retention is 1.00–1.01 (1.00–1.04 in archaea): saturation does not bind at genus depth. The fitted saturating
   kernel and the unsaturated maximal-secant kernel give the same packing to within 1% (4% in archaea); the sign
   (fitted slightly above linear) is the matrix-against-trace convention of the secant and is within that construction's
   noise. Composition's saturation is a family-depth phenomenon, not a genus-depth one.
4. The residual — the sixth loss on the Atlas — grows with ε from 1.00 to 0.94 (bacteria) and 0.92 (archaea): real
   genera are more compact than their Gaussian image, increasingly so at coarse resolution. It sits between
   retention and reading in the chain, it is larger in archaea, and it is the "deep collision remainder" that
   PREREG11–13 could not derive from a rate: compaction beyond the image, not saturation of the kernel.
5. Ordering of the Atlas's losses: occupancy (the demand is tiny against the room) ≫ availability > residual
   ≈ writing > retention ≈ 1. The recorder's ordering (PREREG20 recorder arm) was writer speed > correlated writing
   > reading > collisions; the two media lose in different places, which is what the audit is for.
