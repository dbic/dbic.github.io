---
title: "DBIC Advisory Committee"
source_url: https://www.dartmouth.edu/dbic/people/advisorycommittee.html
retrieved: 2026-11-04
---

[Home](../index.md "Home") >
 [People](index.md) >

# DBIC Advisory Committee

 {%- for person in include.people %} {%- assign lines = person.Bio | split: " | " %}
{{ person.Name }}
{%- if person['Profile Link'] != "" %}{{ person.Name }}{% else %}{{ person.Name }}{% endif %} {%- for line in lines %}
{{ line }}{% endfor %}
{%- endfor %} 
