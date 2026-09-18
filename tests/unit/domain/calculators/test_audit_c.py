"""BDD Unit tests for AUDIT-C alcohol risk calculator gender cutoff logic."""

from app.domain.calculators.audit_c import AuditCCalculator
from app.domain.entities.audit_c_data import AuditCData
from app.domain.value_objects.score_result import CalculationStatus


def test_bdd_audit_c_gender_cutoff_score_3_is_low_risk_for_males() -> None:
    """
    Given: A male operator with an AUDIT-C total score of 3
           (frequency=1, quantity=1, heavy_drinking=1).
    When: The AUDIT-C calculator executes with sex='M'.
    Then: The risk level MUST be 'Low risk' (positive_screening = False)
          because male threshold is >= 4.
    """
    # Given
    data = AuditCData(frequency=1, quantity=1, heavy_drinking=1, sex="M")
    calculator = AuditCCalculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 3.0
    assert result.risk_level == "Low risk"
    assert result.attention_flags["positive_screening"] is False
    assert result.normalized_value == 37.5


def test_bdd_audit_c_gender_cutoff_score_3_is_high_risk_for_females() -> None:
    """
    Given: A female operator with an AUDIT-C total score of 3
           (frequency=1, quantity=1, heavy_drinking=1).
    When: The AUDIT-C calculator executes with sex='F'.
    Then: The risk level MUST be 'High risk' (positive_screening = True)
          because female threshold is >= 3.
    """
    # Given
    data = AuditCData(frequency=1, quantity=1, heavy_drinking=1, sex="F")
    calculator = AuditCCalculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 3.0
    assert result.risk_level == "High risk"
    assert result.attention_flags["positive_screening"] is True
    assert result.normalized_value == 51.0


def test_bdd_audit_c_male_score_4_triggers_high_risk() -> None:
    """
    Given: A male operator with an AUDIT-C total score of 4
           (frequency=2, quantity=1, heavy_drinking=1).
    When: The AUDIT-C calculator executes with sex='M'.
    Then: The risk level MUST be 'High risk' (positive_screening = True).
    """
    # Given
    data = AuditCData(frequency=2, quantity=1, heavy_drinking=1, sex="M")
    calculator = AuditCCalculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 4.0
    assert result.risk_level == "High risk"
    assert result.attention_flags["positive_screening"] is True
    assert result.normalized_value == 51.0
