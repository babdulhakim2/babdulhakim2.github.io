---
layout: default
permalink: /ml/
---

# Machine Learning 2023

<div class="module-container">
  <div class="module-sidebar">
    {% include module-navigation.html units=site.data.ml_units module_title="Machine Learning" %}
  </div>
  
  <div class="module-content">
    <div class="welcome-banner">
      <h2>Machine Learning Module</h2>
      <p>This section contains all my work for the Machine Learning module from November 2023. Each unit builds upon core machine learning concepts, with projects, assignments, and artifacts that demonstrate my learning journey.</p>
    </div>
    
    {% for unit in site.data.ml_units %}
    {% if unit.artifacts %}
    {% include unit-card.html
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
