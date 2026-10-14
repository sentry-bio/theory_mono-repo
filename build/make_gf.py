"""Derive the version-Gf sources from the vG sources: version line + typographic fixes only.

Usage (from the worktree root): python3 -I build/make_gf.py
Writes build/Gf/*.tex. Every replacement must hit exactly once (or as counted), else the script aborts.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "Gf"
OUT.mkdir(parents=True, exist_ok=True)

def apply(text, old, new, count=1, name=""):
    n = text.count(old)
    if n != count:
        sys.exit(f"ABORT {name}: expected {count} occurrence(s) of {old[:50]!r}, found {n}")
    return text.replace(old, new)

def allowbreak(text):
    return text.replace("\\_", "\\_\\allowbreak{}")

# ---- Paper I
p1 = (ROOT / "paper1" / "paper1_vG.tex").read_text()
p1 = apply(p1, "\\date{Version G, October 2026}", "\\date{Version Gf, 14 October 2026}", name="p1 version")
p1 = apply(p1, "\\documentclass[11pt,reqno]{amsart}", "\\documentclass[11pt,reqno]{amsart}\n\\raggedbottom", name="p1 raggedbottom")
p1 = apply(p1,
    "\\[\n\\boxed{\\text{retained exponential novelty}\\ \\Longrightarrow\\ \\beta\\le c\\,\\hpack,\\qquad D_\\eps(R_\\tau)\\le\\min(|S_\\tau|,P(A_\\tau,\\eps))}\n\\]\n"
    "unconditionally. Separately, $\\boxed{\\text{A3}\\ \\Longrightarrow\\ M=\\Hk}$ by Schur, with no genericity claim and no claim any process satisfies A3; and $\\boxed{\\text{exact saturation with bounded tax}\\ \\Longrightarrow\\ \\text{tree at scale }\\eps}$. Imposing in addition",
    "\\[\n\\boxed{\\text{retained exponential novelty}\\ \\Longrightarrow\\ \\beta\\le c\\,\\hpack}\\qquad\n\\boxed{D_\\eps(R_\\tau)\\le\\min\\bigl(|S_\\tau|,P(A_\\tau,\\eps)\\bigr)}\n\\]\n"
    "unconditionally. Separately,\n\\[\n\\boxed{\\text{A3}\\ \\Longrightarrow\\ M=\\Hk}\\qquad\\text{and}\\qquad\n"
    "\\boxed{\\text{exact saturation with bounded tax}\\ \\Longrightarrow\\ \\text{tree at scale }\\eps},\n\\]\n"
    "the first by Schur, with no genericity claim and no claim any process satisfies A3. Imposing in addition",
    name="p1 minimal statement")
p1 = apply(p1, "p{3.3cm}>{\\raggedright\\arraybackslash}p{10.4cm}@{}}\n\\toprule\n\\textbf{File} & \\textbf{Certifies}",
           "p{3.9cm}>{\\raggedright\\arraybackslash}p{9.7cm}@{}}\n\\toprule\n\\textbf{File} & \\textbf{Certifies}", name="p1 table widths")
p1 = allowbreak(p1)
(OUT / "paper1_addressability_limit_vGf.tex").write_text(p1)

# ---- Paper II
p2 = (ROOT / "paper2" / "paper2_vG.tex").read_text()
p2 = apply(p2, "Version G --- October 2026", "Version Gf --- 14 October 2026", name="p2 version")
p2 = apply(p2, "\\newpage\\setcounter{page}{1}", "\\bigskip", name="p2 front matter break")
p2 = allowbreak(p2)
(OUT / "paper2_evolution_as_active_geometry_vGf.tex").write_text(p2)

# ---- Note
nt = (ROOT / "paper1" / "structured-addressability-note_vG.tex").read_text()
nt = apply(nt, "\\date{}", "\\date{Version Gf, 14 October 2026}", name="note version")
nt = allowbreak(nt)
(OUT / "structured-addressability-note_vGf.tex").write_text(nt)
print("Gf sources written to", OUT)
