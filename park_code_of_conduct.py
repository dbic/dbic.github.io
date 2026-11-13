#!/usr/bin/env python3
"""Temporarily take the Code of Conduct page off the site, and put it back later. Run from the repository root.

    python park_code_of_conduct.py hide             # preview
    python park_code_of_conduct.py hide --apply     # remove it
    python park_code_of_conduct.py restore          # preview
    python park_code_of_conduct.py restore --apply  # put it back

HIDE moves policies/codeofconduct.md into the folder _parked/ (folders starting with "_" are never published, and the
page stays in the repository so people can still read and edit it there), and removes the lines that point at it from the
menu (which also feeds the footer and the search box), the Safety & compliance document list and the forms library.
Every removed line is saved in _parked/code_of_conduct.json, together with its neighbours, so RESTORE can put it back
in the same place. Nothing else is touched. Both commands are safe to repeat."""
import json, sys
from pathlib import Path
APPLY = "--apply" in sys.argv
CMD = next((a for a in sys.argv[1:] if a in ("hide", "restore")), None)
PAGE = Path("policies/codeofconduct.md"); PARKED = Path("_parked/codeofconduct.md"); STASH = Path("_parked/code_of_conduct.json")
NEEDLE = "/policies/codeofconduct.html"
FILES = ["_data/menu.yml", "_data/policy_documents.csv", "_data/documents.csv"]
if not CMD: print(__doc__); sys.exit(0)
say = lambda s: print(("do    " if APPLY else "would ") + s)

if CMD == "hide":
    stash = json.loads(STASH.read_text(encoding="utf-8")) if STASH.exists() else {"lines": []}
    if PAGE.exists():
        say(f"move {PAGE} -> {PARKED}")
        if APPLY: PARKED.parent.mkdir(exist_ok=True); PAGE.replace(PARKED)
    elif PARKED.exists(): print(f"ok    page is already in {PARKED}")
    else: print(f"CHECK {PAGE} not found (and nothing in {PARKED})")
    for f in FILES:
        p = Path(f)
        if not p.exists(): print(f"CHECK {f} not found"); continue
        lines = p.read_text(encoding="utf-8").split("\n"); keep = []; gone = False
        for i, l in enumerate(lines):
            if NEEDLE in l:
                gone = True; say(f"remove from {f}: {l.strip()[:90]}")
                prev = next((x for x in reversed(lines[:i]) if x.strip()), ""); nxt = next((x for x in lines[i + 1:] if x.strip()), "")
                stash["lines"].append({"file": f, "line": l, "prev": prev, "next": nxt})
            else: keep.append(l)
        if gone and APPLY: p.write_text("\n".join(keep), encoding="utf-8")
        if not gone: print(f"ok    {f}: no reference left")
    if APPLY and stash["lines"]: STASH.parent.mkdir(exist_ok=True); STASH.write_text(json.dumps(stash, indent=1, ensure_ascii=False), encoding="utf-8")
    print("\nThe Code of Conduct page is " + ("now hidden." if APPLY else "not hidden yet: run again with --apply."))
else:
    if PARKED.exists() and not PAGE.exists():
        say(f"move {PARKED} -> {PAGE}")
        if APPLY: PAGE.parent.mkdir(exist_ok=True); PARKED.replace(PAGE)
    elif PAGE.exists(): print(f"ok    page is already at {PAGE}")
    else: print(f"CHECK the page is not in {PARKED} either")
    if not STASH.exists(): print("CHECK no saved lines found (_parked/code_of_conduct.json): add the menu and list entries back by hand"); sys.exit(0)
    stash = json.loads(STASH.read_text(encoding="utf-8")); left = []
    for e in stash["lines"]:
        p = Path(e["file"]); lines = p.read_text(encoding="utf-8").split("\n")
        if any(NEEDLE in l for l in lines): print(f"ok    {e['file']}: already has the entry"); continue
        at = None
        if e["prev"] and e["prev"] in lines: at = lines.index(e["prev"]) + 1
        elif e["next"] and e["next"] in lines: at = lines.index(e["next"])
        if at is None:
            at = len(lines) - 1 if lines and lines[-1] == "" else len(lines); print(f"CHECK {e['file']}: could not find the neighbouring lines; adding the entry at the end, please move it")
        say(f"add back to {e['file']}: {e['line'].strip()[:90]}")
        if APPLY: lines.insert(at, e["line"]); p.write_text("\n".join(lines), encoding="utf-8")
    if APPLY and STASH.exists(): STASH.unlink(); (STASH.parent.rmdir() if not any(STASH.parent.iterdir()) else None)
    print("\nThe Code of Conduct page is " + ("back on the site." if APPLY else "not restored yet: run again with --apply."))
