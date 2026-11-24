#!/usr/bin/env python3
"""Checks the pictures in assets/images_for_auto_display/ (run from the repository root, before committing).
    python check_images.py
For each folder (each is a "tag": homepage, and later events, news, ...) it lists the pictures and warns about things that would make them look wrong
or slow the page down: names, file sizes, pixel sizes, shapes, duplicates and pictures that would not be used. ERRORS must be fixed (exit code 1);
WARNINGS are advice. It reads the size of JPEG, PNG, WebP and GIF files itself, so nothing needs installing. Works on Python 3.8 or newer."""
import hashlib, os, re, struct, sys
ROOT = "assets/images_for_auto_display"
CATEGORIES = {"homepage": {"ratio": 4 / 3, "max": 6, "min_width": 1000}}          # add a folder here once a page uses it
USED_EXT = {".jpg", ".jpeg", ".png", ".webp"}
WARN_KB, ERR_KB, WIDE = 300, 1024, 2400
def pixel_size(path):
    with open(path, "rb") as fh: d = fh.read()
    if d[:8] == b"\x89PNG\r\n\x1a\n": return struct.unpack(">II", d[16:24])
    if d[:6] in (b"GIF87a", b"GIF89a"): return struct.unpack("<HH", d[6:10])
    if d[:4] == b"RIFF" and d[8:12] == b"WEBP":
        k = d[12:16]
        if k == b"VP8 ": return struct.unpack("<H", d[26:28])[0] & 0x3FFF, struct.unpack("<H", d[28:30])[0] & 0x3FFF
        if k == b"VP8L": b = d[21:25]; return 1 + (((b[1] & 0x3F) << 8) | b[0]), 1 + (((b[3] & 0xF) << 10) | (b[2] << 2) | ((b[1] & 0xC0) >> 6))
        if k == b"VP8X": return 1 + int.from_bytes(d[24:27], "little"), 1 + int.from_bytes(d[27:30], "little")
    if d[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(d):
            if d[i] != 0xFF: i += 1; continue
            mk = d[i + 1]
            if mk in (0xD8, 0x01) or 0xD0 <= mk <= 0xD7 or mk == 0xFF: i += 2 if mk != 0xFF else 1; continue
            ln = struct.unpack(">H", d[i + 2:i + 4])[0]
            if mk in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF): h, w = struct.unpack(">HH", d[i + 5:i + 9]); return w, h
            i += 2 + ln
    return None
if not os.path.isdir(ROOT): print("%s does not exist: nothing to check." % ROOT); sys.exit(0)
errors = warns = 0
def say(level, name, msg):
    global errors, warns
    if level == "ERROR": errors += 1
    elif level == "warn": warns += 1
    print("  %-5s %s: %s" % (level, name, msg))
for cat in sorted(d for d in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, d))):
    folder = os.path.join(ROOT, cat); spec = CATEGORIES.get(cat)
    files = sorted(f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and not f.startswith("."))
    pics = [f for f in files if os.path.splitext(f)[1].lower() in (USED_EXT | {".gif", ".svg", ".avif"})]
    print("%s/  (%d picture%s)%s" % (cat, len(pics), "" if len(pics) == 1 else "s", "" if spec else "  -- no page uses this folder yet"))
    seen, prefixes = {}, {}
    for f in files:
        path = os.path.join(folder, f); stem, ext = os.path.splitext(f); kb = os.path.getsize(path) / 1024.0
        if f.lower() == "readme.md": continue
        if ext.lower() not in (USED_EXT | {".gif", ".svg", ".avif"}): say("warn", f, "not a picture the site uses (.jpg, .jpeg, .png or .webp): ignored"); continue
        if ext != ext.lower(): say("ERROR", f, "the extension must be lower-case (%s): the page ignores it" % ext.lower() + " as written")
        if ext.lower() in (".gif", ".svg", ".avif"): say("warn", f, "the %s format is not picked up (use .jpg, .jpeg, .png or .webp)" % ext.lower()); continue
        if not re.match(r"^[a-z0-9][a-z0-9_-]*$", stem): say("ERROR", f, "use only lower-case letters, digits, hyphens and underscores in the name (no spaces or capitals)")
        desc = stem.split("__")[-1]
        if re.match(r"^(img|dsc|dscn|dscf|image|photo|pic|screenshot|untitled|copy)[-_]?\d*$", desc) or len(re.findall(r"[a-z]{3,}", desc)) < 2: say("warn", f, "the name is the picture's description for people who cannot see it: describe what it shows, e.g. 02__researchers-in-the-control-room.jpg")
        mp = re.match(r"^(\d\d)__", stem)
        if mp: prefixes.setdefault(mp.group(1), []).append(f)
        sz = pixel_size(path)
        if sz is None: say("ERROR", f, "cannot read the picture (is it damaged, or not really a %s?)" % ext.lower()); continue
        w, h = sz
        if kb > ERR_KB: say("ERROR", f, "%d KB is too large for a page that loads several pictures (aim for under %d KB)" % (kb, WARN_KB))
        elif kb > WARN_KB: say("warn", f, "%d KB: larger than needed (aim for under %d KB)" % (kb, WARN_KB))
        if w > WIDE: say("warn", f, "%d pixels wide: more than the frame can show (about 1,200 to 1,600 is plenty); a smaller file loads faster" % w)
        if spec:
            if w < spec["min_width"]: say("warn", f, "only %d pixels wide: may look soft in the frame (aim for 1,200 or more)" % w)
            if abs((w / float(h)) / spec["ratio"] - 1) > 0.2: say("warn", f, "%dx%d is a different shape from the frame (4:3): a lot of it will be trimmed" % (w, h))
        dig = hashlib.md5(open(path, "rb").read()).hexdigest()
        if dig in seen: say("ERROR", f, "is an exact copy of %s in the same folder" % seen[dig])
        seen[dig] = f
    for pre, names in sorted(prefixes.items()):
        if len(names) > 1: say("warn", ", ".join(names), "share the order number %s: they will be shown in alphabetical order of the rest of the name" % pre)
    used = [f for f in pics if os.path.splitext(f)[1] == os.path.splitext(f)[1].lower() and os.path.splitext(f)[1] in USED_EXT]
    if spec and len(used) > spec["max"]: say("warn", cat, "%d pictures, but only the first %d (in file-name order) are used: %s" % (len(used), spec["max"], ", ".join(used[spec["max"]:])))
    if spec and not used: print("  (no pictures yet: the page looks as it does without a slideshow)")
print("\n%d error%s, %d warning%s." % (errors, "" if errors == 1 else "s", warns, "" if warns == 1 else "s"))
sys.exit(1 if errors else 0)
