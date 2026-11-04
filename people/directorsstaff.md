---
title: "Directors and staff"
source_url: https://www.dartmouth.edu/dbic/people/directorsstaff.html
retrieved: 2026-11-04
---

[Home](../index.md "Home") >
 [People](index.md) >

# Director and Staff

<div class="people">
{%- for person in site.data.directors_staff %}
{%- assign lines = person.Details | split: " | " %}
<div class="person">
<img src="{{ '/' | append: person['Local Image'] | relative_url }}" alt="{{ person.Name }}">
<div><a href="{{ person['Profile Link'] }}"><strong>{{ person.Name }}</strong></a>
{person.Bio}
{%- for line in lines %}<br>{{ line }}{% endfor %}</div>
</div>
{%- endfor %}
</div>
