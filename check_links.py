#!/usr/bin/env python3
"""
Check links in the Markdown site (run from the repo root, or pass the folder).

Internal checks (always):
  * the target file exists, with EXACTLY the right upper/lower case (GitHub Pages
    is case-sensitive even if your Mac or Windows disk is not)
  * "x.html" links resolve to x.md, and "folder/" links to folder/index.md
  * #fragment links match an <a id>, an id=, or a heading in the target page

External checks (only with --external):
  * each distinct http(s) URL is requested once; reports errors and permanent
    redirects (a page that "moved")

Usage:
    python check_links.py                 # internal only, fast, no network
    python check_links.py --external      # also check other sites
    python check_links.py path/to/repo --out link_report.csv

Writes link_report.csv and exits with status 1 if anything is wrong.
Approximate by design: it cannot see soft 404s (error pages served with status 200).
"""

import argparse
import csv
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote, urlparse

SKIP_DIRS = {".git", "_site", "node_modules", "vendor", "__pycache__", "assets"}
SKIP_FILES = {"README.md"}
SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:", "sms:")
MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)")
MD_REF = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*<?(\S+?)>?\s*$")
HTML_ATTR = re.compile(r"""\b(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
ID_ATTR = re.compile(r"""\b(?:id|name)\s*=\s*["']([^"']+)["']""", re.I)
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.*?)\s*#*\s*$")
CUSTOM_ID = re.compile(r"\{#([^}\s]+)\}")
UA = {"User-Agent": "dbic-link-checker/1.0"}


def code_free_lines(text):
    """Lines of the page with front matter and code blanked out (keeps numbering)."""
    lines = text.split("\n")
    out, in_fence = [], False
    start = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                out = [""] * (i + 1)
                start = i + 1
                break
    for line in lines[start:]:
        if re.match(r"^\s*(```|~~~)", line):
            in_fence = not in_fence
            out.append("")
        elif in_fence:
            out.append("")
        else:
            out.append(re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line))
    return out


def heading_ids(h):
    h = CUSTOM_ID.sub("", h)
    clean = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", h)
    clean = re.sub(r"[*_`]", "", clean).strip()
    gfm = re.sub(r"[^\w\- ]", "", clean.lower()).strip().replace(" ", "-")
    kram = re.sub(r"[^a-z0-9 -]", "", re.sub(r"^[^a-zA-Z]+", "", clean)).lower().replace(" ", "-")
    return {gfm, kram}


@lru_cache(maxsize=None)
def anchors_for(path):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    ids = set(ID_ATTR.findall(text)) | set(CUSTOM_ID.findall(text))
    for line in code_free_lines(text):
        m = HEADING.match(line)
        if m:
            ids |= heading_ids(m.group(1))
    return ids


@lru_cache(maxsize=None)
def listdir(d):
    try:
        return frozenset(os.listdir(d))
    except OSError:
        return frozenset()


def exists_exact(root, p):
    """True if file p exists under root with exactly matching name case."""
    try:
        rel = p.resolve().relative_to(root)
    except ValueError:
        return False
    cur = root
    for part in rel.parts:
        if part not in listdir(str(cur)):
            return False
        cur = cur / part
    return cur.is_file()


def resolve_internal(root, src, path):
    p = unquote(path)
    if p == "":
        return src
    base = root if p.startswith("/") else src.parent
    target = base / p.lstrip("/")
    cands = [target]
    if p.endswith("/") or target.is_dir():
        cands += [target / "index.md", target / "index.html"]
    if target.suffix == ".html":
        cands.append(target.with_suffix(".md"))
    for c in cands:
        if exists_exact(root, c):
            return c.resolve()
    return None


def extract(lines):
    for n, line in enumerate(lines, 1):
        found = MD_LINK.findall(line) + HTML_ATTR.findall(line)
        m = MD_REF.match(line)
        if m:
            found.append(m.group(1))
        for link in found:
            yield n, link.strip()


def check_url(args):
    import requests
    url, timeout = args
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout, headers=UA)
        if r.status_code in (400, 403, 404, 405, 501) or r.status_code >= 500:
            r = requests.get(url, allow_redirects=True, timeout=timeout, headers=UA, stream=True)
    except requests.RequestException as e:
        return url, f"error: {type(e).__name__}"
    if r.status_code >= 400:
        note = " (may be the site blocking bots)" if r.status_code in (403, 429) else ""
        return url, f"HTTP {r.status_code}{note}"
    if any(h.status_code in (301, 308) for h in r.history):
        return url, f"moved permanently to {r.url}"
    return url, ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", nargs="?", default=".")
    ap.add_argument("--external", action="store_true", help="also check http(s) links")
    ap.add_argument("--timeout", type=float, default=15)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--out", default="link_report.csv")
    a = ap.parse_args()

    root = Path(a.root).resolve()
    problems, external = [], {}
    n_files = n_links = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in sorted(filenames):
            if not fn.endswith(".md") or fn in SKIP_FILES:
                continue
            src = Path(dirpath) / fn
            rel = src.relative_to(root).as_posix()
            n_files += 1
            text = src.read_text(encoding="utf-8", errors="replace")
            for line_no, link in extract(code_free_lines(text)):
                if not link or link.lower().startswith(SKIP_SCHEMES):
                    continue
                n_links += 1
                if re.match(r"^(https?:)?//", link, re.I):
                    url = ("https:" + link) if link.startswith("//") else link
                    external.setdefault(url.split("#")[0], []).append((rel, line_no, link))
                    continue
                path, _, frag = link.partition("#")
                path = path.split("?")[0]
                target = resolve_internal(root, src, path)
                if target is None:
                    problems.append((rel, line_no, link, "target file not found (check spelling and case)"))
                    continue
                if frag and frag.lower() != "top" and target.suffix == ".md":
                    ids = anchors_for(str(target))
                    f = unquote(frag)
                    if f not in ids and re.sub(r"-\d+$", "", f) not in ids:
                        problems.append((rel, line_no, link, f"anchor '#{frag}' not found in target page"))

    if a.external and external:
        print(f"Checking {len(external)} external URLs ...")
        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            for url, result in ex.map(check_url, [(u, a.timeout) for u in external]):
                if result:
                    for rel, line_no, link in external[url]:
                        problems.append((rel, line_no, link, result))

    problems.sort()
    with open(a.out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["file", "line", "link", "problem"])
        w.writerows(problems)
    for rel, line_no, link, why in problems:
        print(f"{rel}:{line_no}: {link}  ->  {why}")
    mode = "internal + external" if a.external else "internal only"
    print(f"\n{n_files} pages, {n_links} links checked ({mode}); {len(problems)} problem(s). "
          f"Report: {a.out}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
    
