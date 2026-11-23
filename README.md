# DBIC website

The website of the Dartmouth Brain Imaging Center (DBIC), written in Markdown and published as a
GitHub Pages site at https://dbic.github.io. It began as an automatic conversion of
https://www.dartmouth.edu/dbic/ (Stage 1), was then redesigned (Stage 2), and finally had its content
reviewed and edited (Stage 3). The history is at the end of this file; the first sections are a road
map for anyone who needs to change something.

## How the site is put together

### Pages

Each page is a file that starts with a short block of "front matter" between two lines of `---`,
followed by the page itself. For example:

```
---
title: "Scanning rates"
lead: "One sentence, shown under the heading."
related:
  - { title: "Who to contact", url: "/contact.html" }
---

[Home](/) >

# Scanning rates

The text of the page...
```

Layouts have fields
*  `title`; `lead` (the introduction under the heading)
* `description` (this text is shown in searches)
* `glance` (cards under the heading)
* `actions` (buttons under the heading)
* `related` ("Keep exploring" buttons at the bottom)
* `faq_group` (adds the "Common questions" strip, from `_data/faq.yml`)
* `reviewed` (shows the date the page was last reviewed)
* `permalink` (web address)

In some cases there are additional fields `source_url` and `retrieved` from the conversion process.

Note that every page starts with a breadcrumb line and then a `# Heading`, and it will probably cause problems
if we try to put any image, list or table before the initial heading.

All `.md` files are being converted to HTML on the fly from Markdown. In some cases, files end in `.html`, in which case they are passed through as is (e.g., the home page). Note that any markdown entered into `.html` pages won't be processed as formatting!!

Links between pages can be written `[text](other_page.md)` or with paths from the site's root, `/folder/page.html` (a plugin turns them into web addresses). The link to the home page must be `/` (see Issue #1). To link to part of a page, put `<a id="name"></a>` above a heading and link to `page.html#name`. In the data files (the menu, the FAQs and so on) links need their full path from the root, starting with `/`.

### Layouts

All pages use `_layouts/default.html` (provides the title band, the cards and the "Keep exploring"
buttons), which is wrapped in `_layouts/redesign.html` (the header, the footer, the search box, the
styles and the script, in `assets/css/redesign.css` and `assets/js/redesign.js`).

The home page is built separately: `index.html` has only front matter (the title and the description
search engines show), and it uses `_layouts/home.html`, which assembles the page from one template per
section in `_includes/redesign/home/` (`hero`, `status`, `facility`, `research`, `community`, `people`
and `start`). The order of the sections is `sections:` in `_data/home.yml`, and each template reads its
text from a data file (see below).

### Where things live

| What | Where |
|---|---|
| Header menu, footer, and the topics the search finds first | `_data/menu.yml` |
| Section names in the breadcrumbs | `_data/sections.yml` |
| Home page text and the order of its sections | `_data/home.yml` |
| The "Where to next?" cards on the home page | `_data/start_here.yml` |
| Facility cards on the home page | `_data/facility.yml` |
| Research highlights on the home page | `_data/research_highlights.yml` |
| Logo and hero picture | `_data/brand.yml` |
| People pages (in the "Bio" column, a spaced vertical bar starts a new line) | `_data/directors_staff.csv`, `_data/affiliated_faculty.csv`, `_data/advisory_committee.csv` |
| Safety training sessions and brown bag talks | `_data/events.csv` |
| Scan-request windows | `_data/scan_windows.csv` |
| Datasets | `_data/datasets.csv` |
| Forms and other documents (the files are in `assets/dbic/docs/`) | `_data/documents.csv` |
| Questions and answers | `_data/faq.yml` |
| The steps on "How a study works" | `_data/study_steps.yml` |
| Safety rules on the safety page | `_data/safety.yml` |
| Groups on the Policies page | `_data/policy_groups.yml`, `_data/policy_documents.csv` |
| Linked programs | `_data/programs.yml` |
| Scanner calendar | `_data/calendar.yml` |

The pages are in folders: `policies/`, `research_infrastructure/` (the scanner, coils, sequences,
peripherals, the QA reports, Computing and Datasets), `people/`, `events/` and `videos/`, plus the pages
at the top level (`research-with-us.html`, `safety-compliance.html`, `data-computing.html` (the Datasets
overview), `faqs.md`, `contact.md`, `history.md`, and `404.md`). Pictures and documents are in `assets/`.

The page shown for an address that does not exist is `404.md`. It has `permalink: /404.html`, which is
how GitHub Pages knows to show it.

### Search

The search button in the header (or the `/` key) first offers the topics listed in `_data/menu.yml`,
then looks for the words in the text of the pages. The text search reads `assets/search-index.json`,
a file that is built, not written by hand. 

After changing page text or the data files, run

```
python build_search_index.py
```

and commit the output file `assets/search-index.json`. Running `python build_search_index.py --check` will
check for out of date entries. (If the index file is missing or old, the search still works for
the menu topics, it just can't include any newer text.)

## Routine tasks

(These instructions provided by Claude)

**Add or remove a safety training session.** Add or delete a row in `_data/events.csv` with the
category `Safety training` (spelled exactly like that). Copy a neighbouring row. Dates and deadlines are
written `2026-12-10`; the time is written like `10 a.m.–11:30 a.m.`. Sessions whose date has passed
disappear by themselves. They are shown on the Safety training page and on the home page. Then run
`python check_events.py`, which catches typos such as a wrong category or date. Brown bag talks are rows
of the same file, with the category `Brown bag`.

**Scan-request windows.** `_data/scan_windows.csv` has a row per month, with the dates the first two
tiers open and close and the date the third opens. It drives the cards that show the next window (on the
home page and the Scheduling page). The table of windows on the Scheduling page is typed by hand, so
change both.

**Add a form or document.** Put the file in `assets/dbic/docs/`, then add a row to
`_data/documents.csv` (a title, a category, the file's path, and whether it is featured).

**Add a question to the FAQs.** Add it to the right group of `_data/faq.yml`; the file starts with a note
that explains the fields.

**After any change,** run `python check_links.py` (add `--external` to test links to other websites),
`python check_events.py` if `_data/events.csv` changed, and `python build_search_index.py`.

## Conventions

(Notes from Claude)

The content review of November 2026 settled these. They are worth following when adding or editing text.

* **Terms.** scan operator (not "scanner operator" or "MRI operator"); scan buddy (defined on the MRI
  safety training page); MRI safety training; MRI Technologist; REDCap; DataLad; ReproStim; head coil;
  simultaneous multislice (SMS); email; HPC account (with "Discovery account" mentioned once, as another
  name for it). Say DBIC protocol, CPHS protocol or scan protocol, not just "protocol", where it could mean
  more than one of them.
* **Dates and times.** `Jan 5, 2026` for dates (and `Thursday, Nov 5` when there is no year); times as
  `8 a.m.–4 p.m.` and `10:30 a.m.–12 p.m.`, with an en dash and a non-breaking space before a.m. or p.m.;
  days as `Monday–Friday`. Dates in the data files stay as `2026-11-05`, which the site reads.
* **Code formatting.** File paths, folder names and group names in running text are written as code, like
  `/dartfs-hpc/scratch`. `fix_to_apply_backtick_formatting.py` applies this to the pages; run it again
  when you add text with paths.
* **Links.** The link text says where the link goes ("the HPC account request page", not "click here"). The
  site adds "(PDF)" or "(Word)" after a link to a document by itself, so do not type it.
* **Page names.** The Computing page covers storage and the Discovery cluster; Datasets is separate from
  it.

## Programs

These are kept in the top-level folder. They are not part of the published site.

* `get-webpage.py`: crawls a section of a website, converts each page to Markdown and downloads the
  linked documents (used in Stage 1).
* `check_links.py`: checks the links in the converted site. The internal checks always run: the target
  file exists with exactly the right capitals (GitHub Pages is case-sensitive), `x.html` links match
  `x.md`, and `#fragment` links match an anchor. With `--external` it also requests each link to another
  website and reports errors and permanent redirects. It was added after the crawler's own checker, which
  does not flag redirections and does not check links outside the conversion. Links that redirect from
  "http" to "https" at the web server are ignored, since they are handled automatically.
* `check_events.py`: checks the format of `_data/events.csv`, which unifies the safety training and
  brown bag listings. For example:

```
$ python check_events.py
_data/events.csv: 9 columns (date, time, category, title, detail, deadline, url, date_label, talk), 63 rows

rows per category:
    51  Brown bag
    12  Safety training

No problems found.
```

* `fix_home_links.py`: rewrites links to the site's top-level index file so that they point at `/`
  (a breadcrumb link written `../index.md` is not converted, and leads to a page that does not exist).
* `build_search_index.py`: builds `assets/search-index.json` for the search (see Search).
* `fix_to_apply_backtick_formatting.py`: puts paths in running text into code formatting (see Conventions).

## Notes from earlier stages

These are not used by any page of the current site. They can exist in branches for the earlier stages.

* `_includes/style-switcher.html` and `_data/styles.yml`: the style switcher of Stage 2 (a "Style"
  button that appeared when a link had `?dev` added). 
* `_includes/sidebar-nav.html`: the sidebar of Stage 1, which read `_data/navigation.yml`. 
* `redesign/index.html`: a stand-alone prototype of the redesigned home page. It has no front matter,
  so it is published as it is, and nothing links to it.
* `manifest.csv`, `broken_links.csv` and `link_report.csv`: reports written by the crawler and the link
  checker during Stage 1 (kept out of the current site by `_config.yml`).

## History

**Stage 1: Import.** To create the base branch, a program (`get-webpage.py`) imported the content of
https://www.dartmouth.edu/dbic/ by trawling it and converted the HTML to Markdown. The import program
does not handle everything. At that stage the files made by hand (generated as requested using Claude,
and kept between versions) were `_config.yml`, `_layouts/default.html` and `_data/navigation.yml`, plus
this `README.md`, `.gitignore` and similar files. Link problems found by the checkers were fixed on the
original site.

**Stage 2: Redesign.** The plain converted pages were replaced by the layouts, templates, data files and
styles described above. While styles were being tried, a switcher turned on by adding `?dev` to any
address was used; it is no longer connected.

**Stage 3: Content review.** In November 2026 the content of the whole site was reviewed and edited, page
by page. Pages were combined or renamed where that made them easier to use (for example, "Computer
resources" and "Using Discovery" merged to "Computing"), and the conventions above came out of it.
