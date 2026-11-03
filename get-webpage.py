#!/usr/bin/env python3
"""
Crawl a website section, convert each HTML page to Markdown, and download
linked assets (PDFs, images, documents). Links in the Markdown are rewritten
to point to the local copies.

Setup:
    pip install requests beautifulsoup4 markdownify

Quick test (first 5 pages only):
    python get-webpage.py --max-pages 5

Full run:
    python get-webpage.py

Output (default ./dbic.github.io):
    <path>/index.md        one Markdown file per page, mirroring URL structure
    assets/...             downloaded PDFs, images, documents
    manifest.csv           every page and asset, with status
    broken_links.csv       anything that failed to download or was blocked

The script is resumable: assets already on disk are not downloaded again.
"""

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
from collections import deque
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote, urldefrag, urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as to_markdown
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = "dbic-markdown-migration/1.0 (site owner migration to GitHub)"

ASSET_EXTS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".csv", ".txt",
    ".rtf", ".zip", ".gz", ".tar", ".json", ".xml", ".bib", ".mat", ".nii",
    ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".tif", ".tiff", ".ico",
    ".mp3", ".mp4", ".m4v", ".mov", ".avi", ".wmv", ".wav",
}
PAGE_EXTS = {".html", ".htm", ".php", ".aspx", ".asp"}
MEDIA_TAGS = {"img", "source", "video", "audio", "embed"}
LINK_ATTRS = [
    ("a", "href"), ("img", "src"), ("source", "src"),
    ("video", "src"), ("video", "poster"), ("audio", "src"), ("embed", "src"),
]
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "data:", "#")
DEFAULT_SELECTORS = ["main", "[role=main]", "#main-content", "article", "body"]
ALWAYS_STRIP = ["script", "style", "noscript", "nav", "footer", "svg"]


def normalize(url):
    """Drop fragment, collapse //, and fold index.html into the directory."""
    url, _ = urldefrag(url)
    p = urlparse(url)
    path = re.sub(r"/{2,}", "/", p.path or "/")
    base = path.rsplit("/", 1)[-1].lower()
    if base in ("index.html", "index.htm", "index.php"):
        path = path[: -len(base)]
    return p._replace(scheme=p.scheme.lower(), netloc=p.netloc.lower(),
                      path=path, params="").geturl()


def safe_segment(seg):
    return re.sub(r'[<>:"|?*\\]', "_", seg).strip() or "_"


def query_suffix(query):
    return "__" + hashlib.md5(query.encode()).hexdigest()[:8] if query else ""


class Crawler:
    def __init__(self, args):
        self.start = normalize(args.start)
        sp = urlparse(self.start)
        self.host = sp.netloc
        self.prefix = sp.path if sp.path.endswith("/") else sp.path + "/"
        self.out = Path(args.out)
        self.delay = args.delay
        self.max_pages = args.max_pages
        self.selectors = ([args.selector] if args.selector else []) + DEFAULT_SELECTORS
        self.strip = ALWAYS_STRIP + (args.strip or [])
        self.asset_hosts = {self.host} | set(args.asset_host or [])

        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        retry = Retry(total=3, backoff_factor=1,
                      status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))

        self.robots = RobotFileParser()
        self._load_robots()

        self.queue = deque()
        self.page_paths = {}   # local path -> url (dedupe)
        self.assets = {}       # url -> first referring page
        self.rows = []         # manifest rows

    # ---------- setup helpers ----------
    def _load_robots(self):
        try:
            r = self.session.get(f"https://{self.host}/robots.txt", timeout=15)
            self.robots.parse(r.text.splitlines() if r.ok else [])
        except requests.RequestException:
            self.robots.parse([])

    def allowed(self, url):
        return self.robots.can_fetch(USER_AGENT, url)

    def in_scope(self, url):
        p = urlparse(url)
        return p.netloc == self.host and (p.path.rstrip("/") + "/").startswith(self.prefix)

    # ---------- URL -> local path ----------
    def page_path(self, url):
        p = urlparse(url)
        rel = unquote(p.path)[len(self.prefix):] if p.path.startswith(self.prefix) else ""
        suffix = query_suffix(p.query)
        if rel == "" or rel.endswith("/"):
            rel += "index.md"
        else:
            name = rel.rsplit("/", 1)[-1]
            ext = os.path.splitext(name)[1].lower()
            if ext in PAGE_EXTS:
                rel = rel[: -len(ext)] + ".md"
            else:
                rel += "/index.md"
        if suffix:
            rel = rel[:-3] + suffix + ".md"
        parts = [safe_segment(s) for s in rel.split("/")]
        return self.out.joinpath(*parts)

    def asset_path(self, url):
        p = urlparse(url)
        rel = unquote(p.path).lstrip("/")
        if p.netloc != self.host:
            rel = f"_{p.netloc}/{rel}"
        if p.query:
            stem, ext = os.path.splitext(rel)
            rel = stem + query_suffix(p.query) + ext
        parts = [safe_segment(s) for s in rel.split("/")]
        return self.out.joinpath("assets", *parts)

    @staticmethod
    def rel_link(target, from_file):
        rel = os.path.relpath(target, start=from_file.parent)
        return quote(Path(rel).as_posix(), safe="/._-~()")

    # ---------- link handling ----------
    def classify(self, page_url, tag, raw):
        raw = (raw or "").strip()
        if not raw or raw.lower().startswith(SKIP_PREFIXES):
            return None, None, ""
        absolute = urljoin(page_url, raw)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            return None, None, ""
        url = normalize(absolute)
        ext = os.path.splitext(unquote(parsed.path))[1].lower()
        if parsed.netloc.lower() in self.asset_hosts and (
                tag in MEDIA_TAGS or ext in ASSET_EXTS):
            return "asset", url, parsed.fragment
        if self.in_scope(url):
            return "page", url, parsed.fragment
        return "external", absolute, ""

    def discover(self, soup, page_url):
        """Scan the FULL page (including nav) for pages and assets to fetch."""
        for tag, attr in LINK_ATTRS:
            for el in soup.find_all(tag):
                kind, url, _ = self.classify(page_url, tag, el.get(attr))
                if kind == "page":
                    self.enqueue(url)
                elif kind == "asset":
                    self.assets.setdefault(url, page_url)

    def enqueue(self, url):
        lp = self.page_path(url)
        if lp in self.page_paths:
            return
        self.page_paths[lp] = url
        self.queue.append(url)

    def rewrite(self, root, page_url, page_file):
        for el in root.find_all("img"):
            if (not el.get("src") or el["src"].startswith("data:")) and el.get("data-src"):
                el["src"] = el["data-src"]
            el.attrs.pop("srcset", None)
        for tag, attr in LINK_ATTRS:
            for el in root.find_all(tag):
                raw = el.get(attr)
                kind, url, frag = self.classify(page_url, tag, raw)
                if kind == "asset":
                    new = self.rel_link(self.asset_path(url), page_file)
                elif kind == "page":
                    new = self.rel_link(self.page_path(url), page_file)
                    if frag:
                        new += "#" + frag
                elif kind == "external":
                    new = url
                else:
                    continue
                el[attr] = new

    # ---------- HTTP ----------
    def get(self, url, stream=False):
        time.sleep(self.delay)
        return self.session.get(url, timeout=30, stream=stream, allow_redirects=True)

    def row(self, kind, url, local, status, ref=""):
        self.rows.append({
            "type": kind, "url": url,
            "local_path": Path(local).as_posix() if local else "",
            "status": status, "referenced_from": ref,
        })

    # ---------- page conversion ----------
    def convert(self, url, resp):
        soup = BeautifulSoup(resp.content, "html.parser")
        page_file = self.page_path(url)

        # 1. find links anywhere on the page (nav included)
        self.discover(soup, url)

        # 2. pick the content container and clean it
        root = None
        for sel in self.selectors:
            root = soup.select_one(sel)
            if root:
                break
        for sel in self.strip:
            for el in root.select(sel):
                el.decompose()

        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        else:
            h1 = soup.find("h1")
            title = h1.get_text(strip=True) if h1 else page_file.parent.name

        # 3. rewrite links to local copies, convert, tidy
        self.rewrite(root, url, page_file)
        body = to_markdown(str(root), heading_style="ATX", bullets="-")
        body = re.sub(r"[ \t]+\n", "\n", body)
        body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

        front = (
            "---\n"
            f"title: {json.dumps(title, ensure_ascii=False)}\n"
            f"source_url: {url}\n"
            f"retrieved: {date.today().isoformat()}\n"
            "---\n\n"
        )
        page_file.parent.mkdir(parents=True, exist_ok=True)
        page_file.write_text(front + body, encoding="utf-8")
        return page_file

    # ---------- main phases ----------
    def crawl_pages(self):
        self.enqueue(self.start)
        done = 0
        while self.queue:
            if self.max_pages and done >= self.max_pages:
                print(f"Reached --max-pages ({self.max_pages}); stopping.")
                break
            url = self.queue.popleft()
            if not self.allowed(url):
                print(f"[robots] blocked: {url}")
                self.row("page", url, "", "blocked by robots.txt")
                continue
            try:
                resp = self.get(url)
            except requests.RequestException as e:
                print(f"[error] {url}: {e}")
                self.row("page", url, "", f"error: {e}")
                continue
            final = normalize(resp.url)
            if resp.status_code != 200:
                print(f"[{resp.status_code}] {url}")
                self.row("page", url, "", f"HTTP {resp.status_code}")
                continue
            if not self.in_scope(final):
                self.row("page", url, "", f"redirected out of scope: {final}")
                continue
            ctype = resp.headers.get("Content-Type", "")
            if "html" not in ctype.lower():
                # Not a page after all; treat as an asset instead.
                self.assets.setdefault(final, "(linked as page)")
                continue
            local = self.convert(final, resp)
            done += 1
            print(f"[{done}] {final} -> {local}")
            self.row("page", final, local, "ok")
        print(f"\nPages converted: {done}. Assets found: {len(self.assets)}")

    def download_assets(self):
        for i, (url, ref) in enumerate(sorted(self.assets.items()), 1):
            dest = self.asset_path(url)
            if dest.exists():
                self.row("asset", url, dest, "ok (already present)", ref)
                continue
            if not self.allowed(url):
                self.row("asset", url, "", "blocked by robots.txt", ref)
                continue
            try:
                resp = self.get(url, stream=True)
                if resp.status_code != 200:
                    print(f"[{resp.status_code}] asset {url}")
                    self.row("asset", url, "", f"HTTP {resp.status_code}", ref)
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                tmp = dest.with_suffix(dest.suffix + ".part")
                with open(tmp, "wb") as f:
                    for chunk in resp.iter_content(65536):
                        f.write(chunk)
                tmp.replace(dest)
                print(f"[asset {i}/{len(self.assets)}] {url}")
                self.row("asset", url, dest, "ok", ref)
            except requests.RequestException as e:
                print(f"[error] asset {url}: {e}")
                self.row("asset", url, "", f"error: {e}", ref)

    def write_reports(self):
        self.out.mkdir(parents=True, exist_ok=True)
        fields = ["type", "url", "local_path", "status", "referenced_from"]
        for name, rows in (
            ("manifest.csv", self.rows),
            ("broken_links.csv", [r for r in self.rows if not r["status"].startswith("ok")]),
        ):
            with open(self.out / name, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)
        bad = sum(1 for r in self.rows if not r["status"].startswith("ok"))
        print(f"Wrote manifest.csv and broken_links.csv ({bad} problem rows) in {self.out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default="https://www.dartmouth.edu/dbic/")
    ap.add_argument("--out", default="dbic.github.io")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="seconds between requests (default 0.5)")
    ap.add_argument("--max-pages", type=int, default=0,
                    help="stop after N pages (0 = no limit); useful for testing")
    ap.add_argument("--selector",
                    help="CSS selector for the main content area; tried first")
    ap.add_argument("--strip", action="append",
                    help="extra CSS selector to remove from content (repeatable)")
    ap.add_argument("--asset-host", action="append",
                    help="extra host to download assets from (repeatable)")
    args = ap.parse_args()

    c = Crawler(args)
    try:
        c.crawl_pages()
        c.download_assets()
    except KeyboardInterrupt:
        print("\nInterrupted; writing reports for what was completed.")
    finally:
        c.write_reports()


if __name__ == "__main__":
    sys.exit(main())
    
