# PHQ-9 (Patient Health Questionnaire-9 - Depression Severity)

**Domain:** Depression
**Health Topic:** `depression` ("Depression & Mental Health")
**Raw Score Range:** 0 to 27 points
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **PHQ-9** (Kroenke, Spitzer, & Williams, 2001) is a 9-item clinical depression screening instrument. It assesses the frequency of diagnostic DSM criteria over the past two weeks and flags suicidal or self-harm ideation (Item 9).

---

## 1. Questions & Scoring Rules

Each of the 9 items is scored on a 4-point scale:
- `0`: Not at all
- `1`: Several days
- `2`: More than half the days
- `3`: Nearly every day

### Items:
1. `little_interest`: Little interest or pleasure in doing things.
2. `feeling_down`: Feeling down, depressed, or hopeless.
3. `sleep_trouble`: Trouble falling or staying asleep, or sleeping too much.
4. `tired_energy`: Feeling tired or having little energy.
5. `appetite`: Poor appetite or overeating.
6. `feeling_bad`: Feeling bad about yourself — or that you are a failure or have let yourself or your family down.
7. `concentration`: Trouble concentrating on things, such as reading the newspaper or watching television.
8. `psychomotor`: Moving or speaking so slowly that other people could have noticed, or being so fidgety/restless.
9. `self_harm_thoughts`: **Thoughts that you would be better off dead or of hurting yourself in some way.**

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw score is the sum of all 9 items ($\text{raw\_value} \in [0, 27]$).

### Internal Risk Value
$$\text{risk\_value} = \text{round}\left(\frac{\text{raw\_value}}{27.0} \times 100.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the platform standard (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Total Score (0–27) | Risk Level | Clinical Severity |
| :--- | :--- | :--- |
| **0–4** | **Low risk** | Minimal or no depressive symptoms. |
| **5–9** | **Mild risk** | Mild depressive symptoms; supportive monitoring. |
| **10–14** | **Moderate risk** | Moderate depression; clinical evaluation indicated. |
| **15–19** | **High risk** | Moderately severe depression; active treatment plan recommended. |
| **20–27** | **Very high risk** | Severe depression; immediate multidisciplinary psychiatric intervention. |

---

## 4. Critical Safety Attention Flag (Item 9)

If `self_harm_thoughts > 0`, the calculator triggers:
- `attention_flags.self_harm_thoughts = true`
- Explanation advisory notice: *"Item 9 (thoughts of death or self-harm) is positive and requires clinical attention."*

> [!CAUTION]
> In client applications, this attention flag immediately triggers supportive resource displays (e.g., suicide crisis hotlines like 135 in Argentina) and occupational health medical guidance.

---

## 5. Engine Required Variables

To calculate PHQ-9 via the `ScoringEngine`, the `Phq9Data` entity requires all 9 items:

- `little_interest` (int: 0–3)
- `feeling_down` (int: 0–3)
- `sleep_trouble` (int: 0–3)
- `tired_energy` (int: 0–3)
- `appetite` (int: 0–3)
- `feeling_bad` (int: 0–3)
- `concentration` (int: 0–3)
- `psychomotor` (int: 0–3)
- `self_harm_thoughts` (int: 0–3)

If any item is missing or outside 0–3, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 6. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/phq9`

### Request Payload

```json
{
  "little_interest": 1,
  "feeling_down": 1,
  "sleep_trouble": 2,
  "tired_energy": 2,
  "appetite": 1,
  "feeling_bad": 0,
  "concentration": 0,
  "psychomotor": 0,
  "self_harm_thoughts": 0
}
```

### Example Response (200 OK)

```json
{
  "score_id": "phq9",
  "score_name": "PHQ-9",
  "domain": "Depression",
  "topic_key": "depression",
  "topic_label": "Depression & Mental Health",
  "status": "CALCULATED",
  "raw_value": 7.0,
  "health_index": 74.1,
  "risk_level": "Mild risk",
  "explanation": null,
  "contributing_factors": {
    "little_interest": 1.0,
    "feeling_down": 1.0,
    "sleep_trouble": 2.0,
    "tired_energy": 2.0,
    "appetite": 1.0,
    "feeling_bad": 0.0,
    "concentration": 0.0,
    "psychomotor": 0.0,
    "self_harm_thoughts": 0.0,
    "self_harm_flag": 0.0
  },
  "attention_flags": {
    "self_harm_thoughts": false
  }
}
```
