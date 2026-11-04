---
title: "DBIC Advisory Committee"
source_url: https://www.dartmouth.edu/dbic/people/advisorycommittee.html
retrieved: 2026-11-04
---

[Home](../index.md "Home") >
 [People](index.md) >

# DBIC Advisory Committee

<div class="people">
{%- for person in site.data.advisory_committee %}
{%- assign lines = person.Bio | split: " | " %}
<div class="person">
<img src="{{ '/' | append: person['Local Image'] | relative_url }}" alt="{{ person.Name }}">
<div><a href="{{ person['Profile Link'] }}"><strong>{{ person.Name }}</strong></a>
{%- for line in lines %}<br>{{ line }}{% endfor %}</div>
</div>
{%- endfor %}
</div>
