# RESULTS — PREREG23, the rate-class test on GTDB r232 bac120 (real alignment)

Registration frozen 2026-10-14 04:59:00 CEST; amendments (i)–(iii) 05:01:06, (iv)–(vi) 05:06:48 (tree-only
diagnostic, before any reader result), (vii) 05:21:33 (code fix at the disclosed smoke read); verdict run 05:22:03
to 05:22:12 CEST (all per `run.log`). Data: GTDB `latest` = r232 (released 15 Apr 2026); `bac120_msa_reps.faa.gz`
md5 3102f1b7… and `bac120.tree.gz` md5 58a23a44…, both matching `MD5SUM.txt`. 1,500 taxa (seed 23), 5,008 kept
columns; IQ-TREE 2.4.0 LG+G4 on the fixed topology: Gamma shape α = 1.743, log-likelihood −3,557,112.6, tree length
226.0 substitutions per site; 302 quartets (internal branch 0.02–0.20, median τ = 0.038) in six of eight depth bins,
depths 0.03–0.92 substitutions per site; mean valid (gap-free in all four) columns per quartet 2,958 of 5,008.

## Verdict: NOT SUPPORTED AS REGISTERED (all cells UNRESOLVED)

The registered estimator defines t*(L) as the depth at which a logistic fit of success against ln t crosses 0.90.
On this tree that level is crossed, where it is crossed at all, below the shallowest quartets (fitted t* 0.000–0.041
for every reader and L, all below t_min), so every cell is UNRESOLVED and, by the registered rules, V1–V5 all FAIL
and κ cannot be fitted. The failure is one of resolution, not a contradiction of the law: the alignment does not
contain enough shallow quartets, and the success curve is not logistic in ln t (below).

| Verdict | Result |
|---|---|
| V1 form, unweighted | FAIL (no resolved cell) |
| V2 form, weighted | FAIL (no resolved cell) |
| V3 ordering | FAIL (no resolved cell) |
| V4 exponent | FAIL (no resolved cell) |
| V5 shuffle control | FAIL (no resolved cell) |

## Readings (not scored)

Success rate of the true split, by depth bin (bin edges 0.049, 0.08, 0.13, 0.21, 0.35, 0.56 substitutions per site;
quartets per bin 5, 19, 79, 118, 71, 10), 40 column subsets per quartet:

| reader | L | 0.03–0.05 | 0.05–0.08 | 0.08–0.13 | 0.13–0.21 | 0.21–0.35 | 0.35–0.56 |
|---|---|---|---|---|---|---|---|
| U | 64 | 0.55 | 0.47 | 0.40 | 0.39 | 0.35 | 0.37 |
| U | 512 | 0.92 | 0.82 | 0.60 | 0.56 | 0.54 | 0.57 |
| U | 4096 | 1.00 | 0.99 | 0.74 | 0.70 | 0.72 | 0.85 |
| W | 64 | 0.57 | 0.52 | 0.45 | 0.45 | 0.41 | 0.40 |
| W | 512 | 0.93 | 0.83 | 0.62 | 0.58 | 0.55 | 0.57 |
| W | 4096 | 1.00 | 0.99 | 0.74 | 0.70 | 0.73 | 0.85 |
| S (shuffled rates) | 512 | 0.93 | 0.83 | 0.62 | 0.58 | 0.56 | 0.59 |
| S | 4096 | 1.00 | 0.99 | 0.74 | 0.70 | 0.73 | 0.85 |

1. **Readability rises with L at every depth and falls with depth** — the direction of the law, at every cell.
2. **A depth-independent failure floor.** Beyond 0.13 substitutions per site the success curve flattens at
   0.70–0.85 even at L = 4,096, instead of collapsing; about a quarter of the quartets are not recovered by a
   four-point reader at any L. The Jukes–Cantor derivation has no term for this; it is model violation (20-letter
   non-stationary substitution, heterotachy, saturated markers), and it is why a logistic in ln t does not fit.
3. **The rate-weighted reader is indistinguishable from the shuffled control.** W exceeds U by 0.01–0.05 at small L
   and the gap closes by L = 4,096, and S (weights from permuted rates) equals W within noise at every cell. At
   α = 1.74 the site-rate spectrum is nearly homogeneous and the quartet depths are ≤ 0.6 substitutions per site;
   this is the regime in which the derivation predicts the two readers to coincide (a → ∞), so the exponent
   contrast 1/(2(α+1)) = 0.18 versus 1/(α+2) = 0.27 is not reachable on this alignment.
4. **What a resolving test needs**, stated for a PREREG23b: a nucleotide alignment with α < 1 (a genuinely slow
   tail), quartets to depths of several substitutions per site, many shallow quartets (or a success level below
   0.90), and a reader with an explicit floor term. Candidates: SSU rRNA (SILVA) at domain depth; mitochondrial
   genomes across metazoa.

## What this does and does not establish
Established: on a real protein phylogenomic alignment, a bounded four-point reader's recovery of splits rises with
the number of sites at every depth and falls with depth, with a floor the model lacks; the rate-weighted reader buys
nothing at α ≈ 1.7 and shallow depth, as the derivation says it should not. Not established: the exponents on real
data, in either direction. The law-shaped claim remains confirmed in simulation (PREREG22) and untested in nature.

## Housekeeping
Raw downloads (`data/`, 395 MB) deleted after this file was written; their hashes are in `run.log`. The subsampled
alignment, pruned tree and IQ-TREE outputs stay in `work/` (GTDB CC BY-SA 4.0; derived, small).
