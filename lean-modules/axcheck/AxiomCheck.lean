/-
  Axiom check for every module in ActiveGeometryModules
  ====================================================

  Imports the proved modules and, for every declaration they introduce, collects the axioms
  it depends on. Prints one line per theorem in the form the legacy `<Module>Ax.lean` files
  printed, then fails (a Lean error, so a non-zero exit) if any declaration of any kind
  depends on an axiom outside the permitted three: `propext`, `Classical.choice`, `Quot.sound`.

  A `sorry` is an axiom (`sorryAx`), so a `sorry` anywhere in these modules fails this check
  as well as the source check in `ci.sh`.

  Run from `lean-modules/` after `lake build`:

      lake env lean axcheck/AxiomCheck.lean

  The module list below is the same as `roots` of `ActiveGeometryModules` in `lakefile.toml`
  (the modules of ActiveGeometry/, built under their top-level names, see lakefile.toml);
  `ci.sh` checks that the two agree.
-/
import AuditFactors
import BalloonCapacity
import BalloonPacking
import CoarseConverse
import Heredity
import Persistent
import Rigidity
import Window
import Lean

namespace AxiomCheck

open Lean Elab Command

/-- The modules whose declarations are checked. -/
def checkedModules : List Name := [
  `AuditFactors,
  `BalloonCapacity,
  `BalloonPacking,
  `CoarseConverse,
  `Heredity,
  `Persistent,
  `Rigidity,
  `Window
]

/-- The axioms a declaration may depend on. -/
def permittedAxioms : List Name := [``propext, ``Classical.choice, ``Quot.sound]

/-- The declarations of one module, as stored in its `.olean`, with their kinds. -/
def moduleConstants (env : Environment) (mod : Name) : Except String (Array ConstantInfo) :=
  match env.getModuleIdx? mod with
  | none => .error s!"module {mod} is not imported"
  | some idx => .ok (env.header.moduleData[idx]!.constants)

/-- Auxiliary declarations Lean generates alongside a user declaration (`_proof_1`, `match_1`,
`_private`, equation lemmas, ...). They are checked but not printed. -/
def isAuxiliary (n : Name) : Bool :=
  n.isInternalDetail || n.isInternal

def check : CommandElabM Unit := do
  let env ← getEnv
  let mut failures : Array (Name × Array Name) := #[]
  let mut nTheorems := 0
  let mut nChecked := 0
  for mod in checkedModules do
    let consts ← match moduleConstants env mod with
      | .ok cs => pure cs
      | .error e => throwError e
    IO.println s!"== {mod}: {consts.size} declarations"
    for info in consts do
      let n := info.name
      let axioms ← collectAxioms n
      nChecked := nChecked + 1
      if info.isTheorem && !isAuxiliary n then
        nTheorems := nTheorems + 1
        IO.println s!"'{n}' depends on axioms: {axioms.toList}"
      let forbidden := axioms.filter fun a => !permittedAxioms.contains a
      if !forbidden.isEmpty then
        failures := failures.push (n, forbidden)
  IO.println s!"== checked {nChecked} declarations in {checkedModules.length} modules; \
    {nTheorems} theorems printed; permitted axioms {permittedAxioms}"
  if failures.isEmpty then
    IO.println "== AXIOM CHECK PASSED"
  else
    for (n, ax) in failures do
      IO.println s!"FORBIDDEN AXIOM: '{n}' depends on {ax.toList}"
    throwError "axiom check failed: {failures.size} declaration(s) depend on an axiom outside {permittedAxioms}"

end AxiomCheck

run_cmd AxiomCheck.check
