"""Write <Module>Ax.lean: the module followed by `#print axioms` for every theorem it declares."""
import re, sys, pathlib

src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
text = src.read_text()
ns = re.search(r"^namespace ([\w.]+)", text, re.M).group(1)
names = re.findall(r"^theorem ([\w'.]+)", text, re.M)
dst.write_text(text + "\n" + "\n".join(f"#print axioms {ns}.{n}" for n in names) + "\n")
print(dst, len(names), "theorems")
