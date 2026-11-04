/-
  The eight modules, imported from the kernel
  ===========================================

  The default target of this package. Building it compiles the kernel's
  `ActiveGeometry.<M>` for the eight modules INTEGRATION.md and its 14 October
  addendum added there (and the kernel modules they import), at the commit
  `lakefile.toml` pins. The copies under ActiveGeometry/ in this directory are
  the record; ci.sh checks that each is byte-identical to the kernel's file.
-/
import ActiveGeometry.AuditFactors
import ActiveGeometry.BalloonCapacity
import ActiveGeometry.BalloonPacking
import ActiveGeometry.CoarseConverse
import ActiveGeometry.Heredity
import ActiveGeometry.Persistent
import ActiveGeometry.Rigidity
import ActiveGeometry.Window
