#!/usr/bin/env python3
"""Fail if any Lean file under this directory, outside Challenges/, contains `sorry` in code.

Comments (`-- ...` and `/- ... -/`, nested) are stripped first, so the word may appear in a
docstring or a header comment. With --count, print the number of `sorry` tokens in the files
given instead of failing. Usage:

    check_sorry.py                 # scan lean-modules/, exit 1 on any sorry outside Challenges/
    check_sorry.py --count FILE..  # print "<n> FILE" per file
"""
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent


def strip_comments(text: str) -> str:
    out, i, n, depth = [], 0, len(text), 0
    while i < n:
        if depth == 0 and text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
            continue
        if text.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth > 0 and text.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth == 0:
            out.append(text[i])
        i += 1
    return "".join(out)


def count_sorry(path: pathlib.Path) -> int:
    return len(re.findall(r"\bsorry\b", strip_comments(path.read_text())))


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--count":
        for f in sys.argv[2:]:
            print(count_sorry(pathlib.Path(f)), f)
        return 0
    bad = []
    for f in sorted(HERE.rglob("*.lean")):
        rel = f.relative_to(HERE)
        if rel.parts[0] in (".lake", "Challenges"):
            continue
        k = count_sorry(f)
        if k:
            bad.append((rel, k))
    if bad:
        for rel, k in bad:
            print(f"SORRY OUTSIDE Challenges/: {rel} ({k})")
        return 1
    print("no sorry outside Challenges/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
