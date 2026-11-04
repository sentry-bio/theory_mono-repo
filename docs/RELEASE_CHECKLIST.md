# Release checklist: tag `v0.1.0-pre`

Decision D10: the first tag is `v0.1.0-pre`, cut by a human after tasks T1 and T3 merge. No DOI until the licence
files are merged and the completion audit is clean. Until the tag exists, pin to a commit and say so. Decision D11:
nothing is published, released or deployed from a cloud session. A cloud session may prepare every item below and
check it; a human runs the steps marked **human**.

The items are in the order they must be done. Each names the check that shows it is done.

## 1. Lean CI green

Task T1 adds the build from this repository alone (`lean-modules/lakefile.toml`, `lean-modules/lean-toolchain`,
`lean-modules/ci.sh`, workflow `lean` in `.github/workflows/lean.yml`).

- [ ] T1 is merged into `main`.
- [ ] The `lean` workflow is green on the commit to be tagged (not only on the pull request that merged T1).
- [ ] The run shows: every module under `lean-modules/ActiveGeometry/` builds; every theorem's axioms are exactly
      `propext`, `Classical.choice`, `Quot.sound`; no `sorry` outside `lean-modules/Challenges/`; `Challenges/`
      builds and its `sorry` count equals the twins' theorem count (125 at the 14 October snapshot).
- [ ] The kernel pin (the `rev` of `sentry-bio/addressability-limit` in `lean-modules/lakefile.toml`) is the commit
      the release text cites.

Local equivalent: `cd lean-modules && ./ci.sh`.

## 2. Record hashes green

Task T3 adds `registrations/RECORD_HASHES.tsv`, `registrations/record_index.tsv`, `tools/record_hashes.py`,
`tools/record_index.py` and the workflow `record-check` in `.github/workflows/record-check.yml`.

- [ ] T3 is merged into `main`.
- [ ] The `record-check` workflow is green on the commit to be tagged.
- [ ] Every registration text, results file, frozen script, `run.log` and the ledger is listed in
      `RECORD_HASHES.tsv` and matches its hash; no listed row was changed or removed since the snapshot of
      14 October 2026 (commit `e3b158c`).
- [ ] The ledger index is current (`python3 tools/record_index.py --check`).

Local equivalent: `python3 tools/record_hashes.py check && python3 tools/record_index.py --check`.

## 3. Licence files merged

Task T4 adds `LICENSE` (MIT), `LICENSE-docs` (CC BY 4.0), `LICENSE-sa` (CC BY-SA 4.0), `LICENSES.md`,
`CITATION.cff` and `.zenodo.json`. Merging that pull request is the human sign-off on the licences (D5).

- [ ] T4 is merged into `main`.
- [ ] The items `LICENSES.md` leaves to a human are decided: the copyright holder line in `LICENSE`; the two
      borderline registration texts; `experiments/openai-math-lean/`.
- [ ] `CITATION.cff` has no `TODO` left that the tag needs: `date-released` set to the tag date; ORCIDs filled or
      the TODO lines removed. (The DOI identifier stays empty until step 7.)
- [ ] `.zenodo.json` says the same as `CITATION.cff` (title, creators, version, licence note).

## 4. PDFs built from `build/`, with hashes

The compiled documents are tracked in `build/Gf/` and `build/Gh/`; `build/Gf/GF_HASHES.txt` records the SHA-256 of
the eight files (Paper I vGh source and PDF, Paper I vGf source and PDF, Paper II vGf source and PDF, the note vGf
source and PDF).

- [ ] The derivation scripts reproduce the tracked sources from the vG sources with no missed replacement:
      `python3 build/make_gf.py` and `python3 build/make_gh.py` (both abort on a miss).
- [ ] `paper1/texcheck.py` passes on each source.
- [ ] Each PDF compiles with Tectonic 0.15 (`tectonic -X compile <file>.tex`), from the tracked source, with no
      error and no undefined reference.
- [ ] The tracked PDFs match `GF_HASHES.txt`: `cd build/Gf && sha256sum -c GF_HASHES.txt` (the Gh entries name
      files in `build/Gh/`; check them from there). If a rebuild changes a PDF byte-for-byte, regenerate
      `GF_HASHES.txt` in the same commit and say so in the commit body; a Tectonic rebuild is not guaranteed
      byte-identical.
- [ ] `brf2026/BRF2026_spec_sheet.pdf` compiles from its source and its SHA-256 is recorded (it is not in
      `GF_HASHES.txt` at the 14 October snapshot; add a line for it or a hash file beside it).
- [ ] The versions named on the title pages (Paper I "Version Gh, 14 October 2026"; Paper II "Version G, October
      2026"; the sheet "Draft 0.1, 15 October 2026") are the versions the tag ships.

Not required for a `-pre` tag: Paper I's Gh text is still awaiting one end-to-end human read (CLAUDE.md). The tag
ships Gh as the candidate release text and says so in the tag message. The spec sheet's placeholders (realisation
name, partner institutions, archaeal band label) may stay open at `-pre`.

## 5. Frame fingerprint pinned

The datum the spec sheet describes is BRF2026, built by rule from GTDB r226's published trees; the base map band
rests on the Biosphere Atlas base map v1.0, recipe fingerprint `3b92fc2b…17fa`. The repository holds only the
truncated fingerprint (`README.md`, `brf2026/BRF2026_spec_sheet.tex`, `registrations/PREREG01_atlas_round1.md`); the
recipe file itself is excluded (`.gitignore`).

- [ ] The full 64-hex SHA-256 of the base map v1.0 recipe is written into the repository where the band
      specification lives (`bands.yaml` once task X1 creates it; until then, a line in `README.md` under "Data not
      in this repository"), together with the GTDB release its validation used (r220, per PREREG01) and the
      GTDB release the BRF2026 backbone is built from (r226).
- [ ] The frame edition fingerprint of the BRF2026 datum edition this tag pairs with is recorded in the same place,
      or the line says explicitly that no datum edition is paired with `v0.1.0-pre`.
- [ ] The implementation's `bands.lock.yaml` will pin this tag and the SHA-256 of `bands.yaml` (D3); that step
      belongs to the implementation repository and is not a condition of this tag.

This item needs a local run: the recipe and the datum package are on the team's machines, not in this repository
or reachable from a cloud session.

## 6. Cut the tag (**human**)

- [ ] `main` is at the commit on which steps 1 to 5 were checked; the working tree is clean.
- [ ] Completion audit: the four indexes read as the tag will ship them (`README.md`, the spec sheet, the ledger,
      `lean-modules/INTEGRATION.md` with its addendum); every claim states its kind of evidence; no verdict is
      reworded anywhere it is quoted.
- [ ] Annotated tag, from a local checkout, not from a cloud session (D11):

      ```sh
      git tag -a v0.1.0-pre -m "v0.1.0-pre: snapshot of 14 October 2026; Paper I Gh as candidate release text"
      git push origin v0.1.0-pre
      ```

- [ ] A GitHub release for the tag is optional at `-pre`; if made, its notes list the four documents with their
      hashes from `GF_HASHES.txt` and name what is still open (Paper I Gh read; spec sheet placeholders; open
      items 1 to 4 of the sheet).

## 7. After the tag

- [ ] DOI: only after the licence files are merged (step 3) and the completion audit (step 6) is clean, a human
      deposits the tagged archive (`.zenodo.json` carries the draft metadata). Then fill `identifiers` in
      `CITATION.cff` and the `doi` in `.zenodo.json` in a follow-up commit; that commit post-dates the tag and
      says so.
- [ ] Until then, anyone citing this repository pins the commit and says so (D10).
