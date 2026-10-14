"""Paper I structural pass (levers 2 and 3): vG -> vGh. Slices the vG source at section markers, reorders and
compresses, asserts every anchor matches exactly once. Writes paper1/paper1_vGh.tex and build/Gh/*.tex (typographic form).

Moves: coarse converse and scale invariance first, balloon + both separations as one corollary, rigidity into §3;
four-point section folded into the hyperbolic section; Appendix A's boxes to the end of §1; Appendix B replaced by a
verification paragraph in §1 and per-theorem certificate tags; §8 disclaimers to two sentences; firewall merged with
"What is open" without its duplicate companion paragraph; manuscript note to three sentences.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "paper1" / "paper1_vG.tex"
t = SRC.read_text()

def once(s, name):
    n = t.count(s)
    if n != 1:
        sys.exit(f"ABORT {name}: {n} matches for {s[:60]!r}")

def cut_between(start, end, name):
    """Remove text from `start` (inclusive) up to `end` (exclusive); return the removed text."""
    global t
    once(start, name + " start"); once(end, name + " end")
    i, j = t.index(start), t.index(end)
    assert i < j, name
    removed = t[i:j]
    t = t[:i] + t[j:]
    return removed

def replace(old, new, name):
    global t
    once(old, name)
    t = t.replace(old, new)

SEP = "% =====================================================================\n"

# ---- preamble: certificate tag macro
replace("\\newcommand{\\eps}{\\varepsilon}",
        "\\newcommand{\\eps}{\\varepsilon}\n\\newcommand{\\cert}[1]{{\\footnotesize\\ [\\textsc{Lean}: \\texttt{#1}]}}",
        "cert macro")

# ---- manuscript note to three sentences
i = t.index("{\\small\\noindent\\emph{On this manuscript.}"); j = t.index("\\par}", i) + len("\\par}")
t = t[:i] + ("{\\small\\noindent\\emph{On this manuscript.} This paper supersedes a Zenodo record (concept DOI "
             "\\href{https://doi.org/10.5281/zenodo.19381557}{10.5281/zenodo.19381557}) whose public face was an "
             "\\emph{equality} between curvature and entropy rate; that equality survives only as the named equality case of "
             "an inequality (\\S\\ref{sec:IIb}), and the content is now the separation between two capacities. The companion, "
             "\\emph{Evolution as Active Geometry} (Fenn \\& Fenn), instantiates the bound and ladder on genomic data under its "
             "own evidentiary standard; it is cited, not fed back into any theorem below. No biological claim appears here.\\par}") + t[j:]

# ---- §1: verification paragraph + minimal statement, placed before "Relation to existing work"
VERIF = r"""
\medskip
\noindent\textbf{Formal verification.}\label{sec:lean} A theorem tagged [\textsc{Lean}: \texttt{name}] is machine-checked in Lean~4 against Mathlib, with every declaration depending only on \texttt{propext}, \texttt{Classical.choice} and \texttt{Quot.sound}; the tag names the certifying declaration in \texttt{theory/lean/ActiveGeometry/} of the repository \texttt{sentry-bio/addressability-limit}. The module-by-module inventory, the challenge files (the same statements with every proof replaced by \texttt{sorry}) and their job files are in the companion mathematical note \cite{fennfennnote}. The geometry behind Theorem~\ref{thm:relational}'s lower bound, the representation theory of Proposition~\ref{prop:schur}, Gromov's quasi-isometry invariance, and the theorems of Manning, Katok and Besson--Courtois--Gallot are classical and cited; the Lean predicate \texttt{IsotropicHyperbolic} names a hypothesis, not a derived conclusion.

\medskip
\noindent\textbf{Minimal statement.}
\[
\boxed{\text{retained exponential novelty}\ \Longrightarrow\ \beta\le c\,\hpack}\qquad
\boxed{D_\eps(R_\tau)\le\min\bigl(|S_\tau|,P(A_\tau,\eps)\bigr)}
\]
unconditionally; separately, $\boxed{\text{A3}\ \Longrightarrow\ M=\Hk}$ by Schur, with no claim that any process satisfies A3, and $\boxed{\text{exact saturation with bounded tax}\ \Longrightarrow\ \text{tree at scale }\eps}$. The inequality is the enduring limit; the state equation $\bar\kappa^*=(\heff\ln2/(n-1))^2$ is its equality case in the isotropic host, asserted of no system here.

"""
replace("\\subsection{Relation to existing work}\\label{sec:related}",
        VERIF + "\\subsection{Relation to existing work}\\label{sec:related}", "verif+minimal")

# ---- inline certificates outside §3/§8 (those sections are rewritten below)
replace("(\\texttt{convergent\\_rate\\_addressability\\_limit}, Appendix~B)", "\\cert{convergent\\_rate\\_addressability\\_limit}", "cert bound")
replace("(\\texttt{Audit.Chain.efficiency\\_eq\\_product}, \\texttt{card\\_chain})", "\\cert{Chain.efficiency\\_eq\\_product}", "cert audit")
replace("(\\texttt{identified\\_of\\_sites})", "\\cert{identified\\_of\\_sites}", "cert ident")
replace("(\\texttt{identified\\_mono})", "\\cert{identified\\_mono}", "cert mono")
replace("(\\texttt{window})", "\\cert{window}", "cert window")
replace("(\\texttt{readable\\_depth\\_le})", "\\cert{readable\\_depth\\_le}", "cert depth")
replace("(\\texttt{readable\\_branch\\_lower})", "\\cert{readable\\_branch\\_lower}", "cert branch")
replace("(\\texttt{kestenStigum\\_iff\\_rate})", "\\cert{kestenStigum\\_iff\\_rate}", "cert ks")
replace(" Machine-checked (\\texttt{Persistent.lean}: \\texttt{achievable\\_stable\\_persistent}, \\texttt{capacity\\_stable\\_between}, \\texttt{capacity\\_stable\\_eq\\_packing\\_of\\_boundedGeometry}, Appendix~B).\n\\end{proof}\n",
        "\n\\end{proof}\\cert{capacity\\_stable\\_eq\\_packing\\_of\\_boundedGeometry}\n", "cert persistent")
replace("it remains the named hypothesis of Appendix~B.", "it remains a named hypothesis (\\texttt{ReconstructionThreshold}).", "ks hypothesis")

# ---- pull the rigidity theorem out of §8 (statement + proof + following paragraph)
RIG_START = "\\begin{theorem}[Rigidity of exact saturation]\\label{thm:rigid}"
RIG_END = "\\begin{remark}[Symmetry, and what it does not follow from]\\label{rem:symmetry}"
rig = cut_between(RIG_START, RIG_END, "rigidity block")
rig = rig.replace("The net and quasi-isometry statements are machine-checked (\\texttt{Rigidity.maximal\\_separated\\_isNet}, \\texttt{Rigidity.quasiIsometric\\_of\\_net}); the hyperbolicity conclusion is cited. In words:",
                  "In words:")
rig = rig.replace("\\end{proof}\n", "\\end{proof}\\cert{Rigidity.quasiIsometric\\_of\\_net}\n", 1)

# ---- §8: two-sentence disclaimers, pointer to the moved theorem
replace("Equality \\emph{exactly}, at every depth, with bounded relational distortion, forces the host's coarse geometry.",
        "Equality \\emph{exactly}, at every depth, with bounded relational distortion, forces the host's coarse geometry (Theorem~\\ref{thm:rigid}, \\S\\ref{sec:balloon}).", "sat pointer")
i = t.index("\\noindent\\textbf{What is \\emph{not} proved.}"); j = t.index(SEP, i)
t = t[:i] + ("\\noindent\\textbf{What is not proved, and what would test saturation.} The mismatch $V(\\kappa,\\kappa^*)=(\\sqrt\\kappa-\\sqrt{\\kappa^*})^2$ has a unique zero at $\\kappa^*$ and nothing more is claimed of it: no dynamics is supplied, so neither stability nor attraction is asserted. Saturation is tested only by an $\\eta=\\beta/(c\\,\\hpack)$ whose numerator and denominator have independent provenance; an $\\eta$ produced by fitting one axis to the other, or by back-solving $n$ or $\\kappa$ from an assumed equality, tests nothing.\n\n") + t[j:]

# ---- §5 (four-point) folded into §6
FP_START = "\\section{The structural bridge: four-point geometry}\\label{sec:classifier}"
FP_END = "\\section{Closing the gap: the hyperbolic host}\\label{sec:relational}"
cut_between(FP_START, FP_END, "four-point section")
# the separator line now precedes §6 twice; collapse
t = t.replace(SEP + SEP, SEP)
FOLD = r"""\emph{This theorem is host-specific, not Layer-I universal.} Hyperbolic space closes the gap the balloon opens, exactly.

\subsection{The four-point bridge}\label{sec:classifier}
For four points form $S_1=d(a,b)+d(c,d)$, $S_2=d(a,c)+d(b,d)$, $S_3=d(a,d)+d(b,c)$. A finite metric is an additive weighted-tree metric exactly when the two largest of $S_1,S_2,S_3$ agree for every quartet \cite{buneman1971}; in the geodesic setting, $0$-hyperbolicity is exactly the $\mathbb R$-tree condition \cite{gromov1987}. The defect $\delta$ measures departure from this: it decides whether the qualitative object is a tree, and it determines neither a curvature magnitude nor a growth class, since a metric can be tree-like by the four-point condition and still have polynomial ball growth. One structural floor follows: a genuinely branching tree cannot embed isometrically in a one-dimensional connected manifold, so $n=2$ is the minimal smooth hyperbolic ambient dimension for branching trees at low distortion, a statement about embeddability and not a fitted or curvature-derived constant. This bridge is neither Layer~I nor Layer~II; it motivates the host class and supplies no $\beta$, $c$ or curvature.

\subsection{The hyperbolic equality}
"""
replace("\\emph{This theorem is host-specific, not Layer-I universal.} Hyperbolic space closes the gap the balloon opens, exactly.\n",
        FOLD, "fold four-point")

# ---- §3 rewrite
S3_START = "\\section{The separation: addresses without genealogy}\\label{sec:balloon}"
S3_END = "\\section{The bridge to finite tapes: the window of a random writer}\\label{sec:window}"
old_s3 = cut_between(S3_START, S3_END, "section 3")
def grab(start, end, name):
    once_src = old_s3
    i = once_src.index(start); j = once_src.index(end, i + 1)
    assert i < j, name
    return once_src[i:j]
coarse = grab("\\begin{theorem}[Coarse packing converse]", "The infimum over scales", "coarse thm+proof")
coarse = coarse.replace(" Machine-checked (\\texttt{coarse\\_packing\\_converse}, Appendix~B); Theorem~\\ref{thm:sepcap} is its corollary at any $\\eps'\\ge2$, where the balloon packs one point per star and $\\hpack(B;\\eps')=0$ (\\texttt{balloon\\_coarse\\_entropy\\_zero}).", "")
coarse = coarse.replace("\\end{proof}\n", "\\end{proof}\\cert{coarse\\_packing\\_converse}\n", 1)
infimum = grab("The infimum over scales", "\\begin{theorem}[Bounded geometry closes the scale gap]", "infimum para")
scaleinv = grab("\\begin{theorem}[Bounded geometry closes the scale gap]", "So the gap of Theorem", "scaleinv thm")
scaleinv = scaleinv.replace(" (\\texttt{packingRate\\_scale\\_invariant})", "").replace("\\end{theorem}\n", "\\end{theorem}\\cert{packingRate\\_scale\\_invariant}\n", 1)
balloon_def = grab("\\begin{definition}[Balloon]", "$B$ is a ray", "balloon def")
twogaps = grab("\\begin{remark}[One obstruction, one route; Manning's inequality]", "\\begin{remark}[What the separation does and does not say]", "twogaps")
whatsays = grab("\\begin{remark}[What the separation does and does not say]", "\\begin{question}", "whatsays").replace("Theorem~\\ref{thm:sepcap}", "Corollary~\\ref{thm:sepcap}")
question = grab("\\begin{question}", "% =====", "question").replace("Theorem~\\ref{thm:sepcap}", "Corollary~\\ref{thm:sepcap}")

NEW_S3 = S3_START + "\n" + SEP + r"""
Packing entropy answers the addressing question completely and the structural one not at all. The reason is a matter of scale: block capacity reads packing entropy at the reader's scale, while a code that preserves genealogy over bounded-valence sources is held to packing entropy at \emph{every} scale. We prove that once, and read the separation off it.

""" + coarse + "\n" + scaleinv + "\n" + infimum.rstrip() + r""" So the gap of Theorem~\ref{thm:coarse} is a property of hosts without bounded geometry and of nothing else; here is one.

""" + balloon_def + r"""
$B$ is a ray with a star of $2^i$ leaves at the $i$th hub. Its closed balls are finite, so it is proper; $\hpack(B,\mathsf{hub}\,0;\eps)=\log2$ for $\eps\le1$, since the $2^m$ leaves of hub $m$ are $1$-separated inside radius $m+1$ and a ball of radius $\rho$ holds fewer than $2^{\lfloor\rho\rfloor+2}$ points; and $\hpack(B;\eps')=0$ for $\eps'\ge2$, since separation is strict and above scale $2$ a ball packs one point per star.\cert{balloon\_coarse\_entropy\_zero} The hubs have unbounded degree, so Theorem~\ref{thm:scaleinv} does not apply, and the scale gap opens. Let $\sigma_2$ be the rooted binary tree with its unit-edge clock: metric-ULF with $f(t)=2^t$ (generation-$R$ vertices within tree distance $t$ share their first $R-t$ letters), of growth $\log2$.

\begin{corollary}[Separation]\label{thm:sep}\label{thm:sepcap}
\emph{(i)} At $\eps=c=1$ the rate $\log2$ is achievable for $\sigma_2$ in $B$ at the block rung and, for every lawful distortion, not at the relational rung. \emph{(ii)} Over the family $\mathfrak S$ of metric-ULF sources, for every lawful distortion, resolution and radial rate, no source of positive growth is relationally representable in $B$: the relational rate set over $\mathfrak S$ lies in $\{0\}$. At $\eps=c=1$ the block rate set contains $\log2$ and the relational rate set contains $0$, so as numbers
\[
\Crel(B)\;=\;0\;<\;\log2\;=\;\Cblock(B).
\]
\end{corollary}

\begin{proof}
\emph{Block.} Send $\{0,1\}^R$ injectively onto the leaves of $\mathsf{hub}(R)$: distinct leaves are at distance $2\ge\eps$ inside $\bar B(\mathsf{hub}\,0,R+1)$, so $r(R)/R\to1$. \emph{Relational.} Theorem~\ref{thm:coarse} at any $\eps'\ge2$ gives $\beta\le c\,\hpack(B;\eps')=0$ for every metric-ULF source, $\sigma_2$ among them. The one-history source is relationally representable at growth $0$, and the right-hand equality is the block identity $\Cblock=c\,\hpack$ with $\hpack(B;1)=\log2$. Only the lower side of the relational sandwich is used, here and everywhere in this paper's separation.
\end{proof}\cert{balloon\_capacity\_strict}

""" + whatsays + "\n" + question + "\n" + twogaps + r"""
Exact saturation is the other rigid statement of coarse geometry, and it uses the same net.

""" + rig + SEP

t = t[:t.index(S3_END)] + NEW_S3 + t[t.index(S3_END):]
# the separator that preceded §window in the old file is now duplicated
t = t.replace(SEP + SEP, SEP)

# ---- firewall merged with "What is open", duplicate companion paragraph dropped
i = t.index("\\emph{Relation to the companion.} \\emph{Evolution as Active Geometry} needs the five licenses")
j = t.index("\\section{What is open}\\label{sec:open}")
t = t[:i] + t[j:]
replace("\\section{The firewall}\\label{sec:firewall}\n" + SEP + "\n", "", "firewall heading")
replace("\\section{What is open}\\label{sec:open}\n" + SEP + "\n",
        "\\section{The firewall, and what is open}\\label{sec:open}\\label{sec:firewall}\n" + SEP + "\n", "open heading")
# the firewall paragraph now sits before the new heading; move it after
fw_start = "Theorems~\\ref{thm:bound}, \\ref{thm:block}"
i = t.index(fw_start); j = t.index("\\section{The firewall, and what is open}")
fw = t[i:j]
t = t[:i] + t[j:]
replace("\\section{The firewall, and what is open}\\label{sec:open}\\label{sec:firewall}\n" + SEP + "\n",
        "\\section{The firewall, and what is open}\\label{sec:open}\\label{sec:firewall}\n" + SEP + "\n" + fw.strip() + "\n\n", "firewall move")
t = t.replace(SEP + "\n" + SEP, SEP)
replace("Theorems~\\ref{thm:bound}, \\ref{thm:block}, \\ref{thm:minform}, \\ref{thm:sep}, \\ref{thm:sepcap}, \\ref{thm:coarse}, \\ref{thm:scaleinv}, \\ref{thm:window}, \\ref{thm:relational}, \\ref{thm:rigid}, Proposition~\\ref{prop:identity} and Corollary~\\ref{cor:poly} are unconditional.",
        "Theorems~\\ref{thm:bound}, \\ref{thm:block}, \\ref{thm:minform}, \\ref{thm:coarse}, \\ref{thm:scaleinv}, \\ref{thm:rigid}, \\ref{thm:window} and \\ref{thm:relational}, Corollaries~\\ref{cor:poly} and~\\ref{thm:sepcap}, and Proposition~\\ref{prop:identity} are unconditional.", "firewall list")

# ---- appendices removed (A moved to §1; B replaced by the verification paragraph + tags)
i = t.index("\\clearpage\n\\appendix"); j = t.index("\\begin{thebibliography}")
t = t[:i] + t[j:]
replace("\\bibitem{skenderi2026}", "\\bibitem{fennfennnote} Fenn, R.\\ \\& Fenn, A.\\ \\emph{The Structured Addressability Limit: a note for independent review of the core mathematics}, version Gf (2026). With the Lean~4 inventory, challenge files and job files.\n\\bibitem{skenderi2026}", "note bibitem")

# ---- global reference fixes after the slicing
t = t.replace("Theorem~\\ref{thm:sepcap}", "Corollary~\\ref{thm:sepcap}").replace("Theorem~\\ref{thm:sep}", "Corollary~\\ref{thm:sep}")
replace("(\\texttt{distinguishable\\_le\\_min}, Appendix~B)", "\\cert{distinguishable\\_le\\_min}", "cert minform")
replace("\\textbf{IIb} (\\S\\ref{sec:IIb}) & Exact saturation with bounded tax forces a tree at scale $\\eps$; variational selection of the boundary;",
        "\\textbf{IIb} (\\S\\ref{sec:IIb}) & Exact saturation with bounded tax forces a tree at scale $\\eps$ (Theorem~\\ref{thm:rigid}, \\S\\ref{sec:balloon}); variational selection of the boundary;", "IIb row")
if "Appendix~B" in t:
    sys.exit("ABORT: Appendix~B still referenced")

# ---- version line
replace("\\date{Version G, October 2026}", "\\date{Version Gh, 14 October 2026}", "version")

OUT = ROOT / "paper1" / "paper1_vGh.tex"
OUT.write_text(t)
# typographic form
g = t.replace("\\documentclass[11pt,reqno]{amsart}", "\\documentclass[11pt,reqno]{amsart}\n\\raggedbottom").replace("\\_", "\\_\\allowbreak{}")
(ROOT / "build" / "Gh").mkdir(parents=True, exist_ok=True)
(ROOT / "build" / "Gh" / "paper1_addressability_limit_vGh.tex").write_text(g)
print("written", OUT, "and build/Gh; lines", t.count("\n"))
