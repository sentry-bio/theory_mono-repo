# Lineage recorders (intMEMOIR) — pre-registration

Written 2026-09-26 before any model was fitted or any recording statistic computed. Only descriptive facts were
looked at: 107 colonies with true trees (s18c3 has none and is excluded), 1,454 cells, 1,347 divisions, binary
trees 0–6 generations deep, cell cycle ~48 frames, leaves at frame 216.

Data: intMEMOIR (Chow et al. 2021, Science) as processed and redistributed by raphael-group/intmemoir-processed-data:
per colony a 10-site character matrix (1 = unedited, 0 = deletion, 2 = inversion) and the true lineage tree from
time-lapse imaging, with division times in frames. Analysed in place; not redistributed.

## What is being tested

The theory's recorder picture: a lineage recorder is a write-limited, decay-free channel. History is retained
only while the writer keeps pace with lineage growth; each division is one bit that must be written onto the
daughter branches before they divide again. R1 and R2 are standard irreversible-mutation predictions (the same
model Cassiopeia-style methods use); R3 is the regime statement the addressability framing adds.

## Design

- Split: colonies to train/test by md5("E-R:" + colony) parity. Everything is fitted on train only.
- Writer model: each site s edits with hazard κ_s·λ(t), λ piecewise constant over absolute frames
  [0,60), [60,110), [110,160), [160,217]; an edit is a deletion with probability q_s, else an inversion; edits are
  irreversible; at colony start a site is already edited with probability p0_s; each leaf state is misread with
  probability ε (to either other state equally). Maximum likelihood by pruning on the true trees.
- Recorded division: internal node v with daughter clades A and B is recorded if some site s and edited state
  a ∈ {0, 2} have all leaves of A in state a and not all leaves of B in state a, or the reverse.
- Generation of a division: its depth below the first division (first division = 0).
- Clade signature of a lineage: per site, a if all its leaves are in edited state a, else unedited.
- Predictions: 500 simulations of the fitted writer on each test tree (true topology and times), computing the same
  statistics; per-division predicted probabilities and per-generation predictive distributions.
- Expected distinguishing events per division, m_v: Σ_s P(s unedited at t_v) · [(1 − e^(−Λ_s(A))) + (1 − e^(−Λ_s(B)))]
  with Λ_s(X) the integrated hazard over daughter branch X (prior predictive, fitted parameters).

## Rules

- R1 division recording: in every generation with >= 30 test divisions, |observed − predicted| <= max(0.07, 2 SE of
  the predictive distribution); and calibration over 5 bins of predicted probability has mean |error| <= 0.05.
- R2 distinguishable lineages: collision fraction C_g = 1 − Σ D_g / Σ N_g over test colonies (N_g lineages at depth g,
  D_g distinct clade signatures among them, counted per colony) within max(0.07, 2 SE) of prediction in every
  generation with >= 50 test lineages.
- R3 regime: g_c = first generation whose mean m_v < ln 2 (from the train fit). PASS if the observed recorded fraction
  is >= 0.5 in every generation before g_c and < 0.5 in every generation after g_c (g_c itself may go either way). If
  m_v >= ln 2 in all generations, PASS requires >= 0.5 in all generations.
- Reported, not gated: the envelope P(recorded) <= min(1, m_v) plus spurious records from misreads; efficiency
  (observed / envelope) by generation; age dependence at fixed m_v (decay-free memory predicts none beyond homoplasy).

## Amendment — 2026-09-26 16:29, before fitting (found while loading the trees)

26 of the 107 trees have a root labelled "virtual" that joins two imaged founder lineages whose branches start at
frame ~1. It is not an imaged division and its timing is unknown. Handling: the virtual root is placed at the
founders' common start time with a zero-length root edge; it is excluded from all division statistics; generations
are counted so that the first imaged division is generation 0 in every tree (lineage statistics use depth >= 1).

## Amendment R3 — 2026-09-26 16:30, after the train fit, before any test prediction or statistic

The train fit shows the writer switches on late (hazard 0.0006/frame before frame 60, ~0.009/frame after), so
expected writing per generation rises and then falls; it is not monotone as R3's "first crossing" wording assumed.
R3 is restated in its general, per-generation form: for every generation with >= 30 test divisions, the observed
recorded fraction is >= 0.5 if mean m_v >= ln 2 and < 0.5 if mean m_v < ln 2. R1 and R2 are unchanged.
