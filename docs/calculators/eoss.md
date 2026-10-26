# EOSS (Edmonton Obesity Staging System)

**Domain:** Obesity-related Health Impact
**Health Topic:** `eoss` ("Obesity (EOSS)")
**Raw Score Range:** Stage 0 to Stage 4
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **Edmonton Obesity Staging System (EOSS)** (Sharma & Kushner, 2009) is a 5-stage clinical staging system that classifies obesity beyond BMI alone by assessing the presence and severity of obesity-related comorbidities, mental health symptoms, and functional limitations.

---

## 1. Clinical Domains & Stages

The score is determined by the highest stage observed across three clinical dimensions:
- `physical_health_stage` (0–4)
- `mental_health_stage` (0–4)
- `functional_stage` (0–4)

$$\text{raw\_value} = \max(\text{physical\_health\_stage}, \text{mental\_health\_stage}, \text{functional\_stage})$$

### Stage Definitions:
- **Stage 0:** No apparent obesity-related risk factors (normal BP, glucose, lipids, physical functioning).
- **Stage 1:** Subclinical risk factors (borderline hypertension, impaired fasting glucose, mild aches).
- **Stage 2:** Established chronic disease requiring medical treatment (Type 2 diabetes, hypertension, moderate functional impairment).
- **Stage 3:** Significant end-organ damage or severe functional limitations (myocardial infarction, severe osteoarthritis).
- **Stage 4:** Severe (end-stage) obesity-related chronic diseases or severe disabling functional impairment.

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw value is the maximum stage ($\text{stage} \in [0, 4]$).

### Internal Risk Value
$$\text{risk\_value} = \text{round}\left(\frac{\text{stage}}{4.0} \times 100.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the platform standard (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Stage (0–4) | Risk Level | Health Index | Description |
| :--- | :--- | :--- | :--- |
| **0** | **Low risk** | **100.0** | No risk factors or impairment. |
| **1** | **Slightly elevated risk** | **75.0** | Subclinical risk factors or mild impairment. |
| **2** | **Moderate risk** | **50.0** | Established chronic disease or moderate impairment. |
| **3** | **High risk** | **25.0** | Significant end-organ damage or impairment. |
| **4** | **Very high risk** | **0.0** | Severe or end-stage impairment. |

---

## 4. Attention Flags

The evaluation flags clinical milestones in `attention_flags`:
- `stage_2_or_higher` (bool: `stage >= 2`)
- `stage_3_or_higher` (bool: `stage >= 3`)
- `stage_4` (bool: `stage == 4`)

---

## 5. Engine Required Variables

To calculate EOSS via the `ScoringEngine`, the `EOSSData` entity requires all 3 domain stages:

- `physical_health_stage` (int: 0–4)
- `mental_health_stage` (int: 0–4)
- `functional_stage` (int: 0–4)

If any stage is missing or outside 0–4, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 6. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/eoss`

### Request Payload

```json
{
  "physical_health_stage": 2,
  "mental_health_stage": 1,
  "functional_stage": 0
}
```

### Example Response (200 OK)

```json
{
  "score_id": "eoss",
  "score_name": "EOSS",
  "domain": "Obesity-related Health Impact",
  "topic_key": "eoss",
  "topic_label": "Obesity (EOSS)",
  "status": "CALCULATED",
  "raw_value": 2.0,
  "health_index": 50.0,
  "risk_level": "Moderate risk",
  "explanation": "Stage 2: Established chronic disease or moderate impairment",
  "contributing_factors": {
    "physical_health_stage": 2.0,
    "mental_health_stage": 1.0,
    "functional_stage": 0.0,
    "highest_stage": 2.0
  },
  "attention_flags": {
    "stage_2_or_higher": true,
    "stage_3_or_higher": false,
    "stage_4": false
  }
}
```
