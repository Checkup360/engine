# STOP-BANG (Sleep Apnea Screening)

**Domain:** Sleep Apnea
**Score Range:** 0 to 8 points

The STOP-BANG questionnaire is a clinical screening tool used to identify individuals who are at high risk for Obstructive Sleep Apnea (OSA). It consists of 8 yes/no questions, where each positive answer adds 1 point to the total score.

---

## Scoring Table (Business Rules)

The acronym **STOP-BANG** represents the 8 risk factors. Each criterion met (a "Yes" answer or a clinical value above the threshold) adds **1 point**.

| Criterion | Description | Points if "Yes" / Present |
| :--- | :--- | :---: |
| **S** - Snoring | Do you snore loudly? | **+1** |
| **T** - Tired | Do you often feel tired, fatigued, or sleepy during the daytime? | **+1** |
| **O** - Observed | Has anyone observed you stop breathing during your sleep? | **+1** |
| **P** - Pressure | Do you have or are you being treated for high blood pressure? | **+1** |
| **B** - BMI | Is your Body Mass Index (BMI) greater than 35 kg/m²? | **+1** |
| **A** - Age | Are you older than 50 years old? | **+1** |
| **N** - Neck | Is your neck circumference greater than 40 cm? | **+1** |
| **G** - Gender | Are you male? | **+1** |

---

## Risk Interpretation

The total score (0-8) stratifies the risk of having Obstructive Sleep Apnea:

| Total Score | Risk Level |
| :--- | :--- |
| **0–2** | Low Risk |
| **3–4** | Intermediate Risk |
| **5–8** | High Risk |

*Note: STOP-BANG is a screening tool, not a diagnostic tool for sleep apnea.*

---

## Engine Required Variables

To calculate the STOP-BANG score via the `ScoringEngine`, the `EmployeeHealthData` object **must** have the following fields fully populated (none can be null):

- `snoring` (bool)
- `tired` (bool)
- `observed_apnea` (bool)
- `hypertension_medication` (bool)
- `weight` (float - for BMI calculation)
- `height` (float - for BMI calculation)
- `age` (int)
- `neck_circumference` (float)
- `sex` (str: "M" or "F")

If at least one of these values is missing, the calculator will return a result with the `NOT_CALCULABLE` status.
