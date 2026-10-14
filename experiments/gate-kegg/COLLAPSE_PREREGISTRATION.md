# The Certified-Ruler Collapse — Preregistration (frozen 2026-07-03)

**One equation, two independently measured numbers, one parameter-free line.**

## The reduction

Membership in the scale-covariant hyperbolic universality class does **not** require
disentangling `n` and `κ`. The state equation is

    (n−1)√κ  =  h_eff · ln2.

The left side is *exactly the volume entropy* `h_vol` of the manifold (Manning). So the
entire membership test is a single scalar identity between a **geometry** measurement and
an **information** measurement:

    h_vol   =   h_eff · ln2          (both in nats per generative step)

`n` and `κ` are absorbed into `h_vol` and never measured separately. This bypasses the two
places every prior leg failed the audit (a scale-free "curvature" that tracked dimension;
a tree-reconstructed "n=2" that was tautological).

## The two axes — disjoint pipelines (anti-circularity)

- **x = h_eff·ln2** — measured **only from the generating process**, never from geometry.
  (Genomic: bits per substitution from the mutation process. Linguistic: bits per sound
  change from the Index-Diachronica transition matrix. Neural: entropy rate of the code.)
- **y = h_vol** — measured **only from the static distance geometry**, root-referenced
  ball growth, with the certified estimator below. Never back-solved from `h_eff`.

A domain enters the plot **only if both axes are independently measured**. One certified
axis is not enough; a domain with a pending axis is shown as pending, not placed on the line.

## The certified ruler (frozen before any real data)

`certified_volume_entropy.volume_entropy(dist_from_root, unit=1)` — root-referenced
exponential growth rate of `N(R)` = number of nodes within radius `R`, radial coordinate =
generative depth. It must pass **four gates** (see `certify()`), or it is disqualified:

1. **Recovery.** On synthetic `b`-ary generators (b = 2..12), returns `ln(b)` within 5%.
   Equivalently, recovers `h_eff·ln2` across a wide range → establishes the diagonal.
2. **Flat null → 0.** On Euclidean point clouds of *any* dimension (3..200), returns ≈ 0
   (polynomial ball growth has zero exponential rate). This is the gate `tri_kappa` failed
   (it returned 0.18–0.47, tracking dimension).
3. **Dimension-independence.** The recovered `h_vol` for a fixed generator does not change
   when the ambient embedding dimension changes — it is intrinsic, not a dimension proxy.
4. **Unit-covariance.** `h_vol` scales as `1/unit` (it carries units of inverse length /
   inverse step), unlike a scale-invariant shape statistic. Confirms it is a rate.

## Nulls drawn on the collapse figure

- **Flat/whiten null** → points fall onto the x-axis (`h_vol → 0`).
- **Rate-scramble null** → randomize the generator rate independent of geometry → correlation destroyed.
- **Per-domain-offset alternative** → if not one class, domains land on separate lines.

## The prediction and the verdict

Scatter every qualifying system as `y = h_vol` vs `x = h_eff·ln2`. Prediction is
**parameter-free**: slope 1, intercept 0, all domains on one line. Pass = the domains land
on the diagonal within the synthetic tolerance AND the flat null sits on the x-axis AND the
slope-1/intercept-0 fit is not rejected. Fail = separate lines, wrong slope, or no correlation.

**Discipline:** two domains on the diagonal with independent axes beats three with one
fudged axis. If a domain cannot produce an independent `h_eff` (neural) or a certified
`h_vol` (linguistic), it waits — and the figure says so.
