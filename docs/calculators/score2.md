# SCORE2 (Systematic Coronary Risk Evaluation 2)

**Domain:** Cardiovascular
**Score Range:** 0.0% to 100.0% (10-year fatal and non-fatal CVD risk)

The SCORE2 model estimates an individual's 10-year risk of a first fatal or non-fatal cardiovascular disease (CVD) event (myocardial infarction, stroke, or cardiovascular death) among apparently healthy adults aged 40–69 years without prior CVD or diabetes, using sex-specific competing-risk models and regional recalibration.

---

## Model Specification & Formulas

### 1. Centered / Transformed Predictor Variables

* $\text{cage} = (\text{age} - 60) / 5$
* $\text{csbp} = (\text{SBP} - 120) / 20$
* $\text{ctchol} = (\text{total cholesterol} - 6) / 1$ (cholesterol in $\text{mmol/L}$)
* $\text{chdl} = (\text{HDL cholesterol} - 1.3) / 0.5$ (cholesterol in $\text{mmol/L}$)
* $\text{smoking} = 1$ if current smoker, otherwise $0$

*(Note: Cholesterol values provided in $\text{mg/dL}$ are automatically converted to $\text{mmol/L}$ by dividing by $38.67$.)*

### 2. Regression Coefficients (Linear Predictor $\text{lp}$)

| Term | Men | Women |
| :--- | :--- | :--- |
| $\text{cage}$ | 0.3742 | 0.4648 |
| $\text{smoking}$ | 0.6012 | 0.7744 |
| $\text{csbp}$ | 0.2777 | 0.3131 |
| $\text{ctchol}$ | 0.1458 | 0.1002 |
| $\text{chdl}$ | -0.2698 | -0.2606 |
| $\text{cage} \times \text{smoking}$ | -0.0755 | -0.1088 |
| $\text{cage} \times \text{csbp}$ | -0.0255 | -0.0277 |
| $\text{cage} \times \text{ctchol}$ | -0.0281 | -0.0226 |
| $\text{cage} \times \text{chdl}$ | 0.0426 | 0.0613 |

**Men Linear Predictor:**
$$\text{lp} = 0.3742 \cdot \text{cage} + 0.6012 \cdot \text{smoking} + 0.2777 \cdot \text{csbp} + 0.1458 \cdot \text{ctchol} - 0.2698 \cdot \text{chdl} - 0.0755 \cdot \text{cage} \cdot \text{smoking} - 0.0255 \cdot \text{cage} \cdot \text{csbp} - 0.0281 \cdot \text{cage} \cdot \text{ctchol} + 0.0426 \cdot \text{cage} \cdot \text{chdl}$$

**Women Linear Predictor:**
$$\text{lp} = 0.4648 \cdot \text{cage} + 0.7744 \cdot \text{smoking} + 0.3131 \cdot \text{csbp} + 0.1002 \cdot \text{ctchol} - 0.2606 \cdot \text{chdl} - 0.1088 \cdot \text{cage} \cdot \text{smoking} - 0.0277 \cdot \text{cage} \cdot \text{csbp} - 0.0226 \cdot \text{cage} \cdot \text{ctchol} + 0.0613 \cdot \text{cage} \cdot \text{chdl}$$

### 3. Baseline Survival & Uncalibrated Risk

Baseline 10-year survival ($S_0$):
* **Men:** $S_0 = 0.9605$
* **Women:** $S_0 = 0.9776$

$$\text{uncalibrated\_risk} = 1 - S_0^{\exp(\text{lp})}$$

### 4. Regional Calibration

The uncalibrated risk is adjusted for the specific European risk region:
$$\text{calibrated\_risk} = 1 - \exp(-\exp(\text{scale1} + \text{scale2} \times \ln(-\ln(1 - \text{uncalibrated\_risk}))))$$

| Region | Men scale1 | Men scale2 | Women scale1 | Women scale2 |
| :--- | :--- | :--- | :--- | :--- |
| **Low** | -0.5699 | 0.7476 | -0.7380 | 0.7019 |
| **Moderate** | -0.1565 | 0.8009 | -0.3143 | 0.7701 |
| **High** | 0.3207 | 0.9360 | 0.5710 | 0.9369 |
| **Very high** | 0.5836 | 0.8294 | 0.9412 | 0.8329 |

### 5. Normalized Value (0–100 Scale)

For cross-score visualization in the Checkup360 UI, the calibrated risk percentage (`raw_value`) is mapped to a 0–100 severity scale:
$$\text{normalized\_value} = \min\left(100.0, \frac{\text{raw\_value}}{30.0} \times 100.0\right)$$

* **Normalization Ceiling (`_NORMALIZATION_RISK_CEILING_PERCENT = 30.0`):** A 10-year CVD risk $\ge 30\%$ represents maximum severity ($100$) on the unified scale. SCORE2's clinical risk bands already classify risk $\ge 20\%$ as "Very high risk".
* **Raw Value:** Remains un-capped to preserve the exact calibrated risk percentage.

---

## Risk Interpretation

| Calibrated 10-Year CVD Risk | Risk Level | Interpretation & Attention Flags |
| :--- | :--- | :--- |
| **< 5.0%** | Low risk | Optimal cardiovascular parameters; maintain healthy lifestyle. |
| **5.0% to < 10.0%** | Moderate risk | Lifestyle modifications and preventive monitoring advised. |
| **10.0% to < 20.0%** | High risk | Attention flag `high_cardiovascular_risk = true`. Healthcare consult advised. |
| **≥ 20.0%** | Very high risk | Attention flag `high_cardiovascular_risk = true`. Intensive risk factor management. |

---

## Engine Required Variables

To calculate SCORE2 via the `ScoringEngine`, the `Score2Data` object must have:

* `age` (int: 18–120 years)
* `sex` (str: "M" or "F")
* `smoker` (bool)
* `systolic_blood_pressure` (float: mmHg)
* `total_cholesterol` (float: mmol/L or mg/dL)
* `hdl_cholesterol` (float: mmol/L or mg/dL)
* `risk_region` (str: "low", "moderate", "high", or "very_high", defaults to "moderate")

If any required variable is missing, the calculator returns `CalculationStatus.NOT_CALCULABLE`.

## HTTP Endpoint

`POST /risk-scores/score2`

## Sources

* ESC / SCORE2 Working Group. SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe. *European Heart Journal*. 2021;42(25):2439–2454.
* European Society of Cardiology: SCORE2 and SCORE2-OP calculators.
