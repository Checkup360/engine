"""Unit tests for FINDRISCCalculator."""

from app.domain.calculators.findrisc import FINDRISCCalculator
from app.domain.entities.findrisc_data import FindriscData
from app.domain.value_objects.score_result import CalculationStatus


def test_findrisc_not_calculable_if_missing_data() -> None:
    calculator = FINDRISCCalculator()
    # Missing all data
    result = calculator.calculate(FindriscData())
    assert result.status == CalculationStatus.NOT_CALCULABLE
    assert result.score_id == "findrisc"


def test_findrisc_calculates_zero_risk_profile() -> None:
    calculator = FINDRISCCalculator()
    # Profile with all lowest risk options
    data = FindriscData(
        age=30,
        weight=60.0,
        height=1.75,  # BMI = 19.59
        sex="M",
        waist_circumference=90.0,
        daily_physical_activity=True,
        fruits_vegetables=True,
        hypertension_medication=False,
        previous_high_glucose=False,
        family_diabetes="no",
    )
    result = calculator.calculate(data)

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 0
    assert result.risk_level == "Low risk"
    assert result.contributing_factors["age"] == 0
    assert result.contributing_factors["bmi"] == 0
    assert result.contributing_factors["waist"] == 0
    assert result.contributing_factors["physical_activity"] == 0


def test_findrisc_calculates_high_risk_profile() -> None:
    calculator = FINDRISCCalculator()
    data = FindriscData(
        age=66,  # >=65 -> 4 pts
        weight=100.0,
        height=1.70,  # BMI = 34.6 -> 3 pts
        sex="F",
        waist_circumference=90.0,  # F >=88 -> 4 pts
        daily_physical_activity=False,  # -> 2 pts
        fruits_vegetables=False,  # -> 1 pt
        hypertension_medication=True,  # -> 2 pts
        previous_high_glucose=True,  # -> 5 pts
        family_diabetes="first_degree",  # -> 5 pts
    )
    result = calculator.calculate(data)

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 26
    assert result.risk_level == "Very high risk"
    assert result.contributing_factors["age"] == 4
    assert result.contributing_factors["bmi"] == 3
    assert result.contributing_factors["waist"] == 4
    assert result.contributing_factors["physical_activity"] == 2
    assert result.contributing_factors["fruits_vegetables"] == 1
    assert result.contributing_factors["hypertension"] == 2
    assert result.contributing_factors["high_glucose"] == 5
    assert result.contributing_factors["family_diabetes"] == 5


def test_findrisc_risk_levels() -> None:
    calculator = FINDRISCCalculator()
    base_data = FindriscData(
        weight=60.0,
        height=1.75,
        sex="M",
        waist_circumference=90.0,
        daily_physical_activity=True,
        fruits_vegetables=True,
        hypertension_medication=False,
        previous_high_glucose=False,
        family_diabetes="no",
    )

    # 0-6: Low
    # 0 pts total
    data0 = FindriscData(**{**base_data.__dict__, "age": 40})
    result = calculator.calculate(data0)
    assert result.risk_level == "Low risk"

    # 7-11: Slightly elevated (Need 7 pts)
    # age 55-64 (3) + BMI >=30 (3) + physical inactive (2) = 8 pts
    data7 = FindriscData(
        **{
            **base_data.__dict__,
            "age": 60,
            "weight": 100.0,
            "daily_physical_activity": False,
        }
    )
    result = calculator.calculate(data7)
    assert result.risk_level == "Slightly elevated risk"

    # 12-14: Moderate (Need 12 pts)
    # age 55-64 (3) + BMI >=30 (3) + waist >=102 (4) + inactive (2) = 12 pts
    data12 = FindriscData(
        **{
            **base_data.__dict__,
            "age": 60,
            "weight": 100.0,
            "waist_circumference": 105.0,
            "daily_physical_activity": False,
        }
    )
    result = calculator.calculate(data12)
    assert result.risk_level == "Moderate risk"

    # 15-20: High (Need 15 pts)
    # 12 pts + fam diabetes second degree (3) = 15 pts
    data15 = FindriscData(**{**data12.__dict__, "family_diabetes": "second_degree"})
    result = calculator.calculate(data15)
    assert result.risk_level == "High risk"

    # 21-26: Very high (Need 21 pts)
    # 12 pts + previous high glucose (5) + first degree fam (5) = 22 pts
    data22 = FindriscData(
        **{
            **data12.__dict__,
            "previous_high_glucose": True,
            "family_diabetes": "first_degree",
        }
    )
    result = calculator.calculate(data22)
    assert result.risk_level == "Very high risk"


def test_findrisc_edge_cases() -> None:
    calculator = FINDRISCCalculator()
    # Test BMI exactly 30, Waist exactly 102 (M), Waist exactly 88 (F)
    data_m = FindriscData(
        age=50,
        weight=86.7,
        height=1.70,
        sex="M",
        waist_circumference=102.0,
        daily_physical_activity=True,
        fruits_vegetables=True,
        hypertension_medication=False,
        previous_high_glucose=False,
        family_diabetes="no",
    )
    res_m = calculator.calculate(data_m)
    assert res_m.contributing_factors["bmi"] == 3  # ~30.0
    assert res_m.contributing_factors["waist"] == 4

    data_f = FindriscData(
        age=50,
        weight=86.7,
        height=1.70,
        sex="F",
        waist_circumference=88.0,
        daily_physical_activity=True,
        fruits_vegetables=True,
        hypertension_medication=False,
        previous_high_glucose=False,
        family_diabetes="no",
    )
    res_f = calculator.calculate(data_f)
    assert res_f.contributing_factors["waist"] == 4
