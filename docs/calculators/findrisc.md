# FINDRISC (Finnish Diabetes Risk Score)

**Domain:** Diabetes (Risk of developing Type 2 Diabetes)
**Health Topic:** `diabetes` ("Diabetes")
**Raw Score Range:** 0 to 26 points
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **FINDRISC** score estimates an individual's risk of developing Type 2 Diabetes Mellitus over the next 10 years based on 8 clinical and lifestyle risk factors, without requiring invasive laboratory tests.

---

## 1. Scoring Table (Business Rules)

### 1. Age
- `<45` years: **0 points**
- `45–54` years: **2 points**
- `55–64` years: **3 points**
- `≥65` years: **4 points**

### 2. BMI (Body Mass Index)
Calculated as $\text{weight (kg)} / \text{height (m)}^2$:
- `<25`: **0 points**
- `25–<30`: **1 point**
- `≥30`: **3 points**

### 3. Waist Circumference
Risk varies by biological sex:

**Men (`M`):**
- `<94 cm`: **0 points**
- `94–101 cm`: **3 points**
- `≥102 cm`: **4 points**

**Women (`F`):**
- `<80 cm`: **0 points**
- `80–87 cm`: **3 points**
- `≥88 cm`: **4 points**

### 4. Physical Activity
*At least 30 minutes of daily physical activity at work or leisure?*
- **Yes**: **0 points**
- **No**: **2 points**

### 5. Consumption of Fruits and Vegetables
*Daily consumption of vegetables, fruits, or berries?*
- **Yes**: **0 points**
- **No**: **1 point**

### 6. Antihypertensive Medication
*Regular or current intake of medication for high blood pressure?*
- **No**: **0 points**
- **Yes**: **2 points**

### 7. Previous High Blood Glucose
*History of high blood glucose (e.g., check-ups, illness, pregnancy)?*
- **No**: **0 points**
- **Yes**: **5 points**

### 8. Family History of Diabetes
*Diagnosed Type 1 or Type 2 diabetes in biological family?*
- **No**: **0 points**
- **Second degree (grandparents, aunts/uncles, cousins)**: **3 points**
- **First degree (parents, siblings, children)**: **5 points**

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw score is the sum of points across all 8 factors ($\text{raw\_value} \in [0, 26]$).

### Internal Risk Value
$$\text{risk\_value} = \text{round}\left(\frac{\text{raw\_value}}{26.0} \times 100.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the platform standard (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Total Score (0–26) | Risk Level | 10-Year Estimated Probability |
| :--- | :--- | :--- |
| **0–6** | **Low risk** | ~1% (1 in 100) |
| **7–11** | **Slightly elevated risk** | ~4% (1 in 25) |
| **12–14** | **Moderate risk** | ~17% (1 in 6) |
| **15–20** | **High risk** | ~33% (1 in 3) |
| **21–26** | **Very high risk** | ~50% (1 in 2) |

---

## 4. Engine Required Variables

To calculate FINDRISC via the `ScoringEngine`, the `FindriscData` entity requires:

- `age` (int)
- `weight` (float, in kg)
- `height` (float, in meters)
- `sex` (str: `"M"` or `"F"`)
- `waist_circumference` (float, in cm)
- `daily_physical_activity` (bool)
- `fruits_vegetables` (bool)
- `hypertension_medication` (bool)
- `previous_high_glucose` (bool)
- `family_diabetes` (str: `"no"`, `"second_degree"`, `"first_degree"`)

If any value is missing, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 5. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/findrisc`

### Request Payload

```json
{
  "age": 45,
  "sex": "M",
  "weight": 85,
  "height": 1.78,
  "waist_circumference": 98,
  "daily_physical_activity": true,
  "fruits_vegetables": true,
  "hypertension_medication": false,
  "previous_high_glucose": false,
  "family_diabetes": "second_degree"
}
```

### Example Response (200 OK)

```json
{
  "score_id": "findrisc",
  "score_name": "FINDRISC",
  "domain": "Diabetes",
  "topic_key": "diabetes",
  "topic_label": "Diabetes",
  "status": "CALCULATED",
  "raw_value": 9.0,
  "health_index": 65.4,
  "risk_level": "Slightly elevated risk",
  "contributing_factors": {
    "age": 2.0,
    "bmi": 1.0,
    "waist": 3.0,
    "physical_activity": 0.0,
    "fruits_vegetables": 0.0,
    "hypertension": 0.0,
    "high_glucose": 0.0,
    "family_diabetes": 3.0
  },
  "attention_flags": {}
}
```
