"""Write the comparator-style challenge module of a Lean module: the same definitions and theorem statements, every
proof replaced by `sorry`, under namespace prefix `Challenges`. Usage: make_challenge.py SRC DST NewNamespace"""
import re
import sys
import pathlib

src, dst, ns_new = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
lines = src.read_text().splitlines()
ns_old = next(re.match(r"^namespace ([\w.]+)", l).group(1) for l in lines if l.startswith("namespace "))
out, i, theorems, defs = [], 0, [], []
while i < len(lines):
    l = lines[i]
    if l.startswith("theorem "):
        theorems.append(re.match(r"theorem ([\w'.]+)", l).group(1))
        # copy the statement up to the line that ends the type (`:= by`, `:= rfl`, or `:=` + term)
        while i < len(lines):
            s = lines[i]
            m = re.search(r"\s*:=\s*(by\b.*|rfl\b.*|.*)$", s)
            if m and ":=" in s and not s.lstrip().startswith("--"):
                out.append(s[: s.index(":=")].rstrip() + " := by")
                out.append("  sorry")
                i += 1
                break
            out.append(s); i += 1
        # skip the proof body: indented or blank lines until the next column-0 line
        while i < len(lines) and (lines[i] == "" or lines[i][0] in " \t"):
            i += 1
        out.append("")
        continue
    if re.match(r"^(noncomputable def|def|structure|abbrev) ", l):
        defs.append(re.match(r"^(?:noncomputable def|def|structure|abbrev) ([\w'.]+)", l).group(1))
    out.append(l); i += 1
text = "\n".join(out) + "\n"
text = text.replace(f"namespace {ns_old}", f"namespace {ns_new}").replace(f"end {ns_old}", f"end {ns_new}")
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(text)
print(dst, "theorems:", theorems, "defs:", defs)
