# STOP-BANG (Obstructive Sleep Apnea Screening)

**Domain:** Sleep Apnea
**Health Topic:** `sleep_apnea` ("Sleep Apnea")
**Raw Score Range:** 0 to 8 points
**Standardized Scale:** 0 to 100 (`health_index`, higher is healthier)

The **STOP-BANG** questionnaire is a validated clinical screening tool for Obstructive Sleep Apnea (OSA). It assesses four self-reported symptoms (**STOP**) and four objective clinical parameters (**BANG**).

---

## 1. Questions & Clinical Parameters

Each affirmative response scores 1 point:

### STOP (Self-Reported Symptoms)
- **S (Snoring):** Do you snore loudly (louder than talking or loud enough to be heard through closed doors)?
- **T (Tired):** Do you often feel tired, fatigued, or sleepy during daytime?
- **O (Observed):** Has anyone observed you stop breathing or choking/gasping during your sleep?
- **P (Pressure):** Do you have or are you being treated for high blood pressure?

### BANG (Objective Measures)
- **B (BMI):** Body Mass Index $> 35\text{ kg/m}^2$.
- **A (Age):** Age $> 50$ years old.
- **N (Neck):** Neck circumference $> 40\text{ cm}$.
- **G (Gender):** Biological sex is Male (`M`).

---

## 2. Risk Value and Health Index (0–100 Scale)

The raw score is the sum of all 8 criteria ($\text{raw\_value} \in [0, 8]$).

### Internal Risk Value
$$\text{risk\_value} = \text{round}\left(\frac{\text{raw\_value}}{8.0} \times 100.0, 1\right)$$

### Health Index
Exposed in `ScoreResult.health_index` according to the platform standard (**higher is healthier**):
$$\text{health\_index} = 100.0 - \text{risk\_value}$$

---

## 3. Clinical Risk Interpretation

| Total Score (0–8) | Risk Level | OSA Risk Stratification |
| :--- | :--- | :--- |
| **0–2** | **Low risk** | Low risk of moderate-to-severe OSA. |
| **3–4** | **Moderate risk** | Intermediate risk; sleep hygiene evaluation recommended. |
| **5–8** | **High risk** | High probability of moderate-to-severe OSA; polysomnography referral indicated. |

---

## 4. Engine Required Variables

To calculate STOP-BANG via the `ScoringEngine`, the `StopBangData` entity requires:

- `snoring` (bool)
- `tired` (bool)
- `observed_apnea` (bool)
- `hypertension_medication` (bool)
- `weight` (float, in kg)
- `height` (float, in meters)
- `age` (int)
- `neck_circumference` (float, in cm)
- `sex` (str: `"M"` or `"F"`)

If any field is missing, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

---

## 5. HTTP Endpoint & Example

- **Method:** `POST`
- **Path:** `/risk-scores/stop_bang`

### Request Payload

```json
{
  "age": 55,
  "sex": "M",
  "weight": 95,
  "height": 1.75,
  "snoring": true,
  "tired": true,
  "observed_apnea": false,
  "hypertension_medication": true,
  "neck_circumference": 43
}
```

### Example Response (200 OK)

```json
{
  "score_id": "stop_bang",
  "score_name": "STOP-BANG",
  "domain": "Sleep Apnea",
  "topic_key": "sleep_apnea",
  "topic_label": "Sleep Apnea",
  "status": "CALCULATED",
  "raw_value": 5.0,
  "health_index": 37.5,
  "risk_level": "High risk",
  "contributing_factors": {
    "snoring": 1.0,
    "tired": 1.0,
    "observed_apnea": 0.0,
    "pressure": 1.0,
    "bmi": 0.0,
    "age": 1.0,
    "neck": 1.0,
    "gender": 1.0
  },
  "attention_flags": {}
}
```
