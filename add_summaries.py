#!/usr/bin/env python3
"""
Add a one-line `summary:` (and, where the page title is terse, an `index_title:`) to the front matter of
existing pages, so the automatic folder index pages (Research infrastructure, People, Events) can show a
sentence under each page title.

Run from the repo root.  It only SHOWS what it would change, unless you add --apply:

    python add_summaries.py            # preview
    python add_summaries.py --apply    # write the changes

It never overwrites: a page that already has a `summary:` (or `index_title:`) is left alone, and pages that do
not exist are skipped. The wording below is mine, from reading each page; edit the lines in this file before
applying, or edit the pages afterwards.
"""

import sys
from pathlib import Path

ROOT = Path(".")
APPLY = "--apply" in sys.argv

# page (without extension)           ->  (summary, index_title or None)
SUGGESTIONS = {
    "research_infrastructure/fmri_scanner":      ("The 3T Siemens MAGNETOM Prisma and what it can do.", None),
    "research_infrastructure/coils":             ("The head coils: what each offers and when to use it.", None),
    "research_infrastructure/sequences":         ("The standard acquisition sequences and their settings.", None),
    "research_infrastructure/peripherals":       ("Stimulus delivery, response devices, eye tracking and physiological recording.", None),
    "research_infrastructure/qualityassurance":  ("Weekly phantom measurements that track scanner performance.", "Quality assurance"),
    "research_infrastructure/computer_resources": ("Where your scans land, converting them to BIDS, and storage.", None),
    "research_infrastructure/discovery":         ("The DBIC's allocation on the Discovery computing cluster, and its limits.", None),
    "research_infrastructure/datasets":          ("The datasets hosted at the center, with access terms.", None),
    "people/directorsstaff":                     ("The director and the staff who run the center.", "Director and staff"),
    "people/advisorycommittee":                  ("The faculty committee that advises the center.", None),
    "people/affiliated":                         ("Faculty from across campus who use the center in their research.", None),
    "events/fbb":                                ("Past talks in the fMRI brown-bag series.", "fMRI brown bags"),
}


def find(stem):
    for ext in (".md", ".html", ".markdown"):
        p = ROOT / (stem + ext)
        if p.exists():
            return p
    return None


def quote(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


changed = 0
for stem, (summary, idx_title) in SUGGESTIONS.items():
    p = find(stem)
    if not p:
        print(f"skip      {stem}  (no such page)")
        continue
    text = p.read_text(encoding="utf-8")
    if not text.startswith("---"):
        print(f"skip      {p}  (no front matter)")
        continue
    end = text.find("\n---", 3)
    if end == -1:
        print(f"skip      {p}  (front matter not closed)")
        continue
    front, rest = text[3:end], text[end:]
    lines = front.split("\n")
    has = lambda key: any(l.startswith(key + ":") for l in lines)
    add = []
    if not has("summary"):
        add.append(f"summary: {quote(summary)}")
    if idx_title and not has("index_title"):
        add.append(f"index_title: {quote(idx_title)}")
    if not add:
        print(f"ok        {p}  (already has them)")
        continue
    print(f"{'add' if APPLY else 'would add'}  {p}")
    for a in add:
        print(f"            + {a}")
    if APPLY:
        new_front = front.rstrip("\n") + "\n" + "\n".join(add)
        p.write_text("---" + new_front + rest, encoding="utf-8")
    changed += 1

print(f"\n{changed} page(s) {'changed' if APPLY else 'would change'}." + ("" if APPLY else "  Run again with --apply to write them."))
