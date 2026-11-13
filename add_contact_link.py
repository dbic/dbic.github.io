#!/usr/bin/env python3
"""Add a "Who to contact" link to the "Keep exploring" row of the pages that mention a contact person.
Run from the repository root. It only SHOWS what it would do, unless you add --apply:
    python add_contact_link.py            # preview
    python add_contact_link.py --apply    # write the changes
It adds one line to the end of each page's `related:` list (in the front matter), and skips pages that already have it."""
import re, sys
from pathlib import Path
APPLY = "--apply" in sys.argv
LINE = '  - { title: "Who to contact", url: "/contact.html" }'
PAGES = ["policies/scheduling.md", "policies/safetytraining.md", "policies/operator_training.md", "policies/cancellations.md", "policies/dbic_billing.md",
         "policies/dbic_protocol.md", "policies/dbic_parking.md", "policies/forms_templates.md", "policies/housekeeping.md",
         "research_infrastructure/peripherals.md", "research_infrastructure/computer_resources.md", "research_infrastructure/discovery.md",
         "research_infrastructure/datasets.md", "faqs.md"]
n = 0
for rel in PAGES:
    p = Path(rel)
    if not p.exists(): print("skip      ", rel, "(no such page)"); continue
    t = p.read_text(encoding="utf-8"); m = re.match(r"(---\n)(.*?)(\n---\n)", t, re.S)
    if not m: print("skip      ", rel, "(no front matter)"); continue
    fm = m.group(2)
    if "/contact.html" in fm: print("ok        ", rel, "(already has it)"); continue
    last = [l for l in fm.split("\n") if l.strip()][-1]
    if "related:" not in fm or not last.startswith("  - {"): print("CHECK     ", rel, "(no related list at the end of the front matter: add the line by hand)"); continue
    print(("add       " if APPLY else "would add ") + rel); n += 1
    if APPLY: p.write_text(t[:m.end(2)] + "\n" + LINE + t[m.end(2):], encoding="utf-8")
print(f"\n{n} page(s) {'changed' if APPLY else 'would change'}." + ("" if APPLY else "  Run again with --apply to write them."))
