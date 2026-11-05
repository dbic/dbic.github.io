# DBIC new webpage

This is a project to redevelop https://www.dartmouth.edu/dbic/ as a GitHub Pages webpage.

The program `get-webpage.py` is what is used to pull the original content and convert HTML
to MD format.

## Stage 1: Import

To create the base branch, a program was usd to import from the current website
by trawling it.

Note that this import program does not handle everything... The
following are hand-made files created along the way (not produced by
the crawler, but generated as requested using Claude) and kept between
versions:

```
_config.yml
_layouts/default.html
_data/navigation.yml
```

(plus this `README.md`, `.gitignore`, etc.).

The crawler has a link checker built in, but it is quite limited: it
won't flag redirections (which may be "soft 404" results in actuality)
and doesn't check any links that aren't included in the conversion (so
no "external" links, including pages at dartmouth.edu).  The
`check_links.py` program was an add-on step used to double check links
in the converted verison, including external ones if `--external` is
supplied. (Link issues were addressed on the original.)

Note: we are ignoring the flagging of "http" links that redirect at
the webserver to "https" since they're handled automatically.

## Stage 2: Redesign

A new branch is being used for this stage, in which styles are tried.

The current approach uses a kind of "plug-in" style switcher, which
can be turned on by accessing any link with `?dev` added after it. A
small clickable menu button then appears in the bottom right, and
persists (`?dev=0` can disable if required).