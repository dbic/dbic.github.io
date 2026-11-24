#!/usr/bin/env python3
"""Build the search index for the title-bar search (review item ALL-15). Run from the repository root.
    python build_search_index.py            # writes assets/search-index.json
    python build_search_index.py --check    # says whether the file on disk is out of date (exit code 1 if it is); writes nothing
Run it again whenever page text or the data files change, before you commit; the search then finds the new text. If the index is out of date or
missing, the search still works for the menu topics: it only misses the newest page text.
What goes in: every page (title, one-line introduction, headings and text), the FAQ questions and answers (_data/faq.yml), the datasets
(_data/datasets.csv), the document library (_data/documents.csv), the brown-bag talks (_data/events.csv) and the people lists.
Uses only the Python standard library. Works on Python 3.8 or newer."""
import csv, html, io, json, re, sys
from pathlib import Path
ROOT = Path(".")
OUT = ROOT / "assets" / "search-index.json"
if not ((ROOT / "_data").is_dir() and (ROOT / "research_infrastructure").is_dir()): print("run this from the repository root"); sys.exit(1)
SKIP_DIRS = {"assets", "node_modules", "vendor", "redesign", "_site", "__MACOSX"}
SKIP_FILES = {"README.md", "readme.md", "new-location.md", "new-location.html"}
BODY_MAX = 7000
def read(p):
    with io.open(p, encoding="utf-8-sig", newline="") as fh: return fh.read().replace("\r\n", "\n")
def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        out, i, s = [], 0, v[1:-1]
        while i < len(s):
            c = s[i]
            if c == "\\" and i + 1 < len(s):
                n = s[i + 1]; out.append({"n": "\n", "t": "\t", '"': '"', "\\": "\\", "/": "/"}.get(n, n)); i += 2
            else: out.append(c); i += 1
        return "".join(out)
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'": return v[1:-1].replace("''", "'")
    return v
def plain(t):
    t = re.sub(r"(?m)^[ \t]*\{:[^}\n]*\}[ \t]*$", " ", t)                                     # kramdown attribute lines such as {: .note role="note" } are not text
    t = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", t); t = re.sub(r"\{%-?.*?-?%\}|\{\{.*?\}\}", " ", t, flags=re.S); t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<br\s*/?>|<wbr\s*/?>", " ", t); t = re.sub(r"<[^>]+>", " ", t); t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t); t = re.sub(r"<(https?://[^>\s]+)>", " ", t); t = re.sub(r"https?://\S+|mailto:\S+", " ", t)
    t = html.unescape(t); t = re.sub(r"(?m)^\s*#{1,6}\s*", "", t); t = re.sub(r"[`*_|>]+", " ", t); t = re.sub(r"(?m)^\s*[-+]\s+", "", t); t = re.sub(r"-{3,}", " ", t)
    t = re.sub(r"\\([*_`\\\[\]()#.!-])", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()
def fm_value(fm, key):
    m = re.search(r"(?m)^" + re.escape(key) + r":[ \t]*(.*)$", fm)
    return unquote(m.group(1)) if m and m.group(1).strip() not in ("", "|", ">") else ""
GROUP = {"policies": "Policies", "research_infrastructure": "Facility & data", "people": "People", "events": "Events", "videos": "Video"}
docs = []
def add(t, u, g, l="", h="", b=""):
    t, l, h, b = plain(t), plain(l), plain(h), plain(b)
    if t: docs.append({"t": t, "u": u, "g": g, "l": l, "h": h, "b": b[:BODY_MAX]})
def timeline_text():
    """The years and the long texts of _data/timeline.yml (for the page that shows the whole timeline)."""
    t = ROOT / "_data" / "timeline.yml"
    if not t.exists(): return ""
    out = []
    for m in re.finditer(r'(?m)^-[ \t]+year:[ \t]*"([^"]*)"[ \t]*\r?\n(?:[ \t]+short:[^\n]*\n)?[ \t]+long:[ \t]*"((?:[^"\\]|\\.)*)"', read(t)): out.append(m.group(1) + " " + m.group(2).replace('\\"', '"'))
    return " ".join(out)
# ---- pages
for p in sorted(ROOT.rglob("*")):
    if not p.is_file() or p.suffix not in (".md", ".html"): continue
    rel = p.relative_to(ROOT); parts = rel.parts
    if any(x in SKIP_DIRS or x.startswith(("_", ".")) for x in parts[:-1]) or parts[-1] in SKIP_FILES or parts[-1].startswith(("404", "search")): continue
    raw = read(p); m = re.match(r"---\n(.*?)\n---\n?", raw, re.S)
    if not m: continue                                   # Jekyll only builds files that have front matter
    fm, body = m.group(1), raw[m.end():]
    if re.search(r"(?m)^search_exclude:[ \t]*true", fm): continue
    if re.search(r"(?m)^published:[ \t]*false", fm): continue
    h1 = re.search(r"(?m)^# (.+)$", body) or re.search(r"(?is)<h1[^>]*>(.*?)</h1>", body)
    title = fm_value(fm, "title") or (plain(h1.group(1)) if h1 else p.stem)
    lead = fm_value(fm, "lead") or fm_value(fm, "summary")
    perm = fm_value(fm, "permalink"); d, f = rel.parent.as_posix(), rel.name
    if perm: url = perm
    elif rel.stem == "index": url = "/" if d == "." else "/" + d + "/"
    else: url = "/" + ("" if d == "." else d + "/") + rel.stem + ".html"
    heads = re.findall(r"(?m)^#{2,3}[ \t]+(.+)$", body) or re.findall(r"(?is)<h[23][^>]*>(.*?)</h[23]>", body)
    if "redesign/timeline.html" in body: body = body + " " + timeline_text()       # the list on that page is drawn from _data/timeline.yml, so its text is added here
    add(title, url, GROUP.get(parts[0], "Site") if len(parts) > 1 else "Site", lead, " · ".join(plain(x) for x in heads), body)
# ---- data: FAQ questions and answers (the one-line and the multi-line formats)
faq = ROOT / "_data" / "faq.yml"
if faq.exists():
    cur = None
    def flush():
        global cur
        if cur and cur.get("q"): add(cur["q"], cur.get("url", "/faqs.html"), "FAQ", "", "", cur.get("a", ""))
        cur = None
    for line in read(faq).split("\n"):
        s = line.strip()
        if s.startswith("#") or not s: continue
        m = re.match(r"-\s*\{(.*)\}\s*$", s)                  # - { q: "…", url: "…" }
        if m:
            flush(); cur = {}
            for k, v in re.findall(r'(\w+):\s*("(?:[^"\\]|\\.)*"|\'[^\']*\')', m.group(1)): cur[k] = unquote(v)
            flush(); continue
        m = re.match(r"-\s*q:\s*(.+)$", s)                    # - q: "…"   (then a: and url: on the next lines)
        if m: flush(); cur = {"q": unquote(m.group(1))}; continue
        m = re.match(r"(a|url):\s*(.+)$", s)
        if m and cur is not None: cur[m.group(1)] = unquote(m.group(2))
    flush()
# ---- data: datasets, documents, brown-bag talks, people
def rows(name):
    p = ROOT / "_data" / name
    if not p.exists(): return []
    with io.open(p, encoding="utf-8-sig", newline="") as fh: return list(csv.DictReader(fh))
for r in rows("datasets.csv"): add(r.get("name", ""), "/research_infrastructure/datasets.html" + ("#" + r["anchor"] if r.get("anchor") else ""), "Datasets", r.get("description", ""), "", r.get("keywords", ""))
for r in rows("documents.csv"): add(r.get("title", ""), "/policies/forms_templates.html", "Documents & forms", r.get("category", ""), "", r.get("note", ""))
for r in rows("events.csv"):
    if (r.get("category") or "").strip() == "Brown bag": add(r.get("title", ""), "/events/fbb.html", "Brown bags", r.get("talk", ""), "", " ".join(x for x in (r.get("detail", ""), r.get("date_label", "") or r.get("date", "")) if x))
for name, url, grp in (("directors_staff.csv", "/people/directorsstaff.html", "People"), ("affiliated_faculty.csv", "/people/affiliated.html", "People"), ("advisory_committee.csv", "/people/advisorycommittee.html", "People")):
    for r in rows(name): add(r.get("Name", ""), url, grp, "", "", " ".join(x for x in (r.get("Bio", ""), r.get("Details", "")) if x))
docs.sort(key=lambda d: (d["u"], d["t"], d["g"]))
data = (json.dumps({"v": 1, "docs": docs}, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
if "--check" in sys.argv:
    cur_bytes = OUT.read_bytes() if OUT.exists() else None
    if cur_bytes == data: print("The search index is up to date (%d entries)." % len(docs)); sys.exit(0)
    print("The search index is OUT OF DATE or missing. Run:  python build_search_index.py"); sys.exit(1)
OUT.parent.mkdir(parents=True, exist_ok=True)
with io.open(OUT, "wb") as fh: fh.write(data)
print("Wrote %s: %d entries, %d KB." % (OUT.as_posix(), len(docs), len(data) // 1024))
