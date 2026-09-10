# Metabolic Syndrome

**Domain:** Metabolic Health
**Score range:** 0 to 5 criteria
**Rule:** Metabolic syndrome is present when at least 3 criteria are met.

The calculator follows the five harmonized AHA/NHLBI criteria. Measurements use
the units shown below, and treatment for hypertension or hyperglycemia counts as
the corresponding criterion.

| Criterion | Threshold |
| :--- | :--- |
| Elevated waist circumference | **>=102 cm** for men, **>=88 cm** for women |
| Elevated triglycerides | **>=150 mg/dL** |
| Low HDL cholesterol | **<40 mg/dL** for men, **<50 mg/dL** for women |
| Elevated blood pressure | Systolic **>=130 mmHg**, diastolic **>=85 mmHg**, or antihypertensive treatment |
| Elevated fasting glucose | **>=100 mg/dL** or glucose-lowering treatment |

The standardized result contains `raw_value` as `criteria_met` from 0 to 5,
the five criterion flags, and `attention_flags["metabolic_syndrome"]` as the
boolean result. Missing required data returns `NOT_CALCULABLE`.

## HTTP Endpoint

`POST /risk-scores/metabolic_syndrome`

## Source

- Alberti KG, Eckel RH, Grundy SM, et al. Harmonizing the metabolic syndrome.
  *Circulation*. 2009;120(16):1640-1645.
- Thresholds follow the AHA/NHLBI criteria specified in
  `remaining_health_risk_scores.pdf`.
