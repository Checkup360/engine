"""Unit tests for STOPBANGCalculator."""

from app.domain.calculators.stop_bang import STOPBANGCalculator
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.value_objects.score_result import CalculationStatus


def test_stop_bang_not_calculable_if_missing_data() -> None:
    calculator = STOPBANGCalculator()
    result = calculator.calculate(EmployeeHealthData())
    assert result.status == CalculationStatus.NOT_CALCULABLE
    assert result.score_id == "stop_bang"


def test_stop_bang_calculates_zero_risk_profile() -> None:
    calculator = STOPBANGCalculator()
    data = EmployeeHealthData(
        snoring=False,
        tired=False,
        observed_apnea=False,
        hypertension_medication=False,
        weight=60.0,
        height=1.75,  # BMI = 19.59
        age=30,
        neck_circumference=35.0,
        sex="F",
    )
    result = calculator.calculate(data)

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 0
    assert result.risk_level == "Low"
    assert result.contributing_factors["snoring"] == 0
    assert result.contributing_factors["tired"] == 0
    assert result.contributing_factors["observed_apnea"] == 0
    assert result.contributing_factors["pressure"] == 0
    assert result.contributing_factors["bmi"] == 0
    assert result.contributing_factors["age"] == 0
    assert result.contributing_factors["neck"] == 0
    assert result.contributing_factors["gender"] == 0


def test_stop_bang_calculates_max_risk_profile() -> None:
    calculator = STOPBANGCalculator()
    data = EmployeeHealthData(
        snoring=True,
        tired=True,
        observed_apnea=True,
        hypertension_medication=True,
        weight=120.0,
        height=1.70,  # BMI = 41.5
        age=55,
        neck_circumference=45.0,
        sex="M",
    )
    result = calculator.calculate(data)

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 8
    assert result.risk_level == "High"
    assert result.contributing_factors["snoring"] == 1
    assert result.contributing_factors["tired"] == 1
    assert result.contributing_factors["observed_apnea"] == 1
    assert result.contributing_factors["pressure"] == 1
    assert result.contributing_factors["bmi"] == 1
    assert result.contributing_factors["age"] == 1
    assert result.contributing_factors["neck"] == 1
    assert result.contributing_factors["gender"] == 1


def test_stop_bang_risk_levels() -> None:
    calculator = STOPBANGCalculator()
    base_data = EmployeeHealthData(
        snoring=False,
        tired=False,
        observed_apnea=False,
        hypertension_medication=False,
        weight=60.0,
        height=1.75,
        age=30,
        neck_circumference=35.0,
        sex="F",
    )

    # 0-2: Low
    # 2 pts (snoring + male)
    data2 = EmployeeHealthData(**{**base_data.__dict__, "snoring": True, "sex": "M"})
    res2 = calculator.calculate(data2)
    assert res2.raw_value == 2
    assert res2.risk_level == "Low"

    # 3-4: Intermediate
    # 3 pts (snoring + male + tired)
    data3 = EmployeeHealthData(**{**data2.__dict__, "tired": True})
    res3 = calculator.calculate(data3)
    assert res3.raw_value == 3
    assert res3.risk_level == "Intermediate"

    # 4 pts (+ age > 50)
    data4 = EmployeeHealthData(**{**data3.__dict__, "age": 55})
    res4 = calculator.calculate(data4)
    assert res4.raw_value == 4
    assert res4.risk_level == "Intermediate"

    # 5-8: High
    # 5 pts (+ neck > 40)
    data5 = EmployeeHealthData(**{**data4.__dict__, "neck_circumference": 42.0})
    res5 = calculator.calculate(data5)
    assert res5.raw_value == 5
    assert res5.risk_level == "High"
