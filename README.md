# DBIC new webpage

This is a project to redevelop https://www.dartmouth.edu/dbic/ as a GitHub Pages webpage.

The program `get-webpage.py` is what is used to pull the original content and convert HTML
to MD format.

## Import Notes

The main program does not handle everything... The following are hand-made files to keep
between versions (not produced by the crawler)

```
_config.yml
_layouts/default.html
_data/navigation.yml
```

(plus this `README.md`, `.gitignore`, etc.).

There is a link checker built in, but it is quite limited: it won't flag redirections
(which may be "soft 404" results in actuality) and doesn't check any links that aren't
included in the conversion (so no "external" links, including pages at dartmouth.edu).
The `check_links.py` program can be used to check links in the converted verison,
including external ones if `--external` is supplied.

Note: we are ignoring the flagging of "http" links that redirect at the webserver to
"https" since they're handled automatically.