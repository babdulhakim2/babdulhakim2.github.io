---
layout: default
title: "Unit 8 Formative Activity"
---

# Unit 8 Formative Activity

## Task
Work through Chapter 4 of Debellis (2021) A Practical Guide to Building OWL Ontologies Using Protégé 5.5 and Plugins. Create an ontology following Exercises 1-7.

## My University Ontology

**Domain:** Higher Education System

**Classes Created:**
- University
- Department
- Course
- Student
- Professor
- Degree

**Object Properties:**
- hasStudent (University → Student)
- belongsToDepartment (Professor → Department)
- teaches (Professor → Course)
- enrolledIn (Student → Course)

**Data Properties:**
- hasName (String)
- hasID (Integer)
- hasGPA (Float)
- yearEstablished (Integer)

**Key Insights:**
Following the step-by-step exercises made the ontology development process clear. Setting up class hierarchies first, then properties, then instances creates a logical flow. The reasoner validation in Exercise 6 caught several inconsistencies I missed manually.

---

[← Back to Unit 8](/krr/#unit-8) | [KRR Module Home](/krr/)