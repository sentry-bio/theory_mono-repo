# Manuscripts and the debut package — snapshot 2026-10-14 (worktree `theory-oct8`, uncommitted)

## BRF2026 DATUM SPEC SHEET (draft 0.1, 14 Oct) — `brf2026/BRF2026_spec_sheet.tex` / `.pdf`, 2 pages
The hinge between the datum and the papers: one row per component (base map, containment, backbone, witness,
sextant, gate, novelty, chimera, audit) with the band claimed, the licensing theorem or Lean declaration, the
registration and its number, and what would falsify the band; the four open items carried by this realisation
(0.2 substitutions-per-site horizon unmeasured; archaea; PREREG23b pending; organelles/viruses outside); the
realisation rule (no learned component in the foundation layer; no coordinate moved by a later realisation; every
band carries its registration). To be re-issued with every realisation. Numbers taken from the base-map v1.0
document and the ledger; the fingerprint is the v1.0 recipe's.

## PAPER I, version Gh — the structural pass (levers 2 and 3), 14 Oct afternoon
`paper1_addressability_limit_vGh.tex` / `.pdf`: 13 pages of body, references ending on page 14, from 23 (vG) and 17
(Gf layout only). Produced by `build/make_gh.py` from the vG source by slicing at section markers with every
anchor asserted; nothing retyped. What moved: coarse packing converse and scale invariance stated first, the balloon
and both separations as one corollary with a four-line proof, rigidity of exact saturation into §3 beside them; the
four-point section folded into the hyperbolic section as §5.1; Appendix A's boxed lines to the end of §1; Appendix
B replaced by a "Formal verification" paragraph in §1 and one [Lean: name] certificate tag per theorem; §7's
disclaimers to two sentences; the firewall merged with "What is open" without its duplicate companion paragraph;
the manuscript note to three sentences. The module-by-module inventory now lives in the note (new §6, "Inventory by
module", `build/note_inventory.py`), which the verification paragraph cites. Paper I vG remains the pre-pass source;
Gh is the candidate release text and should be read once end to end before it replaces Gf.

## THE COMPLETE SET — version Gf (compiled 14 Oct 2026 06:36 CEST with Tectonic 0.15; derived from the vG sources by `build/make_gf.py`, which aborts if any replacement misses)
Refresh at 12:1x CEST (14 Oct, afternoon; all four PDFs recompiled, hashes in `GF_HASHES.txt`): **the persistent rung
closed** — `lean-modules/ActiveGeometry/Persistent.lean` (44 theorems, standard axioms, challenge file type-checks)
proves that over retentive sources a code whose addresses never move achieves `c·h_pack(2ε)`, that the persistent
capacity sits between `c·h_pack(2ε)` and `c·h_pack(ε)`, and that under bounded geometry it equals the block capacity
(via the scale-invariance theorem). Paper I: §2.4 Theorem "The persistent rung" with proof, one sentence in the ladder
paragraph, one in §9, the layer table, and an App. B row (the inventory table is now a breakable `longtable`, so the
appendix no longer overflows its page); Gh carries the theorem with its certificate tag. Note: Theorem (Lean) after the
chain, a status-table row, inventory regenerated. Paper II: one sentence in the §1 ladder item (now 17 pages). Pages:
Paper I Gf 17, Gh 14; Paper II Gf 17; note 7.
Refresh at 09:2x (layout lever only, no body sentence changed): Paper I now uses the same 1.05 in geometry as Paper II
and a 182-word abstract; 23 pages → 17 pages, overfull lines 32 → 13. The structural legibility pass (coarse converse
first, balloon as corollary, rigidity moved to §3, four-point section folded into the hyperbolic one, Appendix B to
the note, one certificate name per theorem) is planned as a separate "Gh" pass after PREREG23b.
Refresh at 09:09: `Heredity.lean` (the 25 Sep room-of-compositions theorem, 9 theorems, compiled on the pinned
library) added to the Lean set, to Paper I App. B and to Paper II §3.3; the Maynard Smith–Szathmáry framing
paragraph added to Paper II §1 with two bibliography entries; the note's status table column widths fixed.
Refresh at 06:36 after four seams named in review: the "next registration" sentences left beside the PREREG24 and
PREREG23 reports (Paper II §4.1, §4.2, §5.3), the abstract's audit and law clauses (Paper II), the four-to-five
import counts, the firewall's theorem list and the manuscript note (Paper I §1, §9), and ε′ > 2 harmonised to
ε′ ≥ 2 (strict separation) in Paper I and the note.
| document | source | PDF | pages |
|---|---|---|---|
| Paper I, *The Addressability Limit* | `paper1_addressability_limit_vGf.tex` | `paper1_addressability_limit_vGf.pdf` | 17 |
| Paper I, version Gh (structural pass, candidate release text) | `paper1_addressability_limit_vGh.tex` | `paper1_addressability_limit_vGh.pdf` | 14 |
| Paper II, *Evolution as Active Geometry* | `paper2_evolution_as_active_geometry_vGf.tex` | `paper2_evolution_as_active_geometry_vGf.pdf` | 17 |
| The mathematical note, *The Structured Addressability Limit* | `structured-addressability-note_vGf.tex` | `structured-addressability-note_vGf.pdf` | 7 |

Gf = the version-G text as of the evening of 14 October (coarse packing converse, scale-invariance theorem, the
Manning remark, Kesten–Stigum as the min form for the census reader, PREREG22–24) plus typographic fixes only: the
version line, break points after underscores in Lean identifiers, Appendix A's boxed statements on separate lines,
wider first column in the Lean inventory, ragged-bottom pages in Paper I, and the orphan page break after Paper II's
keywords removed. No sentence differs from the `vG` sources below except the version line. Remaining compile
warnings are overfull lines in prose, none in formulas or tables. SHA-256 of the six files are in `GF_HASHES.txt`.

Everything here was produced against `PLAN_CLOSURE_2026-10-14.md`; that file is the item-by-item status. The
three manuscripts are version G, edited today; none has been compiled (no TeX on this machine or biosphereatlas);
all three pass the static check `paper1/texcheck.py` (environments, refs, cites, braces).

## The three documents
- `paper1/paper1_vG.tex` — Paper I, *The Addressability Limit*, version G. New today: the ULF distinction
  (clock-ULF vs metric-ULF, §2.4); Theorem 3.x capacity-level separation over metric-ULF sources with the balloon
  proper and h_pack = log 2 machine-checked, Question 3.4 split into its answered and open halves; §4 "The bridge to
  finite tapes" (the distance reader's window, both edges from the one inequality, Lean-checked); §9 open question
  2 rewritten; Appendix B inventory with the two new modules and the Window extension; abstract and layer table.
- `paper2/paper2_vG.tex` — Paper II, *Evolution as Active Geometry*, version G. New today: the one-inequality spine
  and the window as a fifth import (§1); §4 the two-bit ceiling comparison withdrawn (units) and the audit in
  information (PREREG24: chain ordered, the reading anomaly was the measure, closure fails); §5.3 the rate-tail law
  with its exact finite-L derivation, PREREG22 confirmed, PREREG23 unresolved with the resolving design stated;
  §7.2 frontier re-ranked; Appendix C rows 22–24; "On this version" updated.
- `paper1/structured-addressability-note_vG.tex` — the September note, version G: metric-ULF definition, Theorem
  capacity-level separation, status table rows closed, the question split.

## Reading order (the bridge between the two papers)
1. `paper1_addressability_limit_vG.tex` §2–§4: the bound, the min form, the ULF distinction, the capacity-level
   separation, the **coarse packing converse** (relational capacity over bounded-valence sources is bounded by
   packing entropy at every scale), **bounded geometry closes the scale gap**, the remark on Manning's inequality
   (one obstruction, one route), and the distance reader's window.
2. `lean-modules/ActiveGeometry/{BalloonCapacity,BalloonPacking,CoarseConverse,Window}.lean`: the same statements
   machine-checked, in that order; `axcheck/` prints their axioms; `Challenges/` holds the statements with every
   proof removed.
3. `paper1-work-in-progress/structured-addressability-note_vG.tex`: the four-page mathematical brief with the status
   table (every row now Lean except Skenderi's equality).
4. `paper2_evolution_as_active_geometry_vG.tex` §1 (the one inequality and the five imports), §3–§5 (the window, the
   audit, the rate-tail law), §5.4 (Kesten–Stigum as the min form for the census reader), §7 (frontier), App. C.
5. `paper2-work-in-progress/RATE_TAIL_DERIVATION.md` and `results-2026-10-14/` for the three tests of 14 October.

## Lean (`lean-modules/`, compiled on biosphereatlas against the pinned library; zero sorry; standard axioms)
`ActiveGeometry/Persistent.lean` (44 theorems, 14 Oct afternoon: the persistent rung — nested addresses that never
move achieve `c·h_pack(2ε)` over retentive sources and the full block rate under bounded geometry; Paper I §2.4 Thm
"The persistent rung"), `ActiveGeometry/BalloonCapacity.lean` (10 theorems), `ActiveGeometry/BalloonPacking.lean` (21),
`ActiveGeometry/CoarseConverse.lean` (8: the coarse packing converse, the balloon's coarse entropy zero, the
scale-invariance theorem under bounded geometry), `ActiveGeometry/Window.lean` (extended, 19), plus AuditFactors
and Rigidity from 9 Oct; axiom-check files in `axcheck/`; challenge modules and job JSONs in `Challenges/`
(type-checked); `INTEGRATION.md` and `INTEGRATION_ADDENDUM_2026-10-14.md` say how they go into
`sentry-bio/addressability-limit`. `/fast/scratch_lean2` on biosphereatlas still holds the build (11 GB) — delete
after your Lean review.

## What is NOT in this folder
- The experiment folders with data and scripts (`horizon22/`, `horizon23/work`, `closure/`, `gate-kegg/`, `testB/`,
  `exp1-composition/`, `horizon21/`) live in the worktree `~/.claude/worktrees/theory-oct8/` (uncommitted) and, for
  the 9 Oct state, in `~/Documents/addressability-theory-2026-10-09-recovered/`; only registrations, results and
  logs are copied here.
- The intMEMOIR and GTDB-derived data (licence/size); the Lean build itself (biosphereatlas scratch).
- The repository `sentry-bio/addressability-limit` is unchanged: nothing here has been committed anywhere.
- Compiled PDFs of the version-G manuscripts (no TeX on this machine).

## Registered record (`registrations/`, index in its README)
PREREG00–24 with results. Today's three, all registered before data, amendments dated inside each file:
- 22 two-reader rate-spectrum horizon (synthetic): LAW CONFIRMED IN SIMULATION, V1–V5.
- 23 rate-class test on GTDB r232 bac120: NOT SUPPORTED AS REGISTERED (every cell unresolved; readings: recovery
  rises with L at every depth; ~25% floor; rate-weighted = shuffled control at α = 1.74); resolving design stated.
- 24 the audit in mutual information (intMEMOIR, both splits): NOT AS REGISTERED (MI1, MI2, MI4 pass; MI3 closure
  fails: observed model-critic information negative on every generation).
Supporting derivation: `paper2/RATE_TAIL_DERIVATION.md`. Run logs with clock times and hashes: `horizon22/run.log`,
`horizon23/run.log`, `closure/mi/run.log`.

## Known gaps (named, not hidden)
- Neither paper compiled; expect only cosmetic TeX fixes. Paper II cites in prose, so 25 bibitems are uncited by `\cite`.
- The persistent rung (Paper I §2.4) is closed under bounded geometry and pinned to the scale gap elsewhere (14 Oct afternoon).
- The doc tabs ("The theory on one page", "Path to publication") still carry the pre-review status row and Statement II.
- No memory note could be saved from this worktree session about the machine's memory limit (8.6 GB; cap IQ-TREE
  with `-mem`); please keep that in mind for heavy jobs.

## Data and licences
intMEMOIR analysed in place (`closure/intmemoir`, not redistributed, exclude from commits); GTDB raw downloads
deleted after PREREG23 (hashes logged), derived subsample in `horizon23/work/` (CC BY-SA 4.0); also exclude
`gate-kegg/kegg_profiles_868.npz` and `reference_manifest.csv` from any commit.
