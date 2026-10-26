# Standardized Nordic Questionnaire (NMQ - Musculoskeletal Ergonomic Risk)

**Domain:** Ergonomics
**Health Topic:** `nordic_nmq` ("Musculoskeletal Health")
**Raw Score Range:** 0 to 27 positive responses
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **Standardized Nordic Questionnaire (NMQ)** (Kuorinka et al., 1987) is the occupational health standard for screening work-related musculoskeletal disorders (WMSDs). It maps symptoms across 9 anatomical zones to identify work-limiting physical strain and repetitive motion injuries.

---

## 1. Anatomical Zones & Questions

The questionnaire evaluates 9 distinct anatomical body zones:
1. `neck`
2. `shoulders`
3. `upper_back`
4. `lower_back`
5. `elbows`
6. `wrists_hands`
7. `hips_thighs`
8. `knees`
9. `ankles_feet`

For **each** zone, three sequential questions are assessed:
- **Q1 (12-Month Trouble):** Have you had trouble (ache, pain, discomfort, numbness) in this zone during the last 12 months? (`trouble_last_12_months: bool`)
- **Q2 (Work Impediment):** Has this trouble prevented you from doing your normal work (at home or at your workplace) during the last 12 months? (`prevented_work_last_12_months: bool`)
- **Q3 (7-Day Trouble):** Have you had trouble in this zone during the last 7 days? (`trouble_last_7_days: bool`)

---

## 2. Risk Value and Health Index (0–100 Scale)

Scoring follows occupational risk stratification based on functional impediment and acute pain:

### Stratification Rules
1. **High Risk (`risk_value = 100.0`):**
   Reported work impediment (`prevented_work_last_12_months = true`) in **at least one** anatomical zone.
2. **Moderate Risk (`risk_value = 50.0`):**
   Recent acute pain (`trouble_last_7_days = true`) in at least one anatomical zone without work impediment.
3. **Low Risk (`risk_value = 0.0`):**
   Neither acute pain in the last 7 days nor work impediment in the last 12 months.

### Health Index
Exposed in `ScoreResult.health_index` according to the system-wide convention (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

- **Optimal health (`health_index = 100.0`):** Low ergonomic risk.
- **Moderate health (`health_index = 50.0`):** Moderate ergonomic risk.
- **Impaired health (`health_index = 0.0`):** High ergonomic risk with disability/work impediment.

---

## 3. Attention Flags

The evaluation automatically outputs clinical attention flags in `attention_flags`:
- `has_work_impediment` (bool): `true` if normal work was prevented in any zone.
- `has_recent_7day_pain` (bool): `true` if acute symptoms were experienced in the past week.
- `has_12month_pain` (bool): `true` if any chronic trouble was reported over the year.

---

## 4. Engine Required Variables

To calculate NMQ via the `ScoringEngine`, the `NordicNmqData` entity requires all 9 zones populated with non-null values for all 3 questions.

If any zone is omitted or incomplete, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 5. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/nordic_nmq`

### Request Payload

```json
{
  "zones": {
    "neck": {
      "trouble_last_12_months": true,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": true
    },
    "shoulders": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "upper_back": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "lower_back": {
      "trouble_last_12_months": true,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "elbows": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "wrists_hands": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "hips_thighs": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "knees": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    },
    "ankles_feet": {
      "trouble_last_12_months": false,
      "prevented_work_last_12_months": false,
      "trouble_last_7_days": false
    }
  }
}
```

### Example Response (200 OK)

```json
{
  "score_id": "nordic_nmq",
  "score_name": "Standardized Nordic Questionnaire (NMQ)",
  "domain": "Ergonomics",
  "topic_key": "nordic_nmq",
  "topic_label": "Musculoskeletal Health",
  "status": "CALCULATED",
  "raw_value": 3.0,
  "health_index": 50.0,
  "risk_level": "Moderate risk",
  "explanation": "Moderate ergonomic risk: Recent pain reported in last 7 days without work impediment.",
  "contributing_factors": {
    "neck_12m_trouble": 1.0,
    "neck_12m_work_prevented": 0.0,
    "neck_7d_trouble": 1.0,
    "lower_back_12m_trouble": 1.0
  },
  "attention_flags": {
    "has_work_impediment": false,
    "has_recent_7day_pain": true,
    "has_12month_pain": true
  }
}
```
