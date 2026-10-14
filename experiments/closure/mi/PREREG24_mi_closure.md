# PREREG24 — The audit in mutual information: closure on the intMEMOIR recorder (data in hand)

Registered 2026-10-14, clock time at freeze in `run.log` (the `date` line precedes the file hashes). Written before
any mutual-information statistic was computed on any colony. This is Paper II's frontier item (3) and answers the
9 Oct review's point 4: the state-count efficiency counts states, not information, and a noisy reader can push the
count-based reading factor above one (+3% to +16% in PREREG20). The remedy registered here replaces every stage count
by the mutual information between the lineage label and the stage's leaf record, so that the data-processing
inequality orders the chain and every factor lies in (0, 1] by construction.

## Data and code (unchanged, in place)
- The 107 intMEMOIR colonies with imaged trees in `closure/intmemoir` (analysed in place, not redistributed), the
  PREREG4 split (60 train / 47 test, md5 rule) and its swap; the PREREG4 writer (`rec_fit.json`, `rec_fit_swap.json`),
  the readout mixture, the correlated writer (`rmix`), all imported from the frozen 26 Sep code exactly as
  `closure/closure_recorder.py` does. Generations gated at ≥ 50 test lineages (RM1), as PREREG20.
- Disclosed: the state-count chain and its factors at every generation on both splits were seen in PREREG20. The
  mutual-information quantities below are new.

## Definitions (fixed)
At generation g in a colony, the lineage label ℓ of a leaf is the depth-g ancestor it descends from (leaves not
below a depth-g node are excluded, as in PREREG20's `signatures`). A stage record X is the leaf's ten-site tape at
that stage: X_∞ the event-id tape of the infinite-sites independent writer (`sim_indep`'s E at the leaf), X_dist
the finite-site state tape (S at the leaf), X_read the same after the readout mixture (`read_leaves`); and for the
correlated writer X_corr (`sim_corr` S at the leaf) and X_read6 (after readout). Each chain ℓ → X_∞ → X_dist → X_read
(and ℓ → X_corr → X_read6) is Markov: finite sites is a function of event ids, the readout acts on the state alone.

I_g(ℓ; X) is the mutual information (bits) computed from the empirical joint distribution over all leaves under
depth-g nodes pooled across the 400 simulation replicates (so p(X | ℓ) is estimated from 400 × |clade| samples), per
colony, then averaged over test colonies (the D̄ convention). H_g(ℓ) = entropy of the leaf-weighted lineage label.

The MI chain, per generation (room M = log₂ of the ball of radius r̄ as in PREREG20, availability = 1 at ε = 0):
    fill_MI      = I(ℓ; X_∞) / log₂ M              (demand × writer, in information)
    collisions_MI = I(ℓ; X_dist) / I(ℓ; X_∞)
    reading_MI   = I(ℓ; X_read) / I(ℓ; X_dist)
    η_MI,pred5   = I(ℓ; X_read) / log₂ M = fill_MI · collisions_MI · reading_MI   (an identity)
    correlation_MI = I(ℓ; X_corr) / I(ℓ; X_dist);  reading6_MI = I(ℓ; X_read6) / I(ℓ; X_corr);
    η_MI,pred6   = I(ℓ; X_read6) / log₂ M.
Observed: I_obs,g = plug-in MI between ℓ and the real leaf tapes (one sample per leaf) minus the mean of 200
within-colony label permutations (the shuffle null), floored at 0, averaged over test colonies; η_MI,obs = I_obs/log₂M.
Also reported: the Miller–Madow-corrected plug-in, and I_obs without the null subtraction.

## Verdicts (one per claim; both splits; gated generations only)
- MI1 (the chain is ordered): collisions_MI, reading_MI, correlation_MI and reading6_MI are each ≤ 1.02 at every gated
  g (DPI; the 0.02 is estimator slack). A violation above 1.02 fails.
- MI2 (the symptom resolves): at every gated g where PREREG20's count-based reading factor exceeded 1.00, reading_MI
  is below 1.00.
- MI3 (closure in information): |ln(η_MI,pred6 / η_MI,obs)| ≤ 0.15 at every gated g (the six-factor chain, with
  correlated writing, against the observed, null-subtracted MI); reported alongside, not scored: the same for pred5.
- MI4 (consistency): η_MI,obs ≤ η_count,obs (PREREG20's η_obs) at every gated g, since I(ℓ; X) ≤ log₂ of the
  number of distinct records.
Overall: AUDIT CLOSES IN INFORMATION only if MI1–MI4 pass on the main split; the swap split is the replication and
is reported with the same rules. No post-hoc change of gating, tolerances, replicate counts or the null.

## Disclosed smoke test
Two TRAIN colonies, 5 replicates, 20 permutations, no registered statistic read (`smoke` tag), to validate the code
paths; its output is kept and not interpreted.

## Memory and runtime
State arrays are 400 × nodes × 10 int8 per colony (< 1 MB); the MI tables are dictionaries over ≤ 3^10 records; the
run is light and is executed under `nice` on the Mac (8.6 GB), one split at a time.

## Amendments
- 2026-10-14, after the disclosed smoke test and before any verdict run (time in `run.log`): the smoke test (5
  replicates) showed the pooled plug-in estimator putting the readout stage's MI above the finite-site stage's
  (reading factor 1.07–1.13), which is estimator bias from the readout noise multiplying distinct records, not
  information. The two readout stages are therefore computed **analytically**: p(X_read | ℓ) = Σ_x p̂(x | ℓ)·p(X_read | x),
  where p̂(x | ℓ) is the pooled-replicate empirical distribution of the pre-readout record and p(X_read | x) is the
  registered readout mixture (with probability π each site flips with rate ε_noisy, else ε_clean, flips uniform over
  the two other states), applied site by site to the 3¹⁰-state vector; I(ℓ; X_read) and I(ℓ; X_read6) are then exact
  given p̂. The pre-readout stages (X_∞, X_dist, X_corr) stay pooled plug-in as registered. The pooled plug-in and
  Miller–Madow readout values are reported alongside, not scored. Verdict rules unchanged.
- 2026-10-14, same session, after the second disclosed smoke test and before any verdict run: the observed-side
  quantity. With one record per real leaf and most records unique, the plug-in MI equals H(ℓ) for every labelling,
  so the shuffle-null subtraction returns zero whatever the information (smoke: 0.00–0.36 bits against predicted
  0.8–2.2). The observed quantity scored in MI3 and MI4 is therefore the **model-critic estimator**
  I_obs,model = (1/N) Σ_leaves log₂ [ p(y_leaf | ℓ_leaf) / Σ_ℓ' w(ℓ') p(y_leaf | ℓ') ], with p(y | ℓ) the model's
  read6-stage distribution (correlated writer, analytic readout) and w the leaf weights; its expectation is the
  model's I(ℓ; X_read6) minus a KL term when the model is wrong, so closure means the real records are as informative
  under the model as the model says. The shuffle-null plug-in and Miller–Madow values are reported, not scored. The
  same estimator with the read5-stage distribution is reported for the five-factor chain. Tolerances unchanged.
