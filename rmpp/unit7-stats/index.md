---
layout: default
title: "Unit 7: Statistical Analysis Worksheets"
---

[← Back to RMPP Module]({{ '/rmpp/#unit-7' | relative_url }})

# Unit 7: Statistical Analysis Worksheets

## Artifact Files

- **Hypothesis Testing:** [Hypothesis_Testing_Worksheet.xlsx](./artefacts/Hypothesis_Testing_Worksheet.xlsx)
- **Summary Measures:** [Summary_Measures_Worksheet.xlsx](./artefacts/Summary_Measures_Worksheet.xlsx)
- **Literature Review:** [Unit7_Literature_Review.pdf](./artefacts/Unit7_Literature_Review.pdf)

---

## Hypothesis Testing Worksheet Solutions

**Artifact File:** [Hypothesis_Testing_Worksheet.xlsx](./artefacts/Hypothesis_Testing_Worksheet.xlsx)

### Exercise: Diet Effectiveness Comparison

**Task:** Test whether Diet A is significantly more effective than Diet B for weight loss.

**Data:**
- **Diet A:** Mean = 5.34 kg, SD = 2.54, n = 50
- **Diet B:** Mean = 3.71 kg, SD = 2.77, n = 50

**Hypothesis:**
- H₀: μₐ ≤ μᵦ (Diet A is not more effective)
- H₁: μₐ > μᵦ (Diet A is more effective)

**LibreOffice Analysis:**
Using `=TTEST(array1, array2, tails, type)` function:
- **Test Statistic:** t = 3.12
- **p-value:** 0.0013
- **Critical Value (α = 0.05):** 1.96

**Conclusion:**
With p < 0.05, we reject H₀. Diet A is statistically significantly more effective than Diet B for weight loss. However, practical significance must consider the 1.63 kg difference in context of implementation costs and clinical relevance.

## Summary Measures Worksheet Solutions

**Artifact File:** [Summary_Measures_Worksheet.xlsx](./artefacts/Summary_Measures_Worksheet.xlsx)

### Exercise 1: Descriptive Statistics for Diet Study

**Diet A Statistics:**
- Mean: 5.34 kg
- Median: 5.12 kg
- Standard Deviation: 2.54 kg
- Range: 11.78 kg (Min: -1.72, Max: 10.06)
- Quartiles: Q₁ = 3.45, Q₃ = 7.23

**Diet B Statistics:**
- Mean: 3.71 kg
- Median: 3.89 kg
- Standard Deviation: 2.77 kg
- Range: 14.687 kg (Min: -4.148, Max: 10.539)
- Quartiles: Q₁ = 1.98, Q₃ = 5.44

### Exercise 2: Brand Preference Analysis

**Brand Preference Summary:**
- **Brand A:** 15.7% preference
- **Brand B:** 24.3% preference
- **Other:** 60.0% preference

**Key LibreOffice Functions Used:**
- `=AVERAGE()` for mean calculations
- `=STDEV()` for standard deviation
- `=QUARTILE()` for quartile analysis
- `=TTEST()` for hypothesis testing
- `=COUNT()` for frequency analysis

## Interpretation Guidelines

### Statistical vs Practical Significance
- **Statistical Significance:** p < 0.05 indicates the difference is unlikely due to chance
- **Practical Significance:** Consider effect size, cost-benefit analysis, and real-world impact
- Both measures are essential for evidence-based decision-making

### Understanding p-values
- p-value represents probability of observing results if null hypothesis is true
- Lower p-values provide stronger evidence against null hypothesis
- α = 0.05 is conventional threshold for statistical significance

---

[← Back to RMPP Module]({{ '/rmpp/#unit-7' | relative_url }})