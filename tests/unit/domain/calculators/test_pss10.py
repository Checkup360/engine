"""BDD Unit tests for PSS-10 Perceived Stress Scale item reversal logic."""

from app.domain.calculators.pss10 import PSS10Calculator
from app.domain.entities.pss10_data import Pss10Data
from app.domain.value_objects.score_result import CalculationStatus


def test_bdd_pss10_item_reversal_logic_q4_q5_q7_q8() -> None:
    """
    Given: An operator answers '0' (Never) to all 10 questions.
    When: The PSS-10 calculator executes.
    Then: The 4 reversed items (Q4, Q5, Q7, Q8) MUST invert from 0 to 4 (4 - 0 = 4),
          yielding a total score of 16/40 (Moderate risk).
    """
    # Given
    data = Pss10Data(
        pss10_q1=0,
        pss10_q2=0,
        pss10_q3=0,
        pss10_q4=0,  # Reversed -> 4
        pss10_q5=0,  # Reversed -> 4
        pss10_q6=0,
        pss10_q7=0,  # Reversed -> 4
        pss10_q8=0,  # Reversed -> 4
        pss10_q9=0,
        pss10_q10=0,
    )
    calculator = PSS10Calculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.contributing_factors["pss10_q1"] == 0.0
    assert result.contributing_factors["pss10_q4"] == 4.0
    assert result.contributing_factors["pss10_q5"] == 4.0
    assert result.contributing_factors["pss10_q7"] == 4.0
    assert result.contributing_factors["pss10_q8"] == 4.0
    assert result.raw_value == 16.0
    assert result.risk_level == "Moderate risk"
    assert result.risk_value == 25.8


def test_bdd_pss10_optimal_zero_stress_profile() -> None:
    """
    Given: An operator answers '0' to direct items and '4' to reversed
           items (which invert to 0).
    When: The PSS-10 calculator executes.
    Then: Total score MUST be 0/40 with 'Low risk' and 0.0 normalized score.
    """
    # Given
    data = Pss10Data(
        pss10_q1=0,
        pss10_q2=0,
        pss10_q3=0,
        pss10_q4=4,  # Reversed -> 0
        pss10_q5=4,  # Reversed -> 0
        pss10_q6=0,
        pss10_q7=4,  # Reversed -> 0
        pss10_q8=4,  # Reversed -> 0
        pss10_q9=0,
        pss10_q10=0,
    )
    calculator = PSS10Calculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 0.0
    assert result.risk_level == "Low risk"
    assert result.risk_value == 0.0
    assert result.attention_flags["severe_stress_or_burnout"] is False


def test_bdd_pss10_high_risk_severe_stress_burnout() -> None:
    """
    Given: An operator answers '3' or '4' across questions resulting
           in a score >= 27.
    When: The PSS-10 calculator executes.
    Then: The risk level MUST be 'High risk' with
          severe_stress_or_burnout flag set to True.
    """
    # Given
    data = Pss10Data(
        pss10_q1=3,
        pss10_q2=3,
        pss10_q3=3,
        pss10_q4=0,  # Reversed -> 4
        pss10_q5=0,  # Reversed -> 4
        pss10_q6=3,
        pss10_q7=0,  # Reversed -> 4
        pss10_q8=0,  # Reversed -> 4
        pss10_q9=3,
        pss10_q10=3,
    )
    # Raw total = 3+3+3 + 4+4 + 3 + 4+4 + 3+3 = 34
    calculator = PSS10Calculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 34.0
    assert result.risk_level == "High risk"
    assert result.attention_flags["severe_stress_or_burnout"] is True
    assert result.risk_value == 77.4
