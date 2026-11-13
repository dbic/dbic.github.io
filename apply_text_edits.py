#!/usr/bin/env python3
"""Text edits from the content review: ALL-4 (descriptive links), ALL-5 (numbers stated once), ALL-6 (dates and
"Last reviewed"), ALL-7 (sentence-case headings). Run from the repository root.
    python apply_text_edits.py                 # preview
    python apply_text_edits.py --apply         # write the changes
    python apply_text_edits.py --only ALL-7    # limit to one item (also works with --apply)
Every edit is an exact find-and-replace. If the text is not found (you changed it) or is already in the new form, the
edit is skipped and reported, never forced. The Code of Conduct page is not touched (it is parked; see ALL-6 notes)."""
import re, sys
from pathlib import Path
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
D, P, R_ = "research_infrastructure/datasets.md", "policies/", "research_infrastructure/"
SCHED = "/policies/scheduling.html#scanhours"
E = []          # (item, file, old, new, count, is_regex)
def e(item, f, old, new, count=1, rx=False): E.append((item, f, old, new, count, rx))

# ---------------------------------------------------------------- ALL-4: descriptive link text
e("ALL-4", P + "safetytraining.md", 'the CITI Online Tutorial found [here](https://www.dartmouth.edu/~cphs/tosubmit/education/index.html "CITI Training").', 'the CITI Online Tutorial found on the [Dartmouth CPHS education requirements page](https://www.dartmouth.edu/~cphs/tosubmit/education/index.html "CITI Training").')
e("ALL-4", P + "scheduling.md", "viewed online [here](#calendar).", "viewed online [on this page](#calendar).")
e("ALL-4", P + "scheduling.md", "is available [here.](dbic_billing.md) An approved DBIC protocol", "is available on the [scanning rates page](dbic_billing.md). An approved DBIC protocol")
e("ALL-4", P + "scheduling.md", "can be found [here.](dbic_protocol.md)", "can be found on the [protocol page](dbic_protocol.md).")
e("ALL-4", P + "housekeeping.md", "[housekeeping checklist,](../assets/dbic/docs/policies/housekeeping01282026.pdf) in addition", "[housekeeping checklist](../assets/dbic/docs/policies/housekeeping01282026.pdf), in addition")
e("ALL-4", D, "can be found [here](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/).", "can be found on the [HBN website](https://fcon_1000.projects.nitrc.org/indi/cmi_healthy_brain_network/).")
e("ALL-4", D, "can be found [here](https://www.sciencedirect.com/science/article/abs/pii/S0896627325006610).", "can be found on [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0896627325006610).")
e("ALL-4", D, "(see: <https://www.datalad.org/>)", "(see the [DataLad website](https://www.datalad.org/))")
e("ALL-4", D, "**Link to DUA:** <https://forms.gle/eT4jHxaWwYUDEf2i9>", "**Link to DUA:** [NSD data use agreement form](https://forms.gle/eT4jHxaWwYUDEf2i9)")
e("ALL-4", D, "- <http://naturalscenesdataset.org>", "- [Natural Scenes Dataset website](http://naturalscenesdataset.org)")
e("ALL-4", D, "**Link to DUA**: <https://balsa.wustl.edu/project?project=HCP_YA>", "**Link to DUA**: [HCP Young Adult data use agreement (BALSA)](https://balsa.wustl.edu/project?project=HCP_YA)")
e("ALL-4", D, "- <https://www.humanconnectome.org/study/hcp-young-adult>", "- [HCP Young Adult website](https://www.humanconnectome.org/study/hcp-young-adult)")
e("ALL-4", D, "- <https://www.nature.com/articles/sdata2017181>", "- [Healthy Brain Network data descriptor (Scientific Data, 2017)](https://www.nature.com/articles/sdata2017181)")
e("ALL-4", D, "- [https://www.sciencedirect.com/science/article/pii/S0896627325006610](https://www.sciencedirect.com/science/article/abs/pii/S0896627325006610)", "- [Reproducible Brain Charts paper (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0896627325006610)")
e("ALL-4", D, "Dataset documentation: <https://individual-brain-charting.github.io/docs/index.html> (EBRAINS), <https://openneuro.org/datasets/ds002685/versions/2.0.0>(OpenNeuro)", "Dataset documentation: [IBC documentation (EBRAINS version)](https://individual-brain-charting.github.io/docs/index.html), [OpenNeuro dataset ds002685](https://openneuro.org/datasets/ds002685/versions/2.0.0)")
e("ALL-4", D, "the ImageNet terms of access (<https://www.image-net.org/download.php>)", "the [ImageNet terms of access](https://www.image-net.org/download.php)")
e("ALL-4", D, "Dataset documentation: <https://openneuro.org/datasets/ds007070/versions/1.0.3> (OpenNeuro)", "Dataset documentation: [OpenNeuro dataset ds007070](https://openneuro.org/datasets/ds007070/versions/1.0.3)")
e("ALL-4", D, "Datalad Repository: <https://datasets.datalad.org/?dir=/labs/haxby/life>", "[DataLad repository for the Life dataset](https://datasets.datalad.org/?dir=/labs/haxby/life)")
e("ALL-4", R_ + "computer_resources.md", '([bids.neuroimaging.io](https://bids.neuroimaging.io/ "BIDS"))', '([BIDS website](https://bids.neuroimaging.io/ "BIDS"))')
e("ALL-4", R_ + "computer_resources.md", "([http://centerforopenneuroscience.org](http://centerforopenneuroscience.org/", "([Center for Open Neuroscience](http://centerforopenneuroscience.org/")
e("ALL-4", R_ + "computer_resources.md", '([https://nifti.nimh.nih.gov](https://nifti.nimh.nih.gov "NIFTI"))', '([NIfTI website](https://nifti.nimh.nih.gov "NIFTI"))')
e("ALL-4", R_ + "computer_resources.md", r'can be found at\s+\[https://www\.datalad\.org\]\(https://www\.datalad\.org "DataLad"\)\.', 'can be found on the [DataLad website](https://www.datalad.org "DataLad").', 1, True)
e("ALL-4", R_ + "discovery.md", "Reference link: [https://services.dartmouth.edu/TDClient/1806/Portal/Requests/ServiceCatalog?CategoryID=11669](https://services.dartmouth.edu/TDClient/1806/Portal/Requests/ServiceCatalog?CategoryID=11669)", "[Dartmouth Services Portal: High Performance Computing](https://services.dartmouth.edu/TDClient/1806/Portal/Requests/ServiceCatalog?CategoryID=11669)")
e("ALL-4", R_ + "peripherals.md", "or check out ReproStim on GitHub: <https://github.com/ReproNim/reprostim>", "or check out [ReproStim on GitHub](https://github.com/ReproNim/reprostim)")
e("ALL-4", R_ + "qualityassurance.md", r"can be found at\s+<https://www\.nitrc\.org/projects/fbirn> and", "can be found on the [NITRC fBIRN project page](https://www.nitrc.org/projects/fbirn) and", 1, True)
e("ALL-4", R_ + "qualityassurance.md", "3. <https://www.nitrc.org/projects/bxh_xcede_tools>", "3. [BXH/XCEDE tools (NITRC project page)](https://www.nitrc.org/projects/bxh_xcede_tools)")
e("ALL-4", R_ + "sequences.md", "You can learn more about these sequences here: <https://www.cmrr.umn.edu/multiband/Multi-Band_C2P_Instructions_R016a.pdf>", "You can learn more about these sequences in the [CMRR multiband instructions](https://www.cmrr.umn.edu/multiband/Multi-Band_C2P_Instructions_R016a.pdf).")

# ---------------------------------------------------------------- ALL-5: each number stated once (on the page that owns it)
e("ALL-5", "_data/study_steps.yml", "an in-person session with the MRI technologist (up to four people per class) plus an online module.", "an in-person session with the MRI technologist plus an online module.")
e("ALL-5", "_data/study_steps.yml", "complete at least 10 hours of hands-on training with a certified operator, and pass a final competency check", "complete hands-on training with a certified operator, and pass a final competency check")
e("ALL-5", "_data/study_steps.yml", "Peak hours are weekdays 8 a.m. to 4 p.m. Evenings and weekends need both a certified operator and a [scan buddy](/policies/safetytraining.html#scanbuddy).", "Evenings and weekends need both a certified operator and a [scan buddy](/policies/safetytraining.html#scanbuddy); the [scan hours](" + SCHED + ") are on the scheduling page.")
e("ALL-5", "_data/safety.yml", "operator certification requires at least 10 hours of hands-on training.", "operator certification requires hands-on training with a certified operator.")
e("ALL-5", "_data/events.csv", ",MRI safety training,Up to 4 per class,", ",MRI safety training,,", 12)
e("ALL-5", P + "dbic_billing.md", "<td>8:00am-4:00pm</td>", '<td>peak hours (see <a href="' + SCHED + '">scan hours</a>)</td>')
e("ALL-5", P + "dbic_billing.md", "<td>after 4:00pm</td>", '<td>off-peak hours (see <a href="' + SCHED + '">scan hours</a>)</td>')
e("ALL-5", P + "scheduling.md", "## **Scan hours**", '<a id="scanhours"></a>\n\n## **Scan hours**')

# ---------------------------------------------------------------- ALL-6: no wording that depends on when it was written; last reviewed
e("ALL-6", P + "cancellations.md", "the DBIC will be implementing the following cancellation policy, effective September 1, 2021, for cancellations on/after October 1, 2021.", "the DBIC has the following cancellation policy, effective September 1, 2021, for cancellations on or after October 1, 2021.")
e("ALL-6", "history.md", r"scanner, which is still in use today\.", "scanner.", 1, True)
e("ALL-6", P + "dbic_billing.md", "Rates for scanning effective July 1, 2021\n\nLast reviewed July 1, 2026.\n", "Rates for scanning effective July 1, 2021\n")
REVIEWED = "July 1, 2026"
REVIEWED_PAGES = [P + n for n in ("scheduling.md", "safetytraining.md", "operator_training.md", "cancellations.md", "dbic_billing.md", "dbic_protocol.md", "dbic_parking.md", "housekeeping.md", "codeofconduct.md")]
OPTIONAL = {P + "codeofconduct.md"}      # parked for now (see park_code_of_conduct.py): skipped while it is not on the site

# ---------------------------------------------------------------- ALL-7: sentence-case headings (acronyms and names keep their capitals)
def both(f, old, new):          # page title (front matter) and the matching first heading
    e("ALL-7", f, f'title: "{old}"', f'title: "{new}"'); e("ALL-7", f, f"\n# {old}\n", f"\n# {new}\n")
both(P + "dbic_protocol.md", "DBIC Protocol", "DBIC protocol")
both(P + "forms_templates.md", "Forms & Templates", "Forms & templates")
both(P + "safetytraining.md", "MRI Safety Training", "MRI safety training")
both(P + "scheduling.md", "DBIC Scheduling", "DBIC scheduling")
both(R_ + "computer_resources.md", "Computer Resources", "Computer resources")
both(R_ + "fmri_scanner.md", "fMRI Scanner", "fMRI scanner")
both(P + "codeofconduct.md", "Code of Conduct", "Code of conduct")
both("people/affiliated.md", "Affiliated Faculty", "Affiliated faculty")
e("ALL-7", "people/directorsstaff.md", "\n# Director and Staff\n", "\n# Director and staff\n")
both("new-location.md", "This Page Has Moved", "This page has moved")
for y in (2020, 2021, 2022, 2024, 2025): both(R_ + f"qa_{y}.md", f"{y} QA Reports", f"{y} QA reports")
e("ALL-7", R_ + "qa_2019.md", 'title: "2019 QA Reports"', 'title: "2019 QA reports"')
both(R_ + "qa_2026.md", "QA Reports 2026", "QA reports 2026")
e("ALL-7", P + "scheduling.md", "### **Tier 1 – Grant-funded (External funding)**", "### **Tier 1 – Grant-funded (external funding)**")
for old, new in (("## DBIC Systems Access", "## DBIC systems access"), ("## Data Storage and Access", "## Data storage and access"), ("## Accessing BIDS data using Datalad", "## Accessing BIDS data using DataLad"), ("## DBIC Internal", "## DBIC internal")):
    e("ALL-7", R_ + "computer_resources.md", "\n" + old + "\n", "\n" + new + "\n")
e("ALL-7", R_ + "discovery.md", "\n# DBIC Policy for Computing Resources on Discovery\n", "\n# DBIC policy for computing resources on Discovery\n")
e("ALL-7", R_ + "discovery.md", r"^## Using DBIC.s Allocation$", "## Using DBIC's allocation", 1, True)
for old, new in (("## Cluster Usage", "## Cluster usage"), ("### Individual User Limits on Trackable Resources and Quality of Service", "### Individual user limits on trackable resources and quality of service"), ("### Queue Priority", "### Queue priority"), ("## Best Practices Guidelines for SLURM Cluster Usage", "## Best practices guidelines for SLURM cluster usage"), ("## Storage space on Discovery Hard drives", "## Storage space on Discovery hard drives"), ("### Temporary Scratch Space", "### Temporary scratch space")):
    e("ALL-7", R_ + "discovery.md", "\n" + old + "\n", "\n" + new + "\n")
for old, new in (("### Panasonic PT-DW750BU Projector", "### Panasonic PT-DW750BU projector"), ("### Audio Stimulus (Sensimetrics Model S14)", "### Audio stimulus (Sensimetrics Model S14)"), ("## participant Response devices", "## Participant response devices"), ("### Current Designs 932 Interface", "### Current Designs 932 interface"), ("### 4-Button Bimanual", "### 4-button bimanual"), ("### SR RESEARCH EYELINK 1000 PLUS", "### SR Research EyeLink 1000 Plus"), ("## EYETRaCKING", "## Eye tracking"), ("## Reprostim", "## ReproStim"), ("- [Eyetracking](#eyetracking)", "- [Eye tracking](#eyetracking)"), ("- [Reprostim](#reprostim)", "- [ReproStim](#reprostim)"), ('grid: ["participant Response devices"]', 'grid: ["Participant response devices"]')):
    e("ALL-7", R_ + "peripherals.md", old, new)
e("ALL-7", R_ + "qualityassurance.md", "\n## Weekly qa metrics\n", "\n## Weekly QA metrics\n")
e("ALL-7", R_ + "sequences.md", "\n## Sequence Settings\n", "\n## Sequence settings\n"); e("ALL-7", R_ + "sequences.md", 'listcards: ["Sequence Settings"]', 'listcards: ["Sequence settings"]')
e("ALL-7", "faqs.md", "\n## Scanning in the dbic\n", "\n## Scanning in the DBIC\n")

# ---------------------------------------------------------------- run
texts, report = {}, []
def load(f):
    if f not in texts:
        p = Path(f)
        if not p.exists():
            if f in OPTIONAL: return None
            print(f"missing file {f}: run this from the repository root"); sys.exit(1)
        texts[f] = p.read_text(encoding="utf-8")
    return texts[f]
for item, f, old, new, n, rx in E:
    if ONLY and item != ONLY: continue
    t = load(f)
    if t is None: report.append((item, "skipped (page is parked)", f, old)); continue
    if rx:
        cnt = len(re.findall(old, t, re.M))
        if cnt == n: texts[f] = re.sub(old, new, t, flags=re.M); report.append((item, "ok", f, old)); continue
        done = new in t
    else:
        if old in new and t.count(new) >= n:       # the new text contains the old (an insertion): already there
            report.append((item, "already done", f, old)); continue
        if t.count(old) == n: texts[f] = t.replace(old, new); report.append((item, "ok", f, old)); continue
        done = (old not in t) and (new in t)
    report.append((item, "already done" if done else f"NOT FOUND (found {t.count(old) if not rx else cnt}, expected {n}): change this one by hand", f, old))
if not ONLY or ONLY == "ALL-6":      # the "Last reviewed" date goes in each policy page's front matter
    for f in REVIEWED_PAGES:
        t = load(f)
        if t is None: report.append(("ALL-6", "skipped (page is parked)", f, "reviewed:")); continue
        m = re.match(r"(---\n)(.*?)(\n---\n)", t, re.S)
        if not m: report.append(("ALL-6", "NOT FOUND (no front matter): add reviewed: \"" + REVIEWED + "\" by hand", f, "")); continue
        if re.search(r"^reviewed:", m.group(2), re.M): report.append(("ALL-6", "already done", f, "reviewed:")); continue
        lines = m.group(2).split("\n"); i = next((k for k, l in enumerate(lines) if l.startswith("title:")), 0)
        lines.insert(i + 1, f'reviewed: "{REVIEWED}"'); texts[f] = m.group(1) + "\n".join(lines) + t[m.end(2):]; report.append(("ALL-6", "ok", f, 'reviewed: "' + REVIEWED + '"'))
for item, status, f, old in report:
    print(f"{item:6} {status:12} {f.split('/')[-1]:24} {old[:60]!r}" if status in ("ok", "already done") or status.startswith("skipped") else f"{item:6} {status}\n         {f}: {old[:80]!r}")
from collections import Counter
c = Counter((i, "ok" if s == "ok" else "done" if s == "already done" else "skipped" if s.startswith("skipped") else "NOT FOUND") for i, s, *_ in report)
print("\n" + "; ".join(f"{i}: {c[(i, 'ok')]} edits" + (f", {c[(i, 'done')]} already done" if c[(i, 'done')] else "") + (f", {c[(i, 'skipped')]} skipped (parked page)" if c[(i, 'skipped')] else "") + (f", {c[(i, 'NOT FOUND')]} NOT FOUND" if c[(i, 'NOT FOUND')] else "") for i in sorted({r[0] for r in report})))
if APPLY:
    for f, t in texts.items(): Path(f).write_text(t, encoding="utf-8")
    print("changes written.")
else: print("Preview only. Run again with --apply to write the changes.")
