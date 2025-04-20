---
layout: default
permalink: /ia/
---

# Intelligent Agents January 2025 E-Portfolio

This E-Portfolio outlines the curriculum and associated activities for the Intelligent Agents module in the MSc Program in Artificial Intelligence and Machine Learning at the University of Essex.

## Module Overview

The Intelligent Agents module explores the theory and practice of developing agent-based systems. This includes agent architectures, communication languages, learning mechanisms, and practical applications of intelligent agents.

## Units on Intelligent Agents January 2025

Each unit in this curriculum is designed to build understanding of intelligent agent systems. Below is a detailed breakdown of each unit, its components, and activities.

{% for unit in site.data.ia_units %}
{% if unit.artifacts.size > 0 %}
{% include ia-unit-card.html 
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
