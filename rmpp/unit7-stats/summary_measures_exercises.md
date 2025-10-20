---
layout: default
title: Summary Measures Exercises
parent: Unit 7 Statistics
nav_order: 2
---

[← Back to RMPP Module]({{ '/rmpp/#unit-7' | relative_url }})

# Summary Measures Exercises & Solutions

## Exercise 6.1: Diet B Summary Statistics

**Problem:** Open the Excel workbook Exa8.1B.xlsx. Obtain the sample size, sample mean weight loss and the sample standard deviation of the weight loss for Diet B. Place these results in cells F23 to F25.

**LibreOffice Solution:**

```calc
# In cell F23 (Sample size for Diet B):
=COUNT(B52:B101)

# In cell F24 (Mean weight loss for Diet B):
=AVERAGE(B52:B101)

# In cell F25 (Standard deviation for Diet B):
=STDEV(B52:B101)
```

**Expected Results:**

- **Sample size (n):** 50
- **Mean weight loss (x̄):** 3.710 kg
- **Standard deviation (s):** 2.770 kg

**Interpretation:**
Diet B shows lower mean weight loss (3.710 kg) compared to Diet A (5.341 kg), suggesting Diet A is more effective. The standard deviation (2.770 kg) indicates moderate variability in results.

**File:** [Exe-8.1B-solution-6.1.xlsx](artefacts/Exe-8.1B-solution-6.1.xlsx)

---

## Exercise 6.2: Diet B Quartiles and IQR

**Problem:** Open the Excel workbook Exa8.2B.xlsx. Obtain the sample median, first and third quartiles and the sample interquartile range of the weight loss for Diet B. Place these results in cells F26 to F29.

**LibreOffice Solution:**

```calc
# In cell F26 (Median for Diet B):
=MEDIAN(B52:B101)

# In cell F27 (First quartile Q1 for Diet B):
=QUARTILE(B52:B101,1)

# In cell F28 (Third quartile Q3 for Diet B):
=QUARTILE(B52:B101,3)

# In cell F29 (Interquartile range for Diet B):
=F28-F27
```

**Results:**

- **Median (M):** 3.745 kg
- **First Quartile (Q1):** 1.953 kg
- **Third Quartile (Q3):** 5.404 kg
- **Interquartile Range (IQR):** 3.451 kg

**Interpretation:**
Diet B's median (3.745 kg) is substantially lower than Diet A's median (5.642 kg), confirming Diet A's superior effectiveness. The positive Q1 (1.953 kg) shows at least 75% of Diet B participants experienced weight loss.

**File:** [Exe 8.2B-solution-6.2.xlsx](artefacts/Exe%208.2B-solution-6.2.xlsx)

---

## Exercise 6.3: Brand Preferences - Area 2

**Problem:** Open the Excel workbook Exa8.3D.xlsx. Obtain the frequencies and percentage frequencies of the variable Brand for Area 2 respondents.

**LibreOffice Solution:**

**Step 1: Calculate Frequencies (cells E6-E9)**

```calc
# In cell E6 (Brand A frequency for Area 2):
=COUNTIF(B72:B141,"A")

# In cell E7 (Brand B frequency for Area 2):
=COUNTIF(B72:B141,"B")

# In cell E8 (Other brands frequency for Area 2):
=COUNTIF(B72:B141,"Other")

# In cell E9 (Total for Area 2):
=SUM(E6:E8)
```

**Step 2: Calculate Percentages (cells E15-E18)**

```calc
# In cell E15 (Brand A percentage):
=100*E6/E$9

# Copy E15 to E16:E17 for Brand B and Other percentages

# In cell E18 (Verification - should equal 100%):
=SUM(E15:E17)
```

**Results:**

- **Brand A:** Area 1: 15.7%, Area 2: 21.1%
- **Brand B:** Area 1: 24.3%, Area 2: 33.3%
- **Other:** Area 1: 60.0%, Area 2: 45.6%
- **Total:** Both areas: 100%

**Interpretation:**
Area 2 shows higher preference for premium brands A and B (54.4% combined) compared to Area 1 (40.0% combined). "Other" brands dominate less in Area 2 (45.6%) versus Area 1 (60.0%), suggesting different demographic preferences or higher brand loyalty in Area 2.

**File:** [Exe 8.3D-solution-6.3.xlsx](artefacts/Exe%208.3D-solution-6.3.xlsx)

---

[← Back to RMPP Module]({{ '/rmpp/#unit-7' | relative_url }})
