#!/usr/bin/env python3
"""Checks _data/timeline.yml (run from the repository root, after editing it).
    python check_timeline.py [path]        # default: _data/timeline.yml
The file is read by Jekyll: a mistake in it (an unclosed quote, a wrong indent) stops the whole site from building, so this is worth running before committing.
It checks: the file reads as a list of events; each has a year (as text), a short text and a long text; the years are in date order, oldest first; the short texts
are short enough for the home page strip; "home" is true or false (a word in quotes would NOT hide an event); Markdown links are well formed; and how many events the
home strip will show. If PyYAML is installed it also reads the file the way Jekyll does. ERRORS must be fixed (exit code 1); WARNINGS are advice.
Works on Python 3.8 or newer."""
import re, sys
path = [a for a in sys.argv[1:] if not a.startswith("--")] or ["_data/timeline.yml"]; path = path[0]
try: text = open(path, encoding="utf-8-sig", newline="").read()
except OSError as e: print("cannot read %s: %s" % (path, e)); sys.exit(2)
errors, warns, ents = [], [], []
def E(m): errors.append("  " + m)
def W(m): warns.append("  " + m)
def scalar(v):
    v = v.strip()
    if v.startswith('"') and (len(v) < 2 or v[-1] != '"' or re.search(r'(?<!\\)"', v[1:-1])): return v, "badquote"           # an unclosed quote, or a quote inside the text that is not written \"
    if len(v) >= 2 and v[0] == v[-1] == '"': return v[1:-1].replace('\\"', '"').replace("\\\\", "\\"), "str"
    if len(v) >= 2 and v[0] == v[-1] == "'": return v[1:-1].replace("''", "'"), "str"
    if v in ("true", "false"): return v == "true", "bool"
    if re.match(r"^-?\d+$", v): return int(v), "int"
    return v, "plain"
try:
    import yaml
    data = yaml.safe_load(text)
    if data is None: pass                                            # only comments: reported below as "no events"
    elif not isinstance(data, list): E("the file must be a list of events, each starting with '- year:' (it reads as %s)" % type(data).__name__)
    else:
        for i, d in enumerate(data, 1):
            if not isinstance(d, dict): E("event %d is not a set of fields" % i); continue
            ents.append({k: (v, "bool" if isinstance(v, bool) else "int" if isinstance(v, int) else "str") for k, v in d.items()})
except ImportError:
    cur = None                                                       # a simple reader for the layout this file uses (PyYAML is not installed)
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"): continue
        m = re.match(r"^-[ \t]+(\w+):[ \t]*(.*)$", line)
        if m: cur = {}; ents.append(cur); cur[m.group(1)] = scalar(m.group(2)); continue
        m = re.match(r"^[ \t]+(\w+):[ \t]*(.*)$", line)
        if m and cur is not None: cur[m.group(1)] = scalar(m.group(2)); continue
        E("line %d is not in the form this file uses: %s" % (n, line.strip()[:60]))
except Exception as e:
    E("the file does not read as YAML (Jekyll would stop with an error): %s" % str(e).replace("\n", " ")[:200])
for i, e in enumerate(ents, 1):
    for k, v in e.items():
        if v[1] == "badquote": E("event %d: the text of '%s' has an unclosed or stray double quote (write \\\" for a quote inside the text, or the site will not build): %s" % (i, k, str(v[0])[:50]))
if not ents and not errors: E("the file has no events")
prev = None; home = 0
for i, e in enumerate(ents, 1):
    y = e.get("year"); lab = "event %d (%s)" % (i, y[0] if y else "no year")
    if not y: E("%s: it has no year" % lab); continue
    if y[1] != "str": E("%s: write the year in double quotes, for example \"1999\" (as a bare number it is treated as a number)" % lab)
    ym = re.match(r"\d{4}", str(y[0]))
    if not ym: E("%s: the year should start with four digits" % lab)
    elif prev is not None and int(ym.group(0)) < prev: E("%s: the events must be in date order, oldest first (this one is earlier than the one before)" % lab)
    if ym: prev = int(ym.group(0))
    s, l, h = e.get("short"), e.get("long"), e.get("home")
    if not s or not str(s[0]).strip(): E("%s: it has no 'short' text (for the home page strip)" % lab)
    elif len(str(s[0])) > 90: W("%s: the short text is %d characters; the strip is narrow, so about 80 or fewer is better" % (lab, len(str(s[0]))))
    if not l or not str(l[0]).strip(): W("%s: it has no 'long' text, so the History page will show the short text" % lab)
    else:
        for lt, url in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", str(l[0])):
            if not lt.strip() or not url.strip(): E("%s: a link in the long text is missing its words or its address" % lab)
            elif not re.match(r"^(https?://|/|#)", url.strip()): W("%s: the link address %s should start with https:// or /" % (lab, url.strip()[:40]))
        if re.search(r"\[[^\]]*\]\([^)]*$|\[[^\]]*$", str(l[0])): E("%s: a Markdown link in the long text is not closed" % lab)
        if "<" in str(l[0]): W("%s: the long text has an HTML tag; use Markdown links instead" % lab)
    if h is not None:
        if h[1] != "bool": E("%s: 'home' must be true or false without quotes (a word in quotes does not hide the event)" % lab)
        elif h[0] is False: continue
    home += 1
print("%s: %d event%s; the home strip will show %d" % (path, len(ents), "" if len(ents) == 1 else "s", home))
for i, e in enumerate(ents, 1):
    if e.get("year"): print("  %-6s %s%s" % (str(e["year"][0]), (str(e["short"][0]) if e.get("short") else "(no short text)")[:78], "" if not e.get("home") or e["home"][0] is not False else "   [not on the home strip]"))
if ents and home < 3: W("the home strip will show only %d events" % home)
if home > 7: W("the home strip will show %d events; more than 7 gets crowded" % home)
for label, items in (("ERRORS", errors), ("WARNINGS", warns)):
    if items: print("\n%s:\n%s" % (label, "\n".join(items)))
print("\n%d error%s, %d warning%s." % (len(errors), "" if len(errors) == 1 else "s", len(warns), "" if len(warns) == 1 else "s"))
sys.exit(1 if errors else 0)
