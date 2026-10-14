"""Apply PAPER_I_ADDITIONS.tex to a copy of Paper I v2 at the three anchors; write build/paper1_v2_plus.tex.
The additions file is split on its '% (n) ' markers; the bibliography items go before \\end{thebibliography}."""
import pathlib
import re

HERE = pathlib.Path(__file__).parent
src = (HERE / "build" / "paper1_v2.tex").read_text()
add = (HERE / "PAPER_I_ADDITIONS.tex").read_text()
parts = re.split(r"^% ={10,}\n% \((\d)\).*?\n(?:%.*\n)*% ={10,}\n", add, flags=re.M)
# parts: [preamble, '1', block1, '2', block2, '3', block3, '4', block4]
blocks = {parts[i]: parts[i + 1].strip("\n") for i in range(1, len(parts), 2)}

a1 = "The three quantities $\\beta,c,\\hpack$ are logically independent.\n"
assert src.count(a1) == 1, "anchor 1"
src = src.replace(a1, a1 + "\n" + blocks["1"] + "\n")

a2 = "\\noindent\\textbf{Why the boundary is special, without a dynamics.}"
assert src.count(a2) == 1, "anchor 2"
src = src.replace(a2, blocks["2"] + "\n\n" + a2)

m = re.search(r"(\\section\{Formal \(Lean\) inventory\}\n)(.*?)(\n\n|\n%)", src, flags=re.S)
assert m, "anchor 3"
src = src[: m.start(2)] + blocks["3"] + src[m.end(2):]

a4 = "\\end{thebibliography}"
assert src.count(a4) == 1, "anchor 4"
src = src.replace(a4, blocks["4"] + "\n" + a4)

out = HERE / "build" / "paper1_v2_plus.tex"
out.write_text(src)
print(out, len(src.splitlines()), "lines")
