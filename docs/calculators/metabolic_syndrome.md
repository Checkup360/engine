# Metabolic Syndrome (AHA/NHLBI Criteria)

**Domain:** Metabolic Health
**Health Topic:** `metabolic_syndrome` ("Metabolic Syndrome")
**Raw Score Range:** 0 to 5 criteria met
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **Metabolic Syndrome** calculator implements the American Heart Association and National Heart, Lung, and Blood Institute (AHA/NHLBI, 2005) criteria. Metabolic syndrome is diagnosed when $\ge 3$ of the 5 criteria are present.

---

## 1. Diagnostic Criteria (AHA/NHLBI)

| Criterion | Diagnostic Threshold |
| :--- | :--- |
| **1. Abdominal Obesity** | Waist circumference $\ge 102\text{ cm}$ (Men) or $\ge 88\text{ cm}$ (Women) |
| **2. Triglycerides** | Serum triglycerides $\ge 150\text{ mg/dL}$ |
| **3. HDL Cholesterol** | Serum HDL $< 40\text{ mg/dL}$ (Men) or $< 50\text{ mg/dL}$ (Women) |
| **4. Blood Pressure** | Systolic $\ge 130\text{ mmHg}$ OR Diastolic $\ge 85\text{ mmHg}$ OR on antihypertensive medication |
| **5. Fasting Glucose** | Fasting glucose $\ge 100\text{ mg/dL}$ OR on glucose-lowering medication |

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw value is the count of criteria met ($\text{raw\_value} \in [0, 5]$).

### Internal Risk Value
$$\text{risk\_value} = \text{round}\left(\frac{\text{criteria\_met}}{5.0} \times 100.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the platform standard (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Criteria Met (0–5) | Risk Level | Interpretation |
| :--- | :--- | :--- |
| **0** | **Low risk** | Optimal metabolic health (no criteria met). |
| **1** | **Low risk** | Low metabolic risk (1 of 5 criteria met). |
| **2** | **Moderate risk** | Moderate metabolic risk (2 of 5 criteria met; pre-syndrome state). |
| **3–5** | **High risk** | **Metabolic syndrome present** (diagnostic threshold met). |

---

## 4. Attention Flags

The evaluation flags individual criteria and overall syndrome diagnosis in `attention_flags`:
- `waist_elevated` (bool)
- `triglycerides_elevated` (bool)
- `hdl_low` (bool)
- `blood_pressure_elevated` (bool)
- `fasting_glucose_elevated` (bool)
- `metabolic_syndrome` (bool: `true` if $\ge 3$ criteria met)

---

## 5. Engine Required Variables

To calculate Metabolic Syndrome via the `ScoringEngine`, the `MetabolicSyndromeData` entity requires:

- `sex` (str: `"M"` or `"F"`)
- `waist_circumference` (float, in cm)
- `triglycerides` (float, in mg/dL)
- `hdl_cholesterol` (float, in mg/dL)
- `systolic_blood_pressure` (float, in mmHg)
- `diastolic_blood_pressure` (float, in mmHg)
- `hypertension_medication` (bool)
- `fasting_glucose` (float, in mg/dL)
- `glucose_lowering_medication` (bool)

If any variable is missing, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 6. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/metabolic_syndrome`

### Request Payload

```json
{
  "sex": "M",
  "waist_circumference": 105,
  "triglycerides": 180,
  "hdl_cholesterol": 38,
  "systolic_blood_pressure": 135,
  "diastolic_blood_pressure": 88,
  "hypertension_medication": true,
  "fasting_glucose": 95,
  "glucose_lowering_medication": false
}
```

### Example Response (200 OK)

```json
{
  "score_id": "metabolic_syndrome",
  "score_name": "Metabolic Syndrome",
  "domain": "Metabolic Health",
  "topic_key": "metabolic_syndrome",
  "topic_label": "Metabolic Syndrome",
  "status": "CALCULATED",
  "raw_value": 4.0,
  "health_index": 20.0,
  "risk_level": "High risk",
  "explanation": "Metabolic syndrome present (4 of 5 criteria met).",
  "contributing_factors": {
    "waist_elevated": 1.0,
    "triglycerides_elevated": 1.0,
    "hdl_low": 1.0,
    "blood_pressure_elevated": 1.0,
    "fasting_glucose_elevated": 0.0,
    "criteria_met": 4.0
  },
  "attention_flags": {
    "waist_elevated": true,
    "triglycerides_elevated": true,
    "hdl_low": true,
    "blood_pressure_elevated": true,
    "fasting_glucose_elevated": false,
    "metabolic_syndrome": true
  }
}
```
