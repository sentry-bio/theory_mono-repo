"""Move Paper I's module-by-module Lean inventory table (vG Appendix B) into the note as its own section, with
Paper I cross-references stripped. Idempotent: replaces the section if present. Writes the note vG source in place."""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
P1 = (ROOT / "paper1" / "paper1_vG.tex").read_text()
NOTE = ROOT / "paper1" / "structured-addressability-note_vG.tex"
n = NOTE.read_text()
i = P1.index("\\section{Formal (Lean) inventory}")
j = P1.index("\\end{longtable}}", i) + len("\\end{longtable}}")
blk = P1[i:j]
tab = blk[blk.index("{\\footnotesize"):]
tab = re.sub(r"\(Thm~\\ref\{[^}]*\}:\s*", "(", tab)                              # (Thm~\ref{...}: β ≤ ...) -> (β ≤ ...)
tab = tab.replace("counterpart of Theorem~\\ref{thm:coarse}", "counterpart of the coarse packing converse")
tab = re.sub(r"\s*\((?:Thm|Prop|Cor)~\\ref\{[^}]*\}[^()]*\)", "", tab)          # (Thm~\ref{...}, finite radius)
tab = tab.replace("p{3.3cm}", "p{4.3cm}").replace("p{10.4cm}", "p{10.6cm}")
tab = re.sub(r"\s*\(\\S\\ref\{[^}]*\}\)", "", tab)                                # (\S\ref{sec:window})
tab = re.sub(r"Theorem~\\ref\{[^}]*\}'s", "the hyperbolic equality's", tab)
tab = re.sub(r"\\ref\{[^}]*\}", "", tab)
tab = tab.replace("\\eps", "\\varepsilon").replace("\\Hk", "\\Hyp^n_\\kappa").replace("\\Crel", "\\Capy_{\\mathrm{rel}}").replace("\\Cblock", "\\Capy_{\\mathrm{block}}")
SEC = ("\\section{Inventory by module}\\label{sec:inventory}\n"
       "The kernel, module by module, as compiled on the pinned Mathlib (Lean 4.34.0-rc1). Every declaration depends only on\n"
       "\\texttt{propext}, \\texttt{Classical.choice}, \\texttt{Quot.sound}; each downstream module ships with a challenge file\n"
       "(the same statements with every proof replaced by \\texttt{sorry}) and a job file naming its theorems, definitions\n"
       "and permitted axioms. Paper~I cites declarations by name in its [\\textsc{Lean}: \\ldots] tags.\n\n" + tab + "\n\n")
if "\\section{Inventory by module}" in n:
    a = n.index("\\section{Inventory by module}"); b = n.index("\\section{Relation to neighbouring work}")
    n = n[:a] + SEC + n[b:]
else:
    anchor = "\\section{Relation to neighbouring work}"
    assert n.count(anchor) == 1
    n = n.replace(anchor, SEC + anchor)
if "\\ref{" in tab:
    sys.exit("ABORT: unresolved Paper I reference left in the inventory table")
NOTE.write_text(n)
print("inventory section written into the note;", tab.count("\\\\"), "table lines")
