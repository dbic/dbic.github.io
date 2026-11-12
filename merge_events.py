#!/usr/bin/env python3
"""
Merge rows from another CSV (for example brown_bag_history.csv) into _data/events.csv, safely.

Run from the repository root.  It only SHOWS what it would do, unless you add --apply:

    python merge_events.py brown_bag_history.csv            # preview
    python merge_events.py brown_bag_history.csv --apply    # write _data/events.csv

What it does
  * A row is the "same" row if its date, category and title (the speaker or session) match, ignoring capitals.
  * Rows that are already in events.csv are NEVER overwritten. Only cells that are empty there are filled in
    from the import (for example a talk title that was missing).
  * Rows that are not in events.csv yet are added at the end.
  * Columns that events.csv does not have yet (such as `talk`) are added; every row gets the full set of columns.
  * Nothing else is changed. Running it twice changes nothing the second time.
"""

import csv
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if not a.startswith("--")]
APPLY = "--apply" in sys.argv
if not args:
    sys.exit(__doc__)
IMPORT = Path(args[0])
EVENTS = Path(args[1]) if len(args) > 1 else Path("_data/events.csv")

for p in (IMPORT, EVENTS):
    if not p.exists():
        sys.exit(f"Cannot find {p}. Run this from the repository root.")


def read(path):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    rows = list(csv.reader(text.splitlines()))
    header, body = rows[0], [r for r in rows[1:] if any(c.strip() for c in r)]
    return header, [dict(zip(header, r + [""] * (len(header) - len(r)))) for r in body], bom


key = lambda r: ((r.get("date") or "").strip(), (r.get("category") or "").strip().lower(), (r.get("title") or "").strip().lower())

ev_header, ev_rows, bom = read(EVENTS)
im_header, im_rows, _ = read(IMPORT)

header = list(ev_header) + [c for c in im_header if c not in ev_header]
new_cols = [c for c in header if c not in ev_header]

index = {key(r): r for r in ev_rows}
filled, added, same = [], [], 0
for r in im_rows:
    k = key(r)
    if k in index:
        cur = index[k]
        changed = False
        for col in im_header:
            if (r.get(col) or "").strip() and not (cur.get(col) or "").strip():
                cur[col] = r[col]
                filled.append(f"{k[0]}  {r.get('title')}: filled {col}")
                changed = True
        if not changed:
            same += 1
    else:
        ev_rows.append({c: r.get(c, "") for c in header})
        index[k] = ev_rows[-1]
        added.append(r)

print(f"events file: {EVENTS}  ({len(ev_header)} columns)   import: {IMPORT}  ({len(im_rows)} rows)")
if new_cols:
    print(f"new column(s) added to every row: {', '.join(new_cols)}")
print(f"already present and left alone: {same}")
print(f"empty cells filled in existing rows: {len(filled)}")
for f in filled[:12]:
    print("   " + f)
print(f"rows added: {len(added)}")
for r in added[:5]:
    print(f"   {r['date']}  {r['title']}")
if len(added) > 5:
    print(f"   ... and {len(added) - 5} more")

if not (added or filled or new_cols):
    print("\nNothing to do.")
elif APPLY:
    with EVENTS.open("w", newline="", encoding="utf-8-sig" if bom else "utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for r in ev_rows:
            w.writerow([r.get(c, "") for c in header])
    print(f"\nWritten: {EVENTS}")
else:
    print("\nPreview only. Run again with --apply to write the changes.")
