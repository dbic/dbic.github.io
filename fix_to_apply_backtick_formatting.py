#!/usr/bin/env python3
"""Show file paths and group names on the datasets page as code (`/vast/labs/DBIC/datasets/...`, `rc-DBIC`).
Run from the repository root.
    python apply_dataset_code_formatting.py            # preview: lists each change
    python apply_dataset_code_formatting.py --apply    # write the changes
It only ADDS the backtick marks. It leaves alone text that is already code, link addresses (including web addresses) and
everything else, and it is safe to run again."""
import re, sys
from pathlib import Path
APPLY = "--apply" in sys.argv
F = "research_infrastructure/datasets.md"
PATH = re.compile(r"(?<![\w:/.\-])(/(?:dartfs|dartfs-hpc|vast)/[A-Za-z0-9_./\-]*[A-Za-z0-9_\-])")     # a file path (the last character is never a full stop)
GROUP = re.compile(r"(?<![\w\-])(rc-DBIC)(?![\w\-])")
SKIP = re.compile(r"(`[^`\n]*`|\]\([^)\n]*\)|https?://[^\s)>\]]+|<[^>\n]+>)")                              # code, link addresses, web addresses, HTML tags
def fix(line):
    out, n_p, n_g = [], 0, 0
    for part in SKIP.split(line):
        if SKIP.fullmatch(part): out.append(part); continue
        part, k = PATH.subn(r"`\1`", part); n_p += k
        part, k = GROUP.subn(r"`\1`", part); n_g += k
        out.append(part)
    return "".join(out), n_p, n_g
p = Path(F)
if not p.exists(): print(f"missing file {F}: run this from the repository root"); sys.exit(1)
lines = p.read_text(encoding="utf-8").split("\n"); new, tp, tg = [], 0, 0
for i, l in enumerate(lines, 1):
    f, a, b = fix(l); new.append(f)
    if f != l:
        tp += a; tg += b; print(f"line {i:3}: " + re.sub(r"\*\*[^*]*\*\*", "", f).strip()[:110])
if tp + tg == 0: print("already done: every file path and group name on the page is already shown as code.")
else: print(f"\n{tp} file paths and {tg} group names {'formatted as code' if APPLY else 'would be formatted as code'}.")
if APPLY and tp + tg: p.write_text("\n".join(new), encoding="utf-8")
elif not APPLY and tp + tg: print("Preview only. Run again with --apply to write the changes.")
