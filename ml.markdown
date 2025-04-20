---
layout: default
permalink: /ml/
---

# MSc Artificial Intelligence E-Portfolio Curriculum

This E-Portfolio outlines the curriculum and associated activities for the MSc Program in Artificial Intelligence and Machine Learning at the University of Essex.

## Units on Machine Learning November 2023

Each unit in this curriculum is designed to build upon the knowledge and skills in the Machine Learning November Module 2023. Below is a detailed breakdown of each unit, its components, e-Portfolio and formative activities.

{% for unit in site.data.ml_units %}
{% if unit.artifacts %}
{% include unit-card.html
  unit_number=unit.unit_number
  unit_title=unit.title
  unit_description=unit.description
  artifacts=unit.artifacts
%}
{% else %}

<div class="unit-card">
  <h3 id="unit-{{ unit.unit_number }}">Unit {{ unit.unit_number }}{% if unit.title %}: {{ unit.title }}{% endif %}</h3>
  {% if unit.description %}
  <p>{{ unit.description }}</p>
  {% endif %}
</div>
<hr />
{% endif %}
{% endfor %}

[back](./)
