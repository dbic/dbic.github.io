#!/usr/bin/env python3
"""
Compare the document registry (_data/documents.csv) with what is really in the repository.

Run from the repo root:
    python check_documents.py

It reports:
  1. NOT IN THE REGISTRY  documents that pages link to but documents.csv does not list
  2. MISSING FILES        registry rows whose file does not exist in the repo (broken link)
  3. DUPLICATES           the same file listed twice, or the same id twice
  4. UNLINKED FILES       files in assets/ (other than images, css and js) that nothing links to and the registry lacks
  5. PAGE LINKS           registry rows that point at a page and that page does not exist

Exit status is 1 if there are missing files or duplicates (so it can be used in an automatic check).
"""

import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
DOC_EXTS = {"pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "csv", "txt", "zip", "jpg", "jpeg", "png", "rtf"}
DOC_EXT = "|".join(sorted(DOC_EXTS))
# any link to a file under /assets/ that is not an image folder, stylesheet or script
LINK = re.compile(r"""(?:https?://dbic\.github\.io)?(/assets/[^\s)"'<>\]#?]+\.(?:%s))""" % DOC_EXT, re.I)
SKIP_PREFIX = ("/assets/dbic/images/", "/assets/css/", "/assets/js/")
SCAN_EXT = {".md", ".html", ".csv", ".yml", ".yaml", ".markdown"}
SKIP_DIRS = {".git", "node_modules", "vendor", "_site", "__pycache__"}


def is_doc(path):
    return path.startswith("/assets/") and not path.startswith(SKIP_PREFIX)


# ---------------------------------------------------------------- the registry
reg_path = ROOT / "_data" / "documents.csv"
if not reg_path.exists():
    sys.exit(f"Cannot find {reg_path}. Run this from the repository root.")
rows = list(csv.DictReader(open(reg_path, encoding="utf-8-sig", newline="")))
registry = {}
dups = []
ids = defaultdict(list)
for r in rows:
    f = (r.get("file") or "").strip()
    if f in registry:
        dups.append(f"file listed twice: {f}")
    registry[f] = r
    ids[(r.get("id") or "").strip()].append(r.get("title"))
for i, titles in ids.items():
    if i and len(titles) > 1:
        dups.append(f"id used twice: {i} ({', '.join(titles)})")

# ---------------------------------------------------------------- what pages link to
linked = defaultdict(set)
for dp, dns, fns in os.walk(ROOT):
    dns[:] = [d for d in dns if d not in SKIP_DIRS]
    for fn in fns:
        p = Path(dp) / fn
        if p.suffix.lower() not in SCAN_EXT or p == reg_path:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in LINK.finditer(text):
            path = unquote(m.group(1))
            if is_doc(path):
                linked[path].add(p.relative_to(ROOT).as_posix())

# ---------------------------------------------------------------- checks
def exists_exact(rel):
    """True if the path exists with exactly this upper/lower case (GitHub is case-sensitive)."""
    cur = ROOT
    for part in Path(rel.lstrip("/")).parts:
        if part not in os.listdir(cur):
            return False
        cur = cur / part
    return cur.is_file()


not_in_registry = sorted(p for p in linked if p not in registry)
missing = []
page_missing = []
for f, r in registry.items():
    if f.startswith("/assets/"):
        if not exists_exact(f):
            missing.append((f, r.get("title")))
    elif f.startswith("/") and f.endswith((".html", ".htm")):
        md = ROOT / (f.lstrip("/")[:-5] + ".md")
        html = ROOT / f.lstrip("/")
        idx = ROOT / f.lstrip("/").rstrip("/") / "index.md"
        if not (md.exists() or html.exists() or idx.exists()):
            page_missing.append((f, r.get("title")))

unlisted_files = []
assets = ROOT / "assets"
if assets.exists():
    for dp, dns, fns in os.walk(assets):
        for fn in fns:
            rel = "/" + (Path(dp) / fn).relative_to(ROOT).as_posix()
            if is_doc(rel) and Path(fn).suffix.lower().lstrip(".") in DOC_EXTS and rel not in registry and rel not in linked:
                if "/qa_reports/" in rel:      # the weekly QA reports are listed on the QA pages, not here
                    continue
                unlisted_files.append(rel)

# ---------------------------------------------------------------- report
def section(title, items, fmt):
    print(f"\n{title}  ({len(items)})")
    print("-" * (len(title) + len(str(len(items))) + 4))
    for it in items:
        print("  " + fmt(it))
    if not items:
        print("  none")

print(f"Registry: {len(rows)} documents; pages link to {len(linked)} distinct document files.")
section("1. NOT IN THE REGISTRY (linked from a page)", not_in_registry,
        lambda p: f"{p}\n      linked from: {', '.join(sorted(linked[p])[:4])}{' ...' if len(linked[p]) > 4 else ''}")
section("2. MISSING FILES (registry row, no file in the repo)", missing, lambda t: f"{t[0]}   ({t[1]})")
section("3. DUPLICATES", dups, lambda s: s)
section("4. FILES NOTHING LINKS TO AND THE REGISTRY LACKS", sorted(unlisted_files), lambda s: s)
section("5. PAGE LINKS THAT DO NOT EXIST", page_missing, lambda t: f"{t[0]}   ({t[1]})")
print("\nTip: add rows for anything in section 1 or 4 that visitors should see, and fix or remove rows in section 2.")
sys.exit(1 if (missing or dups) else 0)
