#!/usr/bin/env python3
"""
Rewrite links that point at the site's root index file (index.md or index.html in the
top-level folder) so they point at the root path "/" instead.

Why: a breadcrumb "Home" link written as ../index.md is not converted to a web address
by the Jekyll build, so on the published site it leads to /index.md, which doesn't exist.
Links to folder index pages (people/index.md and similar) are left alone: those are
converted correctly.

Usage, from the repo root:
    python fix_home_links.py            # preview only: lists what would change
    python fix_home_links.py --apply    # make the changes

Handles Markdown links  [Home](../index.md#top)  and HTML  href="../index.md".
A "#fragment" is kept. Skips README.md, the .git folder, and folders starting with "_".

Note: "/" assumes the site lives at the root of its domain (baseurl is empty in
_config.yml, as for dbic.github.io). If you ever serve it from a sub-path, tell me and
we'll switch these to a different form.
"""

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SKIP_DIRS = {".git", "node_modules", "vendor", "assets"}
MD_LINK = re.compile(r"(\]\(\s*<?)([^)\s>]+)")
HTML_HREF = re.compile(r"""(\bhref\s*=\s*["'])([^"']+)""", re.I)


def points_at_root_index(root, src, target):
    """True if `target` (a relative link found in file `src`) is the root index file."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
        return False
    if target.startswith("/"):                       # already root-relative: only /index.md and /index.html matter
        return target.split("#")[0].split("?")[0] in ("/index.md", "/index.html")
    path, hash_, frag = target.partition("#")
    path = path.split("?")[0]
    if not re.search(r"(^|/)index\.(md|html)$", path):
        return False
    resolved = (src.parent / unquote(path)).resolve()
    return resolved in {(root / "index.md").resolve(), (root / "index.html").resolve()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--apply", action="store_true", help="write the changes (default: preview only)")
    a = ap.parse_args()
    root = Path(a.root).resolve()

    total_links = total_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith((".", "_"))]
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn == "README.md":
                continue
            src = Path(dirpath) / fn
            text = src.read_text(encoding="utf-8")
            changes = []

            def fix(m):
                target = m.group(2)
                if not points_at_root_index(root, src, target):
                    return m.group(0)
                frag = target.partition("#")[2]
                new = "/" + ("#" + frag if frag else "")
                changes.append((target, new))
                return m.group(1) + new

            new_text = HTML_HREF.sub(fix, MD_LINK.sub(fix, text))
            if changes:
                total_files += 1
                total_links += len(changes)
                rel = src.relative_to(root).as_posix()
                for old, new in changes:
                    print(f"{rel}: {old}  ->  {new}")
                if a.apply:
                    src.write_text(new_text, encoding="utf-8")

    verb = "Fixed" if a.apply else "Would fix"
    print(f"\n{verb} {total_links} link(s) in {total_files} file(s)."
          + ("" if a.apply or not total_links else "  Run again with --apply to make the changes."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
