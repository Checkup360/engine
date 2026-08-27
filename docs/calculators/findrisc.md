# FINDRISC (Finnish Diabetes Risk Score)

**Domain:** Diabetes (Risk of developing Type 2 Diabetes)
**Score Range:** 0 to 26 points

The FINDRISC score estimates an individual's risk of developing Type 2 Diabetes over the next 10 years based on 8 easily measurable risk factors, without requiring complex laboratory tests.

---

## Scoring Table (Business Rules)

### 1. Age
- `<45` years: **0 points**
- `45–54` years: **2 points**
- `55–64` years: **3 points**
- `≥65` years: **4 points**

### 2. BMI (Body Mass Index)
Calculated as `weight (kg) / height (m)²`.
- `<25`: **0 points**
- `25–<30`: **1 point**
- `≥30`: **3 points**

### 3. Waist Circumference
Risk varies by sex.

**Men:**
- `<94 cm`: **0 points**
- `94–101 cm`: **3 points**
- `≥102 cm`: **4 points**

**Women:**
- `<80 cm`: **0 points**
- `80–87 cm`: **3 points**
- `≥88 cm`: **4 points**

### 4. Physical Activity
*Do you engage in at least 30 minutes of daily physical activity at work or during leisure time?*
- **Yes**: **0 points**
- **No**: **2 points**

### 5. Consumption of Fruits and Vegetables
*Do you eat vegetables, fruits, or berries every day?*
- **Yes**: **0 points**
- **No**: **1 point**

### 6. Antihypertensive Medication
*Do you take or have you regularly taken medication for high blood pressure?*
- **No**: **0 points**
- **Yes**: **2 points**

### 7. Previous High Blood Glucose
*Have you ever been found to have high blood glucose levels (e.g., in medical check-ups, during an illness, or pregnancy)?*
- **No**: **0 points**
- **Yes**: **5 points**

### 8. Family History of Diabetes
*Has any member of your biological family been diagnosed with Type 1 or Type 2 diabetes?*
- **No**: **0 points**
- **Yes: Grandparents, aunts/uncles, or first cousins (2nd degree)**: **3 points**
- **Yes: Parents, siblings, or own children (1st degree)**: **5 points**

---

## Risk Interpretation

The total score (0-26) categorizes the risk of developing Type 2 Diabetes within the next 10 years:

| Total Score | Risk Level | Approximate Probability (10 years) |
| :--- | :--- | :--- |
| **0–6** | Low | ~1% (1 in 100) |
| **7–11** | Slightly elevated | ~4% (1 in 25) |
| **12–14** | Moderate | ~17% (1 in 6) |
| **15–20** | High | ~33% (1 in 3) |
| **21–26** | Very high | ~50% (1 in 2) |

---

## Engine Required Variables

To calculate FINDRISC via the `ScoringEngine`, the `FindriscData` object **must** have the following fields fully populated (none can be null):

- `age` (int)
- `weight` (float)
- `height` (float)
- `sex` (str: "M" or "F")
- `waist_circumference` (float)
- `daily_physical_activity` (bool)
- `fruits_vegetables` (bool)
- `hypertension_medication` (bool)
- `previous_high_glucose` (bool)
- `family_diabetes` (str: "no", "second_degree", "first_degree")

If at least one of these values is missing, the calculator will return a result with the `NOT_CALCULABLE` status.
