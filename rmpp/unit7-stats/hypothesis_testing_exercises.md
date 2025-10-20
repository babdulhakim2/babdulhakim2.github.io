---
layout: default
title: Hypothesis Testing Exercises
parent: Unit 7 Statistics
nav_order: 4
---

[← Back to RMPP Module]({{ '/rmpp/#unit-7' | relative_url }})

# Hypothesis Testing Exercises & Solutions

{: .no_toc }

## Exercise 7.1: One-Tailed Test for Filtration Agents

**Problem:** Using Data Set G, conduct a one-tailed test to determine whether Filter Agent 1 is more effective than Filter Agent 2.

**Hypotheses:**

- H₀: μ₁ ≥ μ₂ vs H₁: μ₁ < μ₂ (lower impurity = more effective)

**LibreOffice Solution:**

```calc
=TTEST(B2:B11, C2:C11, 1, 1)
```

- Mode = 1 (one-tailed), Type = 1 (paired samples)
- Compare with two-tailed result from Exercise 7.3
- One-tailed p-value = two-tailed p-value ÷ 2

**Interpretation:** If sample mean for Agent 1 < Agent 2 and p < 0.05, Agent 1 is significantly more effective.

---

## Exercise 7.2: Gender Income Analysis (Data Set C)

**Problem:** Test whether mean income for males exceeds that of females using Data Set C.

**Hypotheses:**

- H₀: μ_male ≤ μ_female (male income does not exceed female income)
- H₁: μ_male > μ_female (male income exceeds female income)

**F-test for Variance Equality (LibreOffice Results):**

```
F = 1.226
P(two-tail) = 0.436
Alpha = 0.05
df = 59, 59
```

**Result:** p = 0.436 > 0.05 → Equal variances assumption satisfied

**Sample Statistics:**

- **Males (n=60):** Mean = 52.91, SD = 15.27, Variance = 233.13
- **Females (n=60):** Mean = 44.23, SD = 13.79, Variance = 190.18
- **Difference:** 8.68 units higher for males

**F-test Interpretation:**
The F-test result (p = 0.436) indicates that we cannot reject the null hypothesis of equal variances. This means the assumption of equal population variances between male and female incomes is satisfied, which is important for conducting appropriate statistical tests.

**Descriptive Analysis:**
The sample data shows males have higher mean income (52.91) compared to females (44.23), with a difference of 8.68 units. Both groups have similar sample sizes (n=60) and the F-test confirms equal variances assumption is met.

**Assumptions Analysis:**

1. **Equal variances:** F-test p-value = 0.436 > 0.05 (assumption satisfied)
2. **Independence:** Data represents different bank cardholders
3. **Sample adequacy:** Both groups have n=60 observations

**File Attachment:** [Exe 8.6C.xlsx](artefacts/Exe-8.6C.xlsx) _(LibreOffice analysis file)_

---

## Exercise 7.3: Filtration Agents Two-Tailed Test (Data Set G)

**Problem:** Two-tailed test of whether population mean impurity differs between filtration agents.

**Hypotheses:**

- H₀: μ₁ = μ₂ (no difference in mean impurity)
- H₁: μ₁ ≠ μ₂ (difference exists in mean impurity)

**Sample Data (12 batches):**

- **Agent 1:** Mean = 8.25, Variance = 1.059
- **Agent 2:** Mean = 8.68, Variance = 1.078
- **Mean Difference:** -0.433 (Agent 1 lower impurity)

**Paired t-test Results:**

```
t = -3.264, df = 11
P(two-tail) = 0.0075
Alpha = 0.05
```

**Interpretation:**
p = 0.0075 < 0.05 → **Significant difference exists**

Agent 1 produces significantly lower impurity than Agent 2 (p = 0.008). The mean difference of -0.433 indicates Agent 1 is more effective at reducing impurity levels.

**File Attachment:** [Exa8.4G.xlsx](artefacts/Exe-8.4G.xlsx) _(Analysis file)_

---

## Exercise 7.4: One-Tailed Filtration Test

**Problem:** Using Exercise 7.3 results, determine if Filter Agent 1 is more effective (one-tailed test).

**From Exercise 7.3:**

- Agent 1 mean = 8.25, Agent 2 mean = 8.68
- Two-tailed p-value = 0.0075

**One-Tailed Analysis:**

- **Hypotheses:** H₀: μ₁ ≥ μ₂ vs H₁: μ₁ < μ₂ (Agent 1 more effective)
- **Data supports H₁:** Agent 1 mean < Agent 2 mean ✓
- **One-tailed p-value:** 0.0075 ÷ 2 = 0.00375

**Conclusion:**
p = 0.00375 < 0.05 → **Agent 1 is significantly more effective**

One-tailed test provides stronger evidence (p = 0.004) that Agent 1 reduces impurity more than Agent 2.

---

## Exercise 7.5: Bank Cardholder Income Analysis (LibreOffice)

**Problem:** Test if male population mean income exceeds female (Data Set C).

**Note:** This exercise uses the same data as Exercise 7.2.

**Solution:** See Exercise 7.2 above for complete F-test and descriptive analysis.

**Key Finding:** Males have higher mean income (52.91) than females (44.23) with equal variances confirmed.

---

[← Back to RMPP Module]({{ '/rmpp/#unit-7' | relative_url }})
