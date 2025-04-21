---
layout: default
permalink: /ia/
---

# Intelligent Agents 2025

<div class="module-container">
  <div class="module-sidebar">
    {% include module-navigation.html units=site.data.ia_units module_title="Intelligent Agents" %}
  </div>
  
  <div class="module-content">
    <div class="welcome-banner">
      <h2>Intelligent Agents Module</h2>
      <p>This section contains all my work for the Intelligent Agents module from January 2025. The module explores agent architectures, communication languages, learning mechanisms, and practical applications of intelligent agents in various domains.</p>
    </div>
    
    {% for unit in site.data.ia_units %}
    {% if unit.artifacts.size > 0 %}
    {% include ia-unit-card.html
      unit_number=unit.unit_number
      unit_title=unit.title
      unit_description=unit.description
      artifacts=unit.artifacts
      content=unit.content
      references=unit.references
    %}
    {% else %}
    <div class="unit-card" id="unit-{{ unit.unit_number }}">
      <div class="unit-header">
        <span class="unit-number">{{ unit.unit_number }}</span>
        <h3>{% if unit.title %}{{ unit.title }}{% else %}Unit {{ unit.unit_number }}{% endif %}</h3>
      
      </div>
      
      {% if unit.description %}
      <div class="unit-description">
        <p>{{ unit.description }}</p>
      </div>
      {% endif %}
      
      {% if unit.content %}
      <div id="unit-content-{{ unit.unit_number }}" class="unit-content collapsed">
        {{ unit.content }}
        
        {% if unit.references %}
        <div class="references-section">
          <div class="references-header" data-target="references-content-{{ unit.unit_number }}">
            <h4>References</h4>
            <i class="icon fas fa-chevron-down"></i>
          </div>
          <div id="references-content-{{ unit.unit_number }}" class="references-content">
            {{ unit.references }}
          </div>
        </div>
        {% endif %}
      </div>
      {% endif %}
    </div>
    {% endif %}
    {% endfor %}
    
    <div class="back-to-home">
      <a href="{{ '/' | relative_url }}" class="back-link">← Back to Home</a>
    </div>
  </div>
</div>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    // Remove the unit collapse/expand functionality since we're showing all content by default
    
    // Only keep references collapse/expand functionality
    document.querySelectorAll('.references-header').forEach(header => {
      header.addEventListener('click', function() {
        const targetId = this.getAttribute('data-target');
        const contentElement = document.getElementById(targetId);
        
        if (contentElement) {
          contentElement.classList.toggle('collapsed');
          this.classList.toggle('collapsed');
        }
      });
    });
    
    // Check for hash in URL to scroll to the relevant section
    if (window.location.hash) {
      const targetElement = document.querySelector(window.location.hash);
      if (targetElement) {
        // Scroll to the element
        setTimeout(() => {
          window.scrollTo({
            top: targetElement.offsetTop - 20,
            behavior: 'smooth'
          });
        }, 100);
      }
    }
  });
</script>
