# Edmonton Obesity Staging System (EOSS)

**Domain:** Obesity-related Health Impact
**Score range:** Stage 0 to Stage 4

EOSS is a clinical staging system. It should be assigned from a clinician's
assessment of obesity-related health impact, not inferred from BMI alone. The
engine accepts one stage for each domain and returns the highest domain stage.

| Stage | Operational interpretation |
| :--- | :--- |
| **0** | No risk factors, symptoms, psychopathology, or functional impairment |
| **1** | Subclinical risk factors, mild symptoms, mild psychopathology, or mild functional impairment |
| **2** | Established chronic disease, moderate psychopathology, or moderate functional impairment |
| **3** | Significant end-organ damage, significant psychopathology, or significant functional impairment |
| **4** | Severe or potentially end-stage disease, severe psychopathology, or severe functional impairment |

The standardized result uses `raw_value` for the highest stage and includes:

- `contributing_factors` for the three domain stages.
- `attention_flags["stage_2_or_higher"]` for established impact.
- `attention_flags["stage_3_or_higher"]` for significant impact.
- `attention_flags["stage_4"]` for severe or end-stage impact.

Missing or out-of-range stages return `NOT_CALCULABLE`. This score is a clinical
staging aid and is not a diagnosis.

## HTTP Endpoint

`POST /risk-scores/eoss`

Example payload:

```json
{
  "physical_health_stage": 1,
  "mental_health_stage": 0,
  "functional_stage": 2
}
```

## Source

- Sharma AM, Kushner RF. A proposed clinical staging system for obesity.
  *International Journal of Obesity*. 2009;33:289-295.
