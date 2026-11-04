# theory_mono-repo

The canonical record of one theory, written as four documents that share a single inequality, and of the
reference frame it licenses. Everything here is either a theorem (machine-checked in Lean 4 where the kernel
reaches, cited where it does not), a registered measurement (registration dated before its data, verdict scored
by the registered rule, readings kept separate), or a named open question. Nothing else ships.

**Authors.** Rohit Fenn and Amit Fenn (Sentry Bio). Snapshot of 14 October 2026.

## The one inequality

Histories that are far apart must stay far apart in the record:

    D⁻¹ · d_S(u, v) − K  ≤  d_M(addr u, addr v)

At the distance of sisters this is the resolution condition that gives *identity*; at the distance of deep cousins
it is the condition that keeps *genealogy*. Paper I asks which hosts honour it at exponential census rate and proves
the ceiling `β ≤ C_𝒜 ≤ C_block = c · h_pack` with its separations. Paper II asks how long a random writer honours it
on a finite tape and what a reader can recover, and measures the answer under pre-registration. The note is the
mathematical brief that states exactly what is proved. The BRF2026 datum specification sheet is where the three
meet an artefact: every band of the Biosphere Reference Frame carries the theorem that licenses it, the registration
that measured it, and the observation that would falsify it.

## The four documents

| Document | What it is | Evidentiary standard | Source | Compiled |
|---|---|---|---|---|
| **Paper I**, *The Addressability Limit* | What a medium can hold: the packing converse, the block identity, the admissibility ladder (block, persistent, causal, relational), the balloon separation, the coarse packing converse, bounded geometry and scale invariance, the hyperbolic equality, rigidity of exact saturation, the distance reader's window | Unconditional theorems; Lean certificate per theorem | `paper1/paper1_vG.tex` (pre-pass source), `paper1/paper1_vGh.tex` (structural pass, candidate release text) | `build/Gf/paper1_addressability_limit_vGf.pdf` (17 pp), `build/Gh/paper1_addressability_limit_vGh.pdf` (14 pp) |
| **Paper II**, *Evolution as Active Geometry: Descent Under the Addressability Limit* | What a lineage keeps: the window, the audit in five factors, the rate-tail law, the genealogy horizon, the registered record | Registered measurements, PREREG00–25; imports five objects from Paper I and re-derives none | `paper2/paper2_vG.tex`, `paper2/RATE_TAIL_DERIVATION.md` | `build/Gf/paper2_evolution_as_active_geometry_vGf.pdf` (17 pp) |
| **The note**, *The Structured Addressability Limit* | The mathematical brief: definitions, the three stacked facts, the persistent rung, the separations, a status table of what is and is not established, the Lean inventory by module | Theorems with Lean status per row | `paper1/structured-addressability-note_vG.tex` | `build/Gf/structured-addressability-note_vGf.pdf` (7 pp) |
| **BRF2026 datum specification sheet**, draft 0.1 | One row per component of the reference frame (base map, containment, backbone, witness, sextant, gate, novelty, chimera, audit): band claimed, licensing theorem or Lean declaration, registration and number, falsifier; the open items; the realisation rule | Inherits the standards above; re-issued with every realisation | `brf2026/BRF2026_spec_sheet.tex` | `brf2026/BRF2026_spec_sheet.pdf` (2 pp) |

How they cohere: Paper I takes the supremum over codes, Paper II studies the code nature runs, the note states the
mathematics without the biology, and the spec sheet says which theorem and which registration stand behind each
band of the datum. A sentence in any of them should trace to a theorem in `lean-modules/` or the kernel, or to a row
of `registrations/README.md`.

## Map of the repository

```
paper1/           Paper I sources (vG, vGh) and the note; texcheck.py (static checks); archive/ (v2 and the additions)
paper2/           Paper II source; the rate-tail derivation; archive/ (the v4 experiments-and-mathematics draft)
build/            make_gf.py (typographic pass), make_gh.py (structural pass), note_inventory.py, replace_abstract.py;
                  Gf/ and Gh/ hold the compiled sources and PDFs with GF_HASHES.txt
brf2026/          The datum specification sheet
lean-modules/     Lean 4 modules added to the kernel sentry-bio/addressability-limit (ActiveGeometry/), challenge files
                  and job JSONs (Challenges/), axiom checks (axcheck/), INTEGRATION.md and its 14 Oct addendum
registrations/    The ledger: every registration PREREG00–25 with results, index in README.md
experiments/      One folder per experiment: registration, frozen scripts, run.log with clock times and hashes, results
docs/             The closure plan, the package notes of 14 Oct, the status note of 9 Oct
```

## Reading order

1. `brf2026/BRF2026_spec_sheet.pdf` — two pages: what the datum is and what stands behind each band.
2. Paper I (`build/Gh/…vGh.pdf`) §1–§4: the bound, the min form, the ladder with the persistent rung, the coarse
   packing converse, bounded geometry, the balloon as a corollary, the window.
3. The note's status table (§ "What is and is not established") and its inventory by module.
4. Paper II §1 (the one inequality and the five imports), §3–§5 (window, audit, rate-tail law), §7 (frontier),
   Appendix C (the registered record).
5. `registrations/README.md`, then any experiment folder.

## Lean

The kernel lives in `sentry-bio/addressability-limit`. The modules here (`BalloonCapacity`, `BalloonPacking`,
`CoarseConverse`, `Persistent`, `Heredity`, the `Window` extension, `AuditFactors`, `Rigidity`) were compiled against
that repository's pinned library (Lean 4.34.0-rc1, Mathlib as pinned) with every theorem on `propext`,
`Classical.choice`, `Quot.sound` and no `sorry`; the axiom-check files and logs are in `lean-modules/axcheck/`. Each
module ships a challenge file (the same statements with every proof replaced by `sorry`, type-checked) and a job JSON
naming theorems, definitions and permitted axioms. `lean-modules/INTEGRATION.md` and the addendum say how they go
into the kernel.

## The registered record

Every registration was written before its data were read; amendments are dated inside each file and precede the
data they concern; smoke tests are disclosed; one verdict per claim, scored by the registered rule; readings are
reported beside the verdict, never in its place. Clock times come from `date` and the run logs. The index with
every verdict is `registrations/README.md`.

The record is tamper-evident: `registrations/RECORD_HASHES.tsv` lists the sha256 and size of every file under
`registrations/` and of every registration, frozen script, log and results file under `experiments/`, and the
`record-check` workflow fails if a listed file changes or disappears, if a record file is not listed, or if a listed
row is altered relative to the base branch. New files are listed with `tools/record_hashes.py build`, which refuses
to run if a listed file has changed. `registrations/record_index.tsv`, generated by `tools/record_index.py` from the
ledger, gives for each ledger row its date, registration id, verdict as worded, registration and results files,
folder of record and whether that folder is in this repository.

## Building

The manuscripts compile with Tectonic 0.15 (`tectonic -X compile <file>.tex`). `build/make_gf.py` derives the Gf
sources from the vG sources (typographic fixes only; it aborts if any replacement misses); `build/make_gh.py` derives
Paper I's structural pass; `build/note_inventory.py` regenerates the note's inventory section from Paper I's
appendix table. `paper1/texcheck.py` is the static check (environments, refs, cites, braces).

## Data not in this repository

Public data are fetched by the scripts and are not redistributed here: GTDB (r220/r232 trees, taxonomy and marker
alignments, CC BY-SA 4.0), NCBI RefSeq mitochondrial genomes (public domain), KEGG pathway profiles, and the
intMEMOIR processed data (raphael-group, no licence stated; analysed in place). Compiled binaries (IQ-TREE 2.4.0)
and derived alignments are excluded; each experiment's `run.log` carries the hashes of what was used. The Biosphere
Atlas base map v1.0 (186,527 genomes, recipe fingerprint `3b92fc2b…`) is referenced, not stored. See
`experiments/README.md`.

## Status, 15 October 2026

- PREREG23b (the rate-tail law on vertebrate mitogenomes) reported on the evening of 14 October: NOT SUPPORTED AS
  REGISTERED (the registered truth-set rule's second clause was unsatisfiable by construction; recorded as a dated
  amendment before any reader result); readings: the parameter-free finite-length prediction holds within 0.025 at
  every tape length up to 512 for every reader; across the two real alignments the rate-weighted reader's gain is
  absent where the spectrum is flat (α = 1.74) and present, of the predicted and growing size, where it has a slow
  tail (a = 0.43), and absent under shuffled weights; the full-length shortfall below prediction is a function of
  the reader (0.19 → 0.14 → 0.12 → 0.09 across the four readers) and sits on short internal edges, a bias that more
  sequence does not average away (`experiments/horizon23b/RESULTS_PREREG23b.md`, readings 6–7 post hoc and dated;
  ledger row 25). The depth exponents remain untested; the third design is Paper II §7.2 item (1).
- Paper II (15 October): the PREREG23b readings folded into §5.3 with the shortfall table, §7.2 and Appendix C;
  the three-lever pass run to the extent the paper needed it (abstract and version note cut, three paragraphs
  compressed, ledger as a breakable table, bibliography coherence); 17 pages. The pre-pass source is kept in
  `paper2/archive/`.
- Paper I version Gh is the candidate release text pending one end-to-end read; Gf is the pre-pass text.
- The spec sheet needs the realisation name, the partner institutions and the archaeal band label.
- Open mathematically: the clock-ULF separation question, the best-reader window, the hyperbolic equality's
  formalisation (Skenderi), and the persistent rung outside bounded geometry (pinned to the scale gap).
