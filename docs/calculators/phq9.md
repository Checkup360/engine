# PHQ-9 (Patient Health Questionnaire-9)

**Domain:** Depression / Mood and emotional well-being  
**Score Range:** 0 to 27 points  
**Instrument:** 9-item depression symptom questionnaire for the previous two weeks

The PHQ-9 measures the severity of depressive symptoms. It is a symptom-severity
screening instrument and is not, by itself, a clinical diagnosis.

---

## Response Scoring

Each item is scored using the following response scale:

| Response | Points |
| :--- | :---: |
| Not at all | **0** |
| Several days | **1** |
| More than half the days | **2** |
| Nearly every day | **3** |

The total score is the sum of all nine item values:

`total_score = Q1 + Q2 + Q3 + Q4 + Q5 + Q6 + Q7 + Q8 + Q9`

The item fields used by the engine are:

1. `little_interest`
2. `feeling_down`
3. `sleep_trouble`
4. `tired_energy`
5. `appetite`
6. `feeling_bad`
7. `concentration`
8. `psychomotor`
9. `self_harm_thoughts`

Every item must be an integer from 0 through 3.

---

## Severity Interpretation

| Total Score | Severity |
| :--- | :--- |
| **0–4** | None / minimal |
| **5–9** | Mild |
| **10–14** | Moderate |
| **15–19** | Moderately severe |
| **20–27** | Severe |

---

## Item 9 Attention Flag

`self_harm_thoughts` is exposed separately because it concerns thoughts of death
or self-harm. A positive response does not get hidden by the total severity score.

The standardized result contains:

- `attention_flags["self_harm_thoughts"]`: `true` when item 9 is greater than 0.
- `contributing_factors["self_harm_flag"]`: numeric compatibility flag (`0` or `1`).
- `explanation`: an attention message when item 9 is positive.

A positive item 9 response requires appropriate clinical attention and must not be
interpreted only through the total PHQ-9 severity category.

---

## Engine Required Variables

To calculate PHQ-9 via the `ScoringEngine`, the `Phq9Data` object must have all
nine fields populated:

- `little_interest` (int: 0-3)
- `feeling_down` (int: 0-3)
- `sleep_trouble` (int: 0-3)
- `tired_energy` (int: 0-3)
- `appetite` (int: 0-3)
- `feeling_bad` (int: 0-3)
- `concentration` (int: 0-3)
- `psychomotor` (int: 0-3)
- `self_harm_thoughts` (int: 0-3)

If at least one value is missing or outside the supported range, the calculator
returns `NOT_CALCULABLE`.

---

## HTTP Endpoint

`POST /risk-scores/phq9`

Example payload:

```json
{
  "little_interest": 1,
  "feeling_down": 1,
  "sleep_trouble": 0,
  "tired_energy": 2,
  "appetite": 0,
  "feeling_bad": 1,
  "concentration": 0,
  "psychomotor": 0,
  "self_harm_thoughts": 0
}
```

---

## Source

- Kroenke K, Spitzer RL, Williams JBW. *The PHQ-9: Validity of a Brief
  Depression Severity Measure*. Journal of General Internal Medicine.
  2001;16(9):606-613.
- The score bands and item response scale follow the PHQ-9 specification
  provided in `remaining_health_risk_scores.pdf`.
