# PSS-10 (Perceived Stress Scale)

**Domain:** Psychological Health
**Health Topic:** `pss10` ("Stress & Burnout")
**Raw Score Range:** 0 to 40 points
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **PSS-10** (Cohen et al., 1983) is the most widely recognized psychological instrument for measuring an individual's perception of stress over the past month. It evaluates feelings of unpredictability, uncontrollability, and overload in daily and work life.

---

## 1. Questions & Scoring Rules

The questionnaire comprises 10 items scored on a 5-point Likert scale (0 = Never, 1 = Almost Never, 2 = Sometimes, 3 = Fairly Often, 4 = Very Often):

| Item | Focus | Scoring Direction |
| :--- | :--- | :--- |
| **Q1** | Upset because of something that happened unexpectedly | Direct (0–4) |
| **Q2** | Unable to control important things in life | Direct (0–4) |
| **Q3** | Felt nervous and stressed | Direct (0–4) |
| **Q4** | Felt confident about ability to handle personal problems | **Reversed** ($4 - \text{score}$) |
| **Q5** | Felt that things were going your way | **Reversed** ($4 - \text{score}$) |
| **Q6** | Could not cope with all the things you had to do | Direct (0–4) |
| **Q7** | Able to control irritations in life | **Reversed** ($4 - \text{score}$) |
| **Q8** | Felt on top of things | **Reversed** ($4 - \text{score}$) |
| **Q9** | Angered because of things that happened outside control | Direct (0–4) |
| **Q10** | Difficulties piling up so high that you could not overcome them | Direct (0–4) |

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw score is the sum of direct items and reversed items ($\text{raw\_value} \in [0, 40]$).

### Internal Risk Value
Mapped piecewise to reflect established clinical stress severity bands:
- **Low Stress ($\le 13$ points):**
  $$\text{risk\_value} = \text{round}\left(\frac{\text{raw\_value}}{13} \times 20.0, 1\right)$$
- **Moderate Stress ($14–26$ points):**
  $$\text{risk\_value} = \text{round}\left(21.0 + \frac{\text{raw\_value} - 14}{12} \times 29.0, 1\right)$$
- **High Stress / Burnout Risk ($27–40$ points):**
  $$\text{risk\_value} = \text{round}\left(51.0 + \frac{\text{raw\_value} - 27}{13} \times 49.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the system-wide convention (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Total Points (0–40) | Risk Level | Interpretation |
| :--- | :--- | :--- |
| **0–13** | **Low risk** | Healthy coping mechanisms; stress levels are within manageable ranges. |
| **14–26** | **Moderate risk** | Mild-to-moderate perceived stress; workplace ergonomics and wellness support suggested. |
| **27–40** | **High risk** | High perceived stress and elevated burnout vulnerability; stress management interventions recommended. |

---

## 4. Engine Required Variables

To calculate PSS-10 via the `ScoringEngine`, the `Pss10Data` entity requires all 10 fields:

- `pss10_q1` to `pss10_q10` (int: 0–4)

If any item is omitted or outside the 0–4 range, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 5. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/pss10`

### Request Payload

```json
{
  "pss10_q1": 1,
  "pss10_q2": 1,
  "pss10_q3": 2,
  "pss10_q4": 3,
  "pss10_q5": 3,
  "pss10_q6": 1,
  "pss10_q7": 3,
  "pss10_q8": 2,
  "pss10_q9": 1,
  "pss10_q10": 0
}
```

### Example Response (200 OK)

```json
{
  "score_id": "pss10",
  "score_name": "PSS-10 Perceived Stress Scale",
  "domain": "Psychological Health",
  "topic_key": "pss10",
  "topic_label": "Stress & Burnout",
  "status": "CALCULATED",
  "raw_value": 11.0,
  "health_index": 83.1,
  "risk_level": "Low risk",
  "explanation": "Low perceived stress (Score 11/40).",
  "contributing_factors": {
    "pss10_q1": 1.0,
    "pss10_q2": 1.0,
    "pss10_q3": 2.0,
    "pss10_q4": 1.0,
    "pss10_q5": 1.0,
    "pss10_q6": 1.0,
    "pss10_q7": 1.0,
    "pss10_q8": 2.0,
    "pss10_q9": 1.0,
    "pss10_q10": 0.0,
    "total_score": 11.0
  },
  "attention_flags": {}
}
```
