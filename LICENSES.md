# Licences in this repository

Decision D5 (CLAUDE.md): MIT for the Lean code and scripts, matching the kernel; CC BY 4.0 for the papers,
registrations and documentation; CC BY-SA 4.0 for anything that contains GTDB-derived trees or labels, as GTDB's
licence requires. This file maps every top-level directory and root file to its licence. Merging the pull request
that added these files is the human sign-off (D5).

The three licence texts are at the root:

| File | Licence | SPDX identifier |
|---|---|---|
| `LICENSE` | MIT License | `MIT` |
| `LICENSE-docs` | Creative Commons Attribution 4.0 International | `CC-BY-4.0` |
| `LICENSE-sa` | Creative Commons Attribution-ShareAlike 4.0 International | `CC-BY-SA-4.0` |

## By top-level directory

The rule inside a directory that holds more than one kind of file: code (`.lean`, `.py`, `.sh`, `.toml`, `.json`
job files, workflows) is MIT; prose, registrations, results and compiled papers are CC BY 4.0; any file that
contains a GTDB-derived tree or GTDB-derived taxonomy labels is CC BY-SA 4.0, whatever its type.

| Path | Licence | Notes |
|---|---|---|
| `lean-modules/` | MIT | Lean modules (`ActiveGeometry/`, `Challenges/`, `axcheck/`), the challenge job JSONs, the build and check scripts, `INTEGRATION.md` and its addendum. The modules extend the kernel `sentry-bio/addressability-limit`, whose licence is stated as MIT in CLAUDE.md (D5); this repository does not carry a copy of the kernel. |
| `build/*.py` | MIT | `make_gf.py`, `make_gh.py`, `note_inventory.py`, `replace_abstract.py`. |
| `build/Gf/`, `build/Gh/` | CC BY 4.0 | Compiled sources and PDFs of Paper I, Paper II and the note; `GF_HASHES.txt` is a record of their hashes. |
| `paper1/` | CC BY 4.0 | Paper I sources (vG, vGh), the note, `archive/`. Exception: `paper1/texcheck.py` and `paper1/archive/apply_additions.py` are scripts, MIT. |
| `paper2/` | CC BY 4.0 | Paper II source, `RATE_TAIL_DERIVATION.md`, `archive/`. Paper II cites GTDB but contains no GTDB-derived tree or label. |
| `brf2026/` | CC BY 4.0 | The BRF2026 datum specification sheet, source and PDF. It names the base map's recipe fingerprint and GTDB-derived validation numbers but carries no GTDB tree or taxonomy label. |
| `registrations/` | CC BY 4.0 | The ledger and the copies of every registration and results file. Exception, CC BY-SA 4.0: `RESULTS_PREREG21.md` (a table of GTDB r220 bacterial families with their measured horizons). See "Files that carry GTDB-derived labels" below for two borderline registration texts. |
| `experiments/` | mixed, by file | Frozen scripts (`.py`, `.sh`): MIT. Registrations, `RESULTS_*.md`, `run.log`, `.out` logs and results JSON: CC BY 4.0. The GTDB-derived files listed below: CC BY-SA 4.0. `experiments/openai-math-lean/` is unresolved; see below. |
| `docs/` | CC BY 4.0 | The closure plan, the package notes, the status note, the release checklist. |
| `.github/` | MIT | Workflow files (added by tasks T1 and T3). |
| `tools/` | MIT | Record-hash and index scripts (added by task T3). |
| `README.md`, `CLAUDE.md`, `LICENSES.md`, `CITATION.cff`, `.zenodo.json`, `.gitignore` | CC BY 4.0 | Documentation and metadata. |

## Files that carry GTDB-derived trees or labels (CC BY-SA 4.0)

GTDB's data are released under CC BY-SA 4.0. The following tracked files contain trees pruned from GTDB release
trees, GTDB genome accessions, or tables keyed by GTDB taxonomy labels, and are therefore CC BY-SA 4.0:

| Path | What it contains |
|---|---|
| `experiments/horizon23/work/` (every file: `pruned.nwk`, `iq.treefile`, `iq.iqtree`, `iq.log`, `iq.rate`, `iq.ckp.gz`, `quartets.json`, `quartets_codetest.json`, `reads.json`, `pred23.json`, `tstar.json`, `smoke23*.json`, `sub_cols.json`, `prep_summary.json`) | A 1,500-taxon subtree pruned from the GTDB r232 bac120 reference tree, the IQ-TREE re-estimate of it, and quartets and reads keyed by GTDB accessions (`GB_GCA_…`, `RS_GCF_…`). The subsample alignment `work/sub.faa` is excluded from the repository (`.gitignore`). |
| `experiments/horizon21/horizon21_bac.json`, `horizon21_bac_smoke.json`, `horizon21_ar.json`, `run_bac.out`, `run_ar.out`, `smoke.out`, `RESULTS_PREREG21.md` | Per-family results keyed by GTDB r220 family and genus labels. |
| `experiments/closure/atlas/closure_atlas_bac.json`, `closure_atlas_bac_smoke.json`, `closure_atlas_ar.json`, `closure_atlas_bac.log`, `closure_atlas_bac_smoke.log`, `closure_atlas_ar.log`, `run_bac.out`, `run_ar.out`, `smoke.out` | Per-genus results keyed by GTDB r220 family and genus labels. |
| `registrations/RESULTS_PREREG21.md` | Copy of the horizon21 results file. |

Borderline, listed for a human decision rather than guessed (see the pull request that added this file):
`registrations/PREREG11_drop.md` and `registrations/PREREG12_clock.md` name a few bacterial families as examples in
registration prose; `experiments/horizon23/RESULTS_PREREG23.md` and `registrations/RESULTS_PREREG23.md` report on
the GTDB r232 run without quoting accessions or labels.

## Not resolved here

| Path | Why |
|---|---|
| `experiments/openai-math-lean/` | Lean comparator statements in the `OAI` namespace shaped after the openai/math challenge families, with a `README.md` that is the leanprover/comparator repository's own README. The provenance and licence of the statements and of the README are not stated in the repository; the folder is reference material, not a registration (`experiments/README.md`). Left unlicensed until a human decides. |

## Data that are not in this repository

Third-party data analysed in place are never redistributed (D13): GTDB trees, taxonomy and marker alignments
(CC BY-SA 4.0), NCBI RefSeq mitochondrial genomes (public domain), KEGG pathway profiles, and the intMEMOIR
processed data (no licence stated). `README.md`, "Data not in this repository", and `experiments/README.md` say
what each experiment fetched and what each `run.log` hashes.
