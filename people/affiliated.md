---
title: "Affiliated Faculty"
source_url: https://www.dartmouth.edu/dbic/people/affiliated.html
retrieved: 2026-11-04
---

[Home](../index.md "Home") >
 [People](index.md) >

# Affiliated Faculty

The DBIC scanner is utilized by an interdisciplinary community of scientists and scholars who are engaged in neuroscience research at Dartmouth.

<div class="people">
{%- for person in site.data.affiliated_faculty %}
{%- assign lines = person.Bio | split: " | " %}
<div class="person">
<img src="{{ '/' | append: person['Local Image'] | relative_url }}" alt="{{ person.Name }}">
<div><a href="{{ person['Profile Link'] }}"><strong>{{ person.Name }}</strong></a>
{%- for line in lines %}<br>{{ line }}{% endfor %}</div>
</div>
{%- endfor %}
</div>
