#!/usr/bin/env python3
"""
Crawl a website section, convert each HTML page to Markdown, and download
linked assets (PDFs, images, documents). Links in the Markdown are rewritten
to point to the local copies.

Setup:
    pip install requests beautifulsoup4 markdownify

Quick test (first 5 pages only):
    python crawl_to_markdown.py --max-pages 5

Full run:
    python crawl_to_markdown.py

Output (default ./dbic-markdown):
    <path>/index.md        one Markdown file per page, mirroring URL structure
    assets/...             downloaded PDFs, images, documents
    manifest.csv           every page and asset, with status
    broken_links.csv       anything that failed to download or was blocked

The script is resumable: assets already on disk are not downloaded again.
"""

import argparse
import csv
import hashlib
import html as htmlmod
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
from bs4 import BeautifulSoup, NavigableString
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

HEADINGS = ["h1", "h2", "h3", "h4", "h5", "h6"]
BLOCKS = {"p", "div", "li", "td", "th", "tr", "table", "ul", "ol", "section",
          "article", "blockquote", "pre"} | set(HEADINGS)
CELL_HOLDERS = {"li", "td", "th", "tr"}
VIDEO_HOSTS = ("youtube.com", "youtube-nocookie.com", "youtu.be", "vimeo.com")
# markdownify normally reduces images inside headings and table cells to their
# alt text; listing the parent tags here keeps them as real images.
KEEP_IMG_PARENTS = ["td", "th", "a", "span", "strong", "b", "em", "i", "p", "div",
                    "li", "figure", "picture", "center", "font"] + HEADINGS
HTML_TABLE_ATTRS = {"href", "src", "alt", "title", "colspan", "rowspan", "width", "height"}
SSI_ERROR_RE = re.compile(r"\[an error occurred while processing this directive\]", re.I)
FACTORY = BeautifulSoup("", "html.parser")


def slug(frag):
    """Normalise a #fragment so links and their targets always agree."""
    return re.sub(r"\s+", "-", unquote(frag).strip())


def md_href_to_html(href):
    """Raw-HTML links bypass jekyll-relative-links, so point them at .html."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or not re.search(r"\.md(#|$)", href):
        return href
    path, _, frag = href.partition("#")
    path = (path[:-8] or "./") if path.endswith("index.md") else path[:-3] + ".html"
    return path + ("#" + frag if frag else "")


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
        self.table_mode = args.tables
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
        self.stylesheets = set()
        self.css_rows = []     # (stylesheet, image url)
        self.css_mode = args.css_images
        self.extra_assets = [normalize(u) for u in (args.extra_asset or [])]

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
        for link in soup.find_all("link", href=True):
            if "stylesheet" in (link.get("rel") or []):
                css = normalize(urljoin(page_url, link["href"]))
                if urlparse(css).netloc in self.asset_hosts:
                    self.stylesheets.add(css)

    def enqueue(self, url):
        lp = self.page_path(url)
        if lp in self.page_paths:
            return
        self.page_paths[lp] = url
        self.queue.append(url)

    def same_page_fragment(self, href, page_url):
        href = (href or "").strip()
        if href.startswith("#"):
            return href[1:] or None
        if not href or href.lower().startswith(SKIP_PREFIXES):
            return None
        absolute = urljoin(page_url, href)
        if urlparse(absolute).fragment and normalize(absolute) == page_url:
            return urlparse(absolute).fragment
        return None

    def rewrite(self, root, page_url, page_file, ids):
        for el in root.find_all("a", href=True):
            frag = self.same_page_fragment(el["href"], page_url)
            if frag:
                key = slug(frag).lower()
                if key not in ids and key != "top":
                    print(f"    [anchor] #{frag} has no target on {page_url}")
                el["href"] = "#" + ids.get(key, slug(frag))
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
    def place_anchors(self, root, page_url):
        """Keep in-page link targets (id= / <a name=>) that the page links to."""
        wanted = set()
        for a in root.find_all("a", href=True):
            frag = self.same_page_fragment(a["href"], page_url)
            if frag:
                wanted.add(slug(frag).lower())
        ids, tokens = {}, []
        for el in list(root.find_all(True)):
            for val in (el.get("id"), el.get("name") if el.name == "a" else None):
                if not val or not isinstance(val, str):
                    continue
                key = slug(val).lower()
                if key not in wanted or key in ids:
                    continue
                ids[key] = slug(val)
                marker = f"ZZANCHOR{len(tokens)}ZZ"
                tokens.append(slug(val))
                block = el
                while block is not root and block.name not in BLOCKS and block.parent is not None:
                    block = block.parent
                if block is root:
                    el.insert_before(NavigableString(marker))
                elif block.name in CELL_HOLDERS:
                    block.insert(0, NavigableString(marker))
                else:
                    para = FACTORY.new_tag("p")
                    para.string = marker
                    block.insert_before(para)
        return ids, tokens

    def fix_headings(self, root):
        """Headings holding only an image become plain image paragraphs;
        truly empty headings are removed."""
        for h in list(root.find_all(HEADINGS)):
            if h.get_text("", strip=True).replace("\xa0", ""):
                continue
            if h.find(["img", "iframe"]):
                h.name = "p"
            else:
                h.decompose()

    def protect_videos(self, root, page_url, raw):
        for el in list(root.find_all(["iframe", "embed"])):
            src = el.get("src") or el.get("data-src") or ""
            absolute = urljoin(page_url, src.strip()) if src else ""
            host = urlparse(absolute).netloc.lower()
            if any(host == h or host.endswith("." + h) for h in VIDEO_HOSTS):
                w = el.get("width") if str(el.get("width", "")).isdigit() else "560"
                h = el.get("height") if str(el.get("height", "")).isdigit() else "315"
                title = htmlmod.escape(el.get("title") or "Embedded video", quote=True)
                markup = (f'<iframe src="{htmlmod.escape(absolute, quote=True)}" width="{w}" '
                          f'height="{h}" title="{title}" loading="lazy" allowfullscreen></iframe>')
                token = f"ZZRAW{len(raw)}ZZ"
                raw[token] = markup
                para = FACTORY.new_tag("p")
                para.string = token
                el.replace_with(para)
            else:
                el.decompose()

    @staticmethod
    def table_needs_html(table):
        """Markdown tables need a header row and single-line, simple cells."""
        rows = table.find_all("tr")
        if not rows:
            return False
        if table.find("table"):
            return True
        first = rows[0].find_all(["th", "td"])
        has_header = bool(table.find("thead")) or (bool(first) and all(c.name == "th" for c in first))
        if not has_header:
            return True
        for c in table.find_all(["td", "th"]):
            if int(c.get("colspan", 1) or 1) > 1 or int(c.get("rowspan", 1) or 1) > 1:
                return True
            if c.find(["ul", "ol", "pre", "blockquote", "iframe"] + HEADINGS):
                return True
        return False

    def handle_tables(self, root, raw):
        n_html = n_md = 0
        for table in list(root.find_all("table")):
            if table.find_parent("table") is not None:
                continue  # nested tables travel with their outer table
            as_html = (self.table_mode == "html" or
                       (self.table_mode == "auto" and self.table_needs_html(table)))
            if as_html:
                for el in table.find_all(True):
                    el.attrs = {k: v for k, v in el.attrs.items() if k in HTML_TABLE_ATTRS}
                    if el.name == "a" and el.get("href"):
                        el["href"] = md_href_to_html(el["href"])
                for el in table.find_all(["script", "style"]):
                    el.decompose()
                markup = re.sub(r"\n\s*\n+", "\n", str(table))
                token = f"ZZRAW{len(raw)}ZZ"
                raw[token] = markup
                para = FACTORY.new_tag("p")
                para.string = token
                table.replace_with(para)
                n_html += 1
            else:
                for cell in table.find_all(["td", "th"]):
                    for br in cell.find_all("br"):
                        br.replace_with(NavigableString(" ZZBRZZ "))
                    for blk in list(cell.find_all(["p", "div"])):
                        blk.append(NavigableString(" ZZBRZZ "))
                        blk.unwrap()
                n_md += 1
        return n_html, n_md

    @staticmethod
    def tidy(body):
        """Trim trailing spaces but keep two-space hard line breaks."""
        out = []
        for line in body.split("\n"):
            stripped = line.rstrip()
            if stripped and line.endswith("  ") and not stripped.lstrip().startswith("|"):
                stripped += "  "
            out.append(stripped)
        return "\n".join(out)

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

        # 3. structural fixes before conversion
        raw = {}
        ids, anchor_tokens = self.place_anchors(root, url)
        self.fix_headings(root)
        self.rewrite(root, url, page_file, ids)   # before tables are set aside as HTML
        self.protect_videos(root, url, raw)
        n_html, n_md = self.handle_tables(root, raw)

        # 4. convert and tidy
        body = to_markdown(str(root), heading_style="ATX", bullets="-",
                           keep_inline_images_in=KEEP_IMG_PARENTS)
        body = self.tidy(body)
        body = SSI_ERROR_RE.sub("", body)
        body = re.sub(r"^#{1,6}[ \t]*$\n?", "", body, flags=re.M)      # empty headings
        body = re.sub(r"ZZANCHOR(\d+)ZZ",
                      lambda m: f'<a id="{htmlmod.escape(anchor_tokens[int(m.group(1))], quote=True)}"></a>',
                      body)
        body = re.sub(r"(?:\s*ZZBRZZ\s*)+(?=\|)", " ", body)           # trailing break in cell
        body = re.sub(r"(?<=\|)(?:\s*ZZBRZZ\s*)+", " ", body)           # leading break in cell
        body = re.sub(r"\s*ZZBRZZ\s*", "<br>", body)
        body = re.sub(r"ZZRAW\d+ZZ", lambda m: raw[m.group(0)], body)
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
        if n_html or n_md:
            print(f"    tables: {n_md} markdown, {n_html} html")
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

    def scan_css(self):
        """Find images referenced from the site's stylesheets (backgrounds, banners)."""
        todo, seen = sorted(self.stylesheets), set()
        while todo:
            css = todo.pop()
            if css in seen:
                continue
            seen.add(css)
            try:
                r = self.get(css)
            except requests.RequestException as e:
                print(f"[css error] {css}: {e}")
                continue
            if r.status_code != 200:
                print(f"[css {r.status_code}] {css}")
                continue
            text = re.sub(r"/\*.*?\*/", "", r.text, flags=re.S)   # drop comments
            for m in re.finditer(r"@import\s+(?:url\()?['\"]?([^'\")\s;]+)", text):
                imp = normalize(urljoin(css, m.group(1)))
                if urlparse(imp).netloc in self.asset_hosts:
                    todo.append(imp)
            for m in re.finditer(r"url\(\s*['\"]?([^'\")]+?)['\"]?\s*\)", text):
                ref = m.group(1).strip()
                if ref.lower().startswith(("data:", "#")):
                    continue
                img = normalize(urljoin(css, ref))
                ext = os.path.splitext(unquote(urlparse(img).path))[1].lower()
                if urlparse(img).netloc in self.asset_hosts and ext in ASSET_EXTS:
                    if (css, img) not in self.css_rows:
                        self.css_rows.append((css, img))
                    if self.css_mode == "download":
                        self.assets.setdefault(img, css)
        print(f"Stylesheets scanned: {len(seen)}. Images referenced: "
              f"{len({i for _, i in self.css_rows})}")

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
        if self.css_rows:
            with open(self.out / "css_images.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["stylesheet", "image_url", "local_path_if_downloaded"])
                for css, img in self.css_rows:
                    w.writerow([css, img, Path(self.asset_path(img)).as_posix()])
        bad = sum(1 for r in self.rows if not r["status"].startswith("ok"))
        print(f"Wrote manifest.csv and broken_links.csv ({bad} problem rows) in {self.out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--start", default="https://www.dartmouth.edu/dbic/")
    ap.add_argument("--out", default="dbic-markdown")
    ap.add_argument("--delay", type=float, default=0.5,
                    help="seconds between requests (default 0.5)")
    ap.add_argument("--max-pages", type=int, default=0,
                    help="stop after N pages (0 = no limit); useful for testing")
    ap.add_argument("--selector",
                    help="CSS selector for the main content area; tried first")
    ap.add_argument("--strip", action="append",
                    help="extra CSS selector to remove from content (repeatable)")
    ap.add_argument("--tables", choices=["auto", "markdown", "html"], default="auto",
                    help="how to write tables: auto (default) keeps simple tables with a "
                         "header row as Markdown and layout/photo tables as clean HTML")
    ap.add_argument("--css-images", choices=["list", "download"],
                    help="scan linked stylesheets for url(...) images; 'list' only writes "
                         "css_images.csv, 'download' also fetches them as assets")
    ap.add_argument("--extra-asset", action="append",
                    help="URL of an extra file to download into assets/ (repeatable)")
    ap.add_argument("--asset-host", action="append",
                    help="extra host to download assets from (repeatable)")
    args = ap.parse_args()

    c = Crawler(args)
    try:
        c.crawl_pages()
        if c.css_mode:
            c.scan_css()
        for u in c.extra_assets:
            c.assets.setdefault(u, "(--extra-asset)")
        c.download_assets()
    except KeyboardInterrupt:
        print("\nInterrupted; writing reports for what was completed.")
    finally:
        c.write_reports()


if __name__ == "__main__":
    sys.exit(main())
