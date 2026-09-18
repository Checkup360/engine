"""BDD Unit tests for Standardized Nordic Questionnaire (NMQ)
Ergonomic Risk calculator.
"""

from app.domain.calculators.nordic_nmq import NordicNMQCalculator
from app.domain.entities.nordic_nmq_data import (
    NMQ_ANATOMICAL_ZONES,
    NordicNmqData,
    ZoneNmqData,
)
from app.domain.value_objects.score_result import CalculationStatus


def _build_baseline_zones(
    trouble_12m: bool = False,
    prevented_work: bool = False,
    trouble_7d: bool = False,
) -> dict[str, ZoneNmqData]:
    return {
        zone: ZoneNmqData(
            trouble_last_12_months=trouble_12m,
            prevented_work_last_12_months=prevented_work,
            trouble_last_7_days=trouble_7d,
        )
        for zone in NMQ_ANATOMICAL_ZONES
    }


def test_bdd_nmq_high_risk_when_work_prevented_in_any_zone() -> None:
    """
    Given: An operator reports work impediment (Q2 = True) in the lower back zone.
    When: The Nordic NMQ calculator executes.
    Then: The resulting risk level MUST be 'High risk' with normalized value 100.0.
    """
    # Given
    zones = _build_baseline_zones()
    zones["lower_back"] = ZoneNmqData(
        trouble_last_12_months=True,
        prevented_work_last_12_months=True,
        trouble_last_7_days=True,
    )
    data = NordicNmqData(zones=zones)
    calculator = NordicNMQCalculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.risk_level == "High risk"
    assert result.normalized_value == 100.0
    assert result.attention_flags["has_work_impediment"] is True


def test_bdd_nmq_moderate_risk_when_recent_pain_without_work_impediment() -> None:
    """
    Given: An operator reports pain in last 7 days (Q3 = True) in knees
           without work impediment.
    When: The Nordic NMQ calculator executes.
    Then: The resulting risk level MUST be 'Moderate risk' with normalized value 50.0.
    """
    # Given
    zones = _build_baseline_zones()
    zones["knees"] = ZoneNmqData(
        trouble_last_12_months=True,
        prevented_work_last_12_months=False,
        trouble_last_7_days=True,
    )
    data = NordicNmqData(zones=zones)
    calculator = NordicNMQCalculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.risk_level == "Moderate risk"
    assert result.normalized_value == 50.0
    assert result.attention_flags["has_work_impediment"] is False
    assert result.attention_flags["has_recent_7day_pain"] is True


def test_bdd_nmq_low_risk_when_12month_pain_only_without_recent_pain() -> None:
    """
    Given: An operator reports 12-month trouble (Q1 = True) in shoulders,
           but Q2 and Q3 are False for all zones.
    When: The Nordic NMQ calculator executes.
    Then: The resulting risk level MUST be 'Low risk' with normalized value 0.0.
    """
    # Given
    zones = _build_baseline_zones()
    zones["shoulders"] = ZoneNmqData(
        trouble_last_12_months=True,
        prevented_work_last_12_months=False,
        trouble_last_7_days=False,
    )
    data = NordicNmqData(zones=zones)
    calculator = NordicNMQCalculator()

    # When
    result = calculator.calculate(data)

    # Then
    assert result.status == CalculationStatus.CALCULATED
    assert result.risk_level == "Low risk"
    assert result.normalized_value == 0.0
    assert result.attention_flags["has_work_impediment"] is False
    assert result.attention_flags["has_recent_7day_pain"] is False
    assert result.attention_flags["has_12month_pain"] is True
