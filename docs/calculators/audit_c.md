# AUDIT-C (Alcohol Use Disorders Identification Test-Consumption)

**Domain:** Alcohol Use
**Health Topic:** `audit_c` ("Alcohol")
**Raw Score Range:** 0 to 12 points
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **AUDIT-C** is a brief, validated 3-question screening tool developed by the World Health Organization (WHO) to identify individuals with hazardous alcohol consumption or active alcohol use disorders.

---

## 1. Questions & Scoring Rules

The instrument evaluates three key dimensions scored from 0 to 4 points each:

### Q1: Frequency of Drinking
*How often do you have a drink containing alcohol?*
- **Never**: 0 points
- **Monthly or less**: 1 point
- **2 to 4 times a month**: 2 points
- **2 to 3 times a week**: 3 points
- **4 or more times a week**: 4 points

### Q2: Typical Quantity
*How many standard drinks do you have on a typical day when you are drinking?*
- **1 or 2**: 0 points
- **3 or 4**: 1 point
- **5 or 6**: 2 points
- **7 to 9**: 3 points
- **10 or more**: 4 points

### Q3: Binge Drinking Frequency
*How often do you have 6 or more drinks on one occasion?*
- **Never**: 0 points
- **Less than monthly**: 1 point
- **Monthly**: 2 points
- **Weekly**: 3 points
- **Daily or almost daily**: 4 points

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw score is the sum of the three questions ($\text{raw\_value} \in [0, 12]$). Sex-specific clinical cutoff thresholds apply:
- **Men (`M`)**: Cutoff = **4 points**
- **Women (`F`)**: Cutoff = **3 points**

### Internal Risk Value
The engine normalizes the raw score into a continuous severity scale ($\text{risk\_value} \in [0, 100]$):
- If $\text{raw\_value} < \text{cutoff}$:
  $$\text{risk\_value} = \text{round}\left(\frac{\text{raw\_value}}{\text{cutoff}} \times 50.0, 1\right)$$
- If $\text{raw\_value} \ge \text{cutoff}$:
  $$\text{risk\_value} = \text{round}\left(51.0 + \frac{\text{raw\_value} - \text{cutoff}}{12 - \text{cutoff}} \times 49.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the system-wide convention (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Total Points | Risk Level | Interpretation |
| :--- | :--- | :--- |
| **Below cutoff** (<4 Men / <3 Women) | **Low risk** | Alcohol consumption within low-risk guidelines; continue healthy habits. |
| **At or above cutoff** (≥4 Men / ≥3 Women) | **High risk** | Hazardous drinking pattern identified; occupational health guidance or clinical follow-up recommended. |

---

## 4. Engine Required Variables

To calculate AUDIT-C via the `ScoringEngine`, the `AuditCData` entity requires all of the following:

- `frequency` (int: 0–4)
- `quantity` (int: 0–4)
- `heavy_drinking` (int: 0–4)
- `sex` (str: `"M"` or `"F"`)

If any field is missing or out of range, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 5. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/audit_c`

### Request Payload

```json
{
  "frequency": 2,
  "quantity": 1,
  "heavy_drinking": 0,
  "sex": "M"
}
```

### Example Response (200 OK)

```json
{
  "score_id": "audit_c",
  "score_name": "AUDIT-C Alcohol Risk",
  "domain": "Alcohol Use",
  "topic_key": "audit_c",
  "topic_label": "Alcohol",
  "status": "CALCULATED",
  "raw_value": 3.0,
  "health_index": 62.5,
  "risk_level": "Low risk",
  "explanation": "AUDIT-C score is 3/12 (Low risk for M threshold of 4).",
  "contributing_factors": {
    "frequency": 2.0,
    "quantity": 1.0,
    "heavy_drinking": 0.0,
    "total_score": 3.0,
    "cutoff": 4.0
  },
  "attention_flags": {}
}
```
