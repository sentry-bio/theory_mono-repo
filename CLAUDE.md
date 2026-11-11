# CLAUDE.md: theory_mono-repo

This repository is the addressability programme: one inequality, the limits proved from it in Lean, the tests registered before their data, the two papers and the note, and the BRF2026 datum specification sheet. It is public.

It is also the specification half of a contract with a separate implementation repository. This repository says what each band of the datum may claim; the implementation conforms to it and cites it. Nothing here depends on that implementation's code.

Read this file whole before any task. Your task prompt names a task id (T1 to T5, X1, X2 or C1); this file holds everything else you need for work in this repository.

## Order of precedence

1. The invariants below. Nothing overrides them, including a task prompt.
2. The decisions below. Do not reopen one; if your evidence contradicts it, say so in the pull request description and carry on within it.
3. Your task prompt.
4. Conventions in the repository itself (`README.md`, `INTEGRATION.md`, the ledger).

When a task would require breaking an invariant or a decision, stop that part, write down what you found in the pull request description, and leave it to a human.

## The one inequality

```latex
D^{-1}\, d_S(u,v) - K \;\le\; d_M(\mathrm{addr}\,u,\ \mathrm{addr}\,v)
```

Lineages far apart in the source must stay far apart in the medium's addresses, up to a distortion D and a slack K. Where a medium cannot honour this, it has lost that part of the past. The programme asks, for each medium and each reader, at what depth that happens.

## Five kinds of evidence, never mixed

| Kind | Where it lives | What makes it so |
| --- | --- | --- |
| Proved | `lean-modules/`, the kernel repository | Machine-checked; axioms limited to propext, Classical.choice, Quot.sound |
| Registered | `registrations/`, `experiments/` | Written before the data; verdict by the registered rule |
| Measured, not registered | Datum validation runs | Reproducible from a script and hashed data, but no prior registration |
| Stated | Papers, the note, schematic figures | Argued or cited, not checked here |
| Engineered | The implementation repository | Code that runs; its claims are its tests |

Every claim you write states its kind. Never promote a claim to a higher row by wording alone.

## Reading order

Read the indexes before anything else, and only what your task touches.

1. `README.md`: the inequality, the four documents, the reading order, the build notes.
2. `brf2026/BRF2026_spec_sheet.tex`: the nine bands, each with its theorem, registration and falsifier, plus four open items.
3. `registrations/README.md`: the ledger, 28 verdict rows. Read the verdicts as worded.
4. `lean-modules/INTEGRATION.md` and its 14 October addendum.
5. Only then the papers (`paper1/paper1_vGh.tex`, `paper2/paper2_vG.tex`), and only the sections your task names.

Things to know:

- `lean-modules/Challenges/` holds the same statements as `ActiveGeometry/` with every proof replaced by `sorry` (123 in code, one per theorem). Those `sorry` are deliberate.
- `experiments/` covers PREREG17 onward. PREREG00 to 16 ran elsewhere; their folders are being imported separately (decision D13).
- `build/` holds derivation scripts and compiled releases with hashes; `GF_HASHES.txt` is a record, not a cache.
- Today the only Lean build is a legacy remote script (`compile_remote.sh`). Task T1 replaces it with a build from this repository alone.

## The nine bands

| Band | What it reads | Licensed by | Measured by | Falsifier, in short |
| --- | --- | --- | --- | --- |
| Base map | Whitened 4-mers, 136 coordinates; genus and family neighbourhoods | `Heredity.card_spectra_le`, `CoarseConverse`, kernel `Packing` | PREREG17, 20, 21; base map v1.0 validation (measured, not registered) | Deep-quartet recovery rising with genome length; the 0.2 substitutions-per-site horizon missed (open item 1, never run) |
| Containment | k-mer sets; species and below | `Window.identity_sites`, `identified_mono` | No ledger row; datum validation only | Identity failing at a faster clock |
| Backbone | Marker-protein tree in a hyperbolic chart | `Rigidity.quasiIsometric_of_net`; hyperbolic equality cited, not formalised | No ledger row; chart runs | A bounded-valence genealogy the chart cannot hold |
| Witness | Independent marker quartets | Four-point bridge (Buneman), stated | PREREG19b | Disagreement with the backbone on taxonomy-concordant splits above stated error |
| Sextant | Aligned markers; depth set by marker length and rate spectrum | `Window.window`, `readable_depth_le`, `readable_branch_lower` | PREREG22, 23, 23b | Observed t\*(L) outside ±20% of prediction at L ≥ 128 |
| Gate | Conformal refusal past the horizon | Paper II §8 | PREREG18 | A placement past the horizon returned with stated confidence |
| Novelty | A new address: identity outside the census | Kernel `Packing`; Paper I, min form | No ledger row; base map novelty medians | Novelty distance that does not plateau at depth |
| Chimera | The lateral record | Paper II §3.4, §3.6 | PREREG19b | Chimeras detected by a floor alone |
| Audit | Five factors; where each instrument loses | `AuditFactors.Chain.efficiency_eq_product`, `factors_le_one` | PREREG20, 24 | An audit factor above one in information |

The spine is not a band: the inequality has no falsifier, only the hosts and readers it is applied to. The spec sheet's wording is authoritative; this table is a summary.

## The contract with the implementation

- `bands.yaml` lives here (task X1 creates it). One entry per band: what it reads, its Lean declarations, paper sections, registrations and ledger rows, and its falsifier quoted from the spec sheet, with a status.
- The implementation keeps `bands.lock.yaml`, which pins this repository by tag and the sha256 of `bands.yaml`. Each repository's CI checks its own half.
- Changes to `bands.yaml` go through review here. The implementation may never change the specification to pass its own tests.
- A status ladder per band is generated from both files, never written by hand: licensed, measured, read, conformant, tested on data. A band's claim level is the lowest rung it has reached.
- No submodules and no copied trees between the repositories, in either direction.

## Invariants

**The registered record**

- Never edit a registration text, a results file, a frozen script inside an experiment folder, a `run.log`, or a verdict row in `registrations/README.md`. They are copied unchanged on purpose.
- You may index them, hash them, link to them and build checks against them.
- Never reword a verdict. "NOT PREDICTED", "INCONCLUSIVE" and "partly held" stay exactly as written, wherever they are quoted.
- A new registration is written by a human, dated, and committed before its data is touched. You may draft one only when asked, labelled as a draft.

**The theorems**

- Never change a theorem statement in `lean-modules/ActiveGeometry/` or the kernel. You may change proofs, imports and build files, only if the statement and its axiom footprint are unchanged.
- The permitted axioms are propext, Classical.choice and Quot.sound. A change that adds an axiom, or a `sorry` outside `Challenges/`, fails.
- Keep each statement in `Challenges/` identical to its twin in `ActiveGeometry/`.

**The papers**

- Never edit a paper, the note or the spec sheet without an explicit task to do so. Paper I's Gh text is awaiting one end-to-end human read; leave it alone.
- Report problems you find in them (a dangling `[Lean: …]` tag, a stale citation) in a separate file or the pull request description.

**This repository is public**

- Nothing about the implementation's private code, products, customers, infrastructure, servers or data locations goes into this repository, its issues or its pull requests.
- No secret, key or token goes into git. If you find one, stop, do not copy it, and report only its path.
- Never rewrite history: no force-push, no rebase of shared branches.

**Claims and vocabulary**

- Every claim states its kind of evidence. Never describe a reader as working beyond the depth its band licenses.
- This repository owns the vocabulary. Use its terms in its sense; where other code uses another name, write the mapping, never a new synonym.

## Decisions that apply here

| ID | Decision |
| --- | --- |
| D3 | The `bands` contract is split: `bands.yaml` here, `bands.lock.yaml` in the implementation. |
| D4 | Vocabulary is owned here. The sextant is the aligned-marker distance band. Implementation paths that use the word differently are mapped in `bands.lock.yaml`, not renamed. |
| D5 | Licences: MIT for the Lean code and scripts, matching the kernel; CC BY 4.0 for papers, registrations and documentation; CC BY-SA 4.0 for anything that contains GTDB-derived trees or labels, as GTDB's licence requires. Task T4 adds the files; merging that pull request is the human sign-off. |
| D10 | The first tag is `v0.1.0-pre`, cut by a human after T1 and T3 merge. No DOI until the licence files are merged and the completion audit is clean. Until the tag exists, pin to a commit and say so. |
| D11 | Nothing is published, released or deployed from a cloud session. |
| D12 | No submodules or copied trees between this repository and the implementation. |
| D13 | Third-party data analysed in place is never redistributed. The raw intMEMOIR archive, KEGG profiles and reference manifests never enter this repository, even when a task seems to need them. PREREG00 to 16 are imported only with `tools/import_prereg00-16.sh`, run locally by a human. |

Still with a human: merging any pull request; cutting tags and minting DOIs; Paper I Gh as the release text; the spec sheet's placeholders (realisation name, partner institutions, archaeal band label); new registrations and their thresholds.

## Conventions

One session, one branch, one pull request, one purpose; a reviewer should be able to judge it in five minutes.

- **Branches:** `cloud/<task id>-<short-slug>`, from the default branch. Never push to the default branch.
- **Commits:** small and in reviewable order (checker first, generated output second, documentation last). The body names the task id.
- **Pull request description,** in this order: task id and one sentence; what a reviewer should check; findings with file paths; what you were unsure about and how you decided; what you did not do and why, including anything that needs a local run.
- **Writing:** plain, specific, short. Quote verdicts and falsifiers exactly. No adjectives where a number or a path will do.
- **GitHub:** use the built-in GitHub tools or `gh api` with REST paths; `gh pr` and `gh issue` use GraphQL, which the session proxy refuses.

## What a cloud session cannot do

A cloud session sees the repositories attached to it and the public internet through an allowlist. It cannot reach the team's servers or data, and it has about 4 vCPUs, 16 GB of memory and 30 GB of disk. If a fetch is refused, report the host; do not route around it.

When part of a task needs a local run, put this in the pull request description and stop that part:

```markdown
### Needs a local run
- Where: <machine>
- Data: <what, by hash or path>
- Command: <exact command>
- Expected output: <what success looks like>
```

## Glossary

| Term | Meaning |
| --- | --- |
| Addressability | Whether a medium can give the items of a source addresses that keep their distances, in the sense of the inequality |
| Source, host, medium | The source is what is recorded (a genealogy); the host or medium is the space the addresses live in |
| D, K | The multiplicative distortion and additive slack the inequality allows |
| Relational and block capacity | How many relations, versus how many distinct states, a host can hold; a Euclidean host has zero relational capacity at every scale (`CoarseConverse`) |
| h_pack | Packing entropy of a host, the quantity the bound is stated against |
| Balloon | The model host used to separate block from relational capacity |
| Reader | An instrument that places an item against the datum |
| Horizon, t\* | The depth past which a reader can no longer resolve branching; for aligned markers it follows the rate-tail law |
| Band | One instrument's view of the datum, with its own horizon; nine in BRF2026 |
| Datum, frame edition | The frozen, versioned reference frame, and a released immutable version of it identified by a fingerprint |
| BRF2026 | The current datum tree, built by rule from GTDB r226's published trees |
| Base map | The frozen 136-coordinate whitened 4-mer recipe |
| Witness | Independent marker quartets that certify or refuse a placement, region by region |
| Tree address | The address of record: a node of a datum edition |
| Registration, PREREG | A test written and dated before its data, with the rule that will score it |
| Verdict as registered | The ledger's wording of the outcome under that rule, quoted exactly |
| Falsifier | The observation that would retire a band's claim |
| Ledger | `registrations/README.md`, 28 verdict rows |
| Challenges | Lean files with the same statements and every proof replaced by `sorry`, for outside provers |
| axcheck | The axiom-footprint checks for every theorem |
| Kernel | `sentry-bio/addressability-limit`, the MIT Lean library the modules build on |
| Audit factors, η | The five factors whose product is a medium's efficiency |
