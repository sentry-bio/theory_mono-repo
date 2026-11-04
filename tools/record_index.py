#!/usr/bin/env python3
"""Build registrations/record_index.tsv from the ledger, registrations/README.md (task T3).

One row per ledger row, in ledger order. Columns:

    ledger_row              the "#" cell, as written
    date                    the "Date" cell, as written
    registration_id         PREREG ids named in the Registration cell; else
                            derived from the row number (05–06 -> PREREG05; PREREG06);
                            the operating-direction row maps to OPERATING_DIRECTION
    verdict_as_registered   the "Verdict as registered" cell, byte for byte
    registration_file       files in registrations/ named <id>_*
    results_files           files named RESULTS_* in registrations/ (and in the
                            folder of record when it is in this repository) whose
                            name carries the id; RESULTS_PREREG19_and_19b.md
                            carries both PREREG19 and PREREG19b
    folder_of_record        the "Folder of record" cell, as written
    in_repo                 yes if the folder of record (its first word) is a
                            directory of this repository, else no

Multiple values in one cell are joined with "; ". The ledger is read, never
written. `--check` rebuilds the index in memory and fails if the committed
file differs. Standard library only.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

LEDGER = "registrations/README.md"
INDEX = "registrations/record_index.tsv"
REG_DIR = "registrations"
COLUMNS = ("ledger_row", "date", "registration_id", "verdict_as_registered",
           "registration_file", "results_files", "folder_of_record", "in_repo")
HEADER_CELLS = ["#", "Date", "Registration", "Verdict as registered", "Folder of record"]

# Ledger rows that are not PREREG registrations, by the start of their Registration cell.
NON_PREREG = {"Operating direction": "OPERATING_DIRECTION"}

ID_RE = re.compile(r"PREREG\d+[a-z]?")


def repo_root() -> str:
    out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                         check=True, capture_output=True, text=True)
    return out.stdout.strip()


def split_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [c.strip() for c in cells]


def ledger_rows(root: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_table = False
    with open(os.path.join(root, LEDGER), encoding="utf-8") as f:
        for line in f:
            if not line.startswith("|"):
                in_table = False
                continue
            cells = split_row(line)
            if cells == HEADER_CELLS:
                in_table = True
                continue
            if not in_table:
                continue
            if all(set(c) <= set("-: ") for c in cells):
                continue  # the separator row
            if len(cells) != 5:
                sys.exit(f"{LEDGER}: ledger row has {len(cells)} cells, expected 5: {line.rstrip()}")
            rows.append(cells)
    if not rows:
        sys.exit(f"{LEDGER}: ledger table not found")
    return rows


def ids_for(row_cell: str, reg_cell: str) -> list[str]:
    named = []
    for m in ID_RE.findall(reg_cell):
        if m not in named:
            named.append(m)
    if named:
        return named
    for prefix, ident in NON_PREREG.items():
        if reg_cell.startswith(prefix):
            return [ident]
    ids: list[str] = []
    for part in re.split(r"[,/]", row_cell):
        part = part.strip()
        rng = re.fullmatch(r"(\d+)\s*[–-]\s*(\d+)", part)
        if rng:
            a, b = int(rng.group(1)), int(rng.group(2))
            ids += [f"PREREG{n:02d}" for n in range(a, b + 1)]
        elif re.fullmatch(r"\d+[a-z]?", part):
            ids.append("PREREG" + part.zfill(2))
        else:
            sys.exit(f"{LEDGER}: cannot derive a registration id from row '{row_cell}'")
    return ids


def results_ids(name: str) -> set[str]:
    """Ids a RESULTS_* file name carries: RESULTS_PREREG19_and_19b.md -> {PREREG19, PREREG19b}."""
    found = set(ID_RE.findall(name))
    for extra in re.findall(r"_and_(\d+[a-z]?)", name):
        found.add("PREREG" + extra.zfill(2))
    return found


def build(root: str) -> str:
    reg_files = sorted(os.listdir(os.path.join(root, REG_DIR)))
    lines = ["\t".join(COLUMNS)]
    referenced: set[str] = set()
    for row_cell, date, reg_cell, verdict, folder in ledger_rows(root):
        ids = ids_for(row_cell, reg_cell)
        reg_paths = []
        res_paths = []
        for ident in ids:
            for name in reg_files:
                if name.startswith(ident + "_") and not name.startswith("RESULTS_"):
                    reg_paths.append(f"{REG_DIR}/{name}")
                elif name.startswith("RESULTS_") and ident in results_ids(name):
                    res_paths.append(f"{REG_DIR}/{name}")
        folder_path = folder.split()[0] if folder.split() else ""
        in_repo = bool(folder_path) and os.path.isdir(os.path.join(root, folder_path))
        if in_repo:
            for name in sorted(os.listdir(os.path.join(root, folder_path))):
                if name.startswith("RESULTS_") and results_ids(name) & set(ids):
                    res_paths.append(f"{folder_path}/{name}")
        referenced.update(reg_paths)
        referenced.update(p for p in res_paths if p.startswith(REG_DIR + "/"))
        cells = [row_cell, date, "; ".join(ids), verdict, "; ".join(reg_paths),
                 "; ".join(res_paths), folder, "yes" if in_repo else "no"]
        for c in cells:
            if "\t" in c or "\n" in c:
                sys.exit(f"{LEDGER}: a cell contains a tab or newline: {c!r}")
        lines.append("\t".join(cells))
    for name in reg_files:
        p = f"{REG_DIR}/{name}"
        if (name.startswith("PREREG") or name.startswith("RESULTS_")) and p not in referenced:
            print(f"note: {p} is not reached from any ledger row", file=sys.stderr)
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="fail if the committed index differs from a fresh build")
    args = ap.parse_args()
    root = repo_root()
    text = build(root)
    full = os.path.join(root, INDEX)
    if args.check:
        if not os.path.exists(full):
            print(f"{INDEX} is missing", file=sys.stderr)
            return 1
        with open(full, encoding="utf-8") as f:
            if f.read() != text:
                print(f"{INDEX} is stale: rerun tools/record_index.py", file=sys.stderr)
                return 1
        print(f"{INDEX} is up to date")
        return 0
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"{INDEX}: {text.count(chr(10)) - 1} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
