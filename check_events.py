#!/usr/bin/env python3
"""
Check _data/events.csv for the mistakes that make events silently disappear or lose text on the site.

Run from the repository root:
    python check_events.py                 # checks _data/events.csv
    python check_events.py path/to/other.csv

It reports (E = error, W = warning):
  E  a row with MORE values than the header has columns (the extra values are dropped by the site; usually a missing header such as "talk")
  E  a missing or badly written date (must be YYYY-MM-DD, for example 2026-12-04)
  E  a byte-order mark at the start of the file (the first column name is then wrong and EVERY event breaks)
  E  a missing title or category
  W  a line break inside a cell (the text still shows, but with a stray space; usually a hard-wrapped paste)
  W  category names that differ only by capitals or spaces (the site matches them exactly, so "Brown Bag" is not "Brown bag")
  W  the same date, category and title twice
  W  columns the site does not use
It also prints how many rows each category has.  Exit status is 1 if there is any error.
"""

import csv
import datetime
import io
import sys
from collections import Counter, defaultdict
from pathlib import Path

PATH = Path(sys.argv[1] if len(sys.argv) > 1 else "_data/events.csv")
KNOWN = ["date", "time", "category", "title", "detail", "deadline", "url", "date_label", "talk"]
if not PATH.exists():
    sys.exit(f"Cannot find {PATH}. Run this from the repository root.")

raw = PATH.read_bytes()
errors, warnings = [], []

if raw.startswith(b"\xef\xbb\xbf"):
    errors.append("line 1: the file starts with a byte-order mark (invisible character). Re-save it as plain \"CSV UTF-8\" "
                  "without BOM, or delete the first character in a text editor; otherwise the first column is not read as 'date'.")
text = raw.decode("utf-8-sig")
if "\r" in text.replace("\r\n", ""):
    warnings.append("the file contains old-style Mac line endings; re-save it with normal line endings")

reader = csv.reader(io.StringIO(text, newline=""))
rows = []
try:
    for row in reader:
        rows.append((reader.line_num, row))
except csv.Error as e:
    sys.exit(f"E  the file cannot be read as CSV ({e}); look near line {reader.line_num}")

if not rows:
    sys.exit("The file is empty.")
header_line, header = rows[0]
header = [h.strip() for h in header]
for need in ("date", "category", "title"):
    if need not in header:
        errors.append(f"line 1: the header has no '{need}' column (header is: {','.join(header)})")
for h in header:
    if h and h not in KNOWN:
        warnings.append(f"line 1: column '{h}' is not used by the site")

body = [(n, r) for n, r in rows[1:] if any(c.strip() for c in r)]
col = {h: i for i, h in enumerate(header)}
get = lambda r, name: (r[col[name]].strip() if name in col and col[name] < len(r) else "")
extra_rows = []
cats = Counter()
seen = defaultdict(list)
norm_cats = defaultdict(set)


def valid_date(s):
    try:
        datetime.datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False


for n, r in body:
    where = f"line {n}"
    if len(r) > len(header):
        extra_rows.append((n, r[len(header):]))
    d = get(r, "date")
    if not d:
        errors.append(f"{where}: no date ({get(r, 'title') or 'untitled row'})")
    elif not valid_date(d):
        errors.append(f"{where}: the date {d!r} is not written as YYYY-MM-DD (for example 2026-12-04)")
    dl = get(r, "deadline")
    if dl and not valid_date(dl):
        errors.append(f"{where}: the deadline {dl!r} is not written as YYYY-MM-DD")
    if not get(r, "title"):
        errors.append(f"{where}: no title")
    cat = get(r, "category")
    if not cat:
        errors.append(f"{where}: no category")
    cats[cat] += 1
    norm_cats["".join(cat.lower().split())].add(cat)
    for name, i in col.items():
        if i < len(r) and ("\n" in r[i] or "\r" in r[i]):
            warnings.append(f"{where}: a line break inside the '{name}' cell ({r[i][:40].strip()!r}...); the text shows with a stray space")
    seen[(d, cat.lower(), get(r, "title").lower())].append(n)

if extra_rows:
    lost = [(n, e) for n, e in extra_rows if any(x.strip() for x in e)]
    widest = max(len(e) for _, e in extra_rows)
    hint = ('Add ",talk" to the end of the first line (the header) and the text will show.' if "talk" not in header and widest == 1
            else f"The header is missing {widest} column name(s) at its end.")
    if lost:
        n0, e0 = lost[0]
        text0 = next(x for x in e0 if x.strip())
        errors.append(f"{len(extra_rows)} rows have more values than the header has columns ({len(header)}), and {len(lost)} of them hold text "
                      f"that the site is dropping, for example line {n0}: {text0[:60]!r}{'...' if len(text0) > 60 else ''}. {hint}")
    else:
        warnings.append(f"{len(extra_rows)} rows have more values than the header has columns ({len(header)}), but the extra values are empty, so nothing is lost. {hint}")

for k, lines in seen.items():
    if len(lines) > 1 and k[0]:
        warnings.append(f"lines {', '.join(map(str, lines))}: the same date, category and title appear {len(lines)} times ({k[2]})")
for variants in norm_cats.values():
    if len(variants) > 1:
        warnings.append("category written in different ways: " + " / ".join(repr(v) for v in sorted(variants)) +
                        ". The site matches the exact text, so rows under the odd spelling are left out.")

print(f"{PATH}: {len(header)} columns ({', '.join(header)}), {len(body)} rows\n")
print("rows per category:")
for c, k in sorted(cats.items(), key=lambda x: (-x[1], x[0])):
    print(f"  {k:4}  {c or '(none)'}")
print()
for e in errors:
    print("E ", e)
for w in warnings:
    print("W ", w)
if not errors and not warnings:
    print("No problems found.")
else:
    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s).")
sys.exit(1 if errors else 0)
