"""Replace Paper I's abstract with the short form (lever 1 of the legibility pass). Aborts unless exactly one abstract."""
import pathlib, re, sys
p = pathlib.Path(__file__).resolve().parent.parent / "paper1" / "paper1_vG.tex"
t = p.read_text()
NEW = r"""\begin{abstract}
A process cannot retain distinguishable histories faster than its representation gains room to keep them apart: for retained-history growth $\beta$, radial conversion rate $c$ and host packing entropy $\hpack$, $\beta\le c\,\hpack$ in every proper metric space, with no curvature, tree or stationarity hypothesis, and the bound is attained exactly by block codes. What packing entropy does not settle is structure. Over sources with bounded metric balls, a code that preserves genealogy, not only identity, is bounded by packing entropy at \emph{every} scale, so addressing reads growth at the reader's scale and genealogy reads the quasi-isometry-invariant growth; a proper host of entropy $\log2$ with relational capacity zero exhibits the gap, and bounded geometry closes it. In real hyperbolic space relational capacity attains block capacity, $\Crel^{\mathrm{wt}}(\Hk,c;\eps)=c(n-1)\sqrt\kappa$. Exact saturation with bounded distortion forces a tree at the reader's scale; a random writer on a finite tape keeps genealogy only inside a window whose two edges are the same inequality at two depths. Efficiency against the bound is a product of five ratios whose content is an experiment. The kernel is machine-checked in Lean~4.
\end{abstract}"""
blocks = re.findall(r"\\begin\{abstract\}.*?\\end\{abstract\}", t, re.S)
if len(blocks) != 1:
    sys.exit(f"ABORT: found {len(blocks)} abstract blocks")
t = t.replace(blocks[0], NEW)
p.write_text(t)
print("abstract replaced;", len(NEW.split()), "words")
