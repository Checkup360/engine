"""Unit tests for PHQ9Calculator."""

from app.domain.calculators.phq9 import PHQ9Calculator
from app.domain.entities.phq9_data import PHQ9_ITEM_FIELDS, Phq9Data
from app.domain.value_objects.score_result import CalculationStatus


def _data_with_scores(**overrides: int) -> Phq9Data:
    values = dict.fromkeys(PHQ9_ITEM_FIELDS, 0)
    values.update(overrides)
    return Phq9Data(**values)


def test_phq9_not_calculable_if_missing_data() -> None:
    calculator = PHQ9Calculator()
    result = calculator.calculate(Phq9Data())
    assert result.status == CalculationStatus.NOT_CALCULABLE
    assert result.score_id == "phq9"


def test_phq9_not_calculable_if_item_out_of_range() -> None:
    calculator = PHQ9Calculator()
    result = calculator.calculate(_data_with_scores(little_interest=4))
    assert result.status == CalculationStatus.NOT_CALCULABLE


def test_phq9_calculates_minimal_profile() -> None:
    calculator = PHQ9Calculator()
    result = calculator.calculate(_data_with_scores())

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 0
    assert result.risk_level == "None / minimal"
    assert result.normalized_value == 100.0
    assert result.contributing_factors["self_harm_flag"] == 0
    assert result.attention_flags["self_harm_thoughts"] is False
    assert result.explanation is None


def test_phq9_calculates_max_severity() -> None:
    calculator = PHQ9Calculator()
    result = calculator.calculate(
        Phq9Data(**dict.fromkeys(PHQ9_ITEM_FIELDS, 3))
    )

    assert result.status == CalculationStatus.CALCULATED
    assert result.raw_value == 27
    assert result.risk_level == "Severe"
    assert result.normalized_value == 0.0
    assert result.contributing_factors["self_harm_flag"] == 1
    assert result.attention_flags["self_harm_thoughts"] is True
    assert result.explanation is not None


def test_phq9_severity_bands() -> None:
    calculator = PHQ9Calculator()

    res_4 = calculator.calculate(
        _data_with_scores(little_interest=1, feeling_down=1, sleep_trouble=1, tired_energy=1)
    )
    assert res_4.raw_value == 4
    assert res_4.risk_level == "None / minimal"

    res_5 = calculator.calculate(
        _data_with_scores(
            little_interest=1,
            feeling_down=1,
            sleep_trouble=1,
            tired_energy=1,
            appetite=1,
        )
    )
    assert res_5.raw_value == 5
    assert res_5.risk_level == "Mild"

    res_10 = calculator.calculate(
        Phq9Data(
            little_interest=2,
            feeling_down=2,
            sleep_trouble=2,
            tired_energy=2,
            appetite=2,
            feeling_bad=0,
            concentration=0,
            psychomotor=0,
            self_harm_thoughts=0,
        )
    )
    assert res_10.raw_value == 10
    assert res_10.risk_level == "Moderate"

    res_15 = calculator.calculate(
        Phq9Data(
            little_interest=3,
            feeling_down=3,
            sleep_trouble=3,
            tired_energy=3,
            appetite=3,
            feeling_bad=0,
            concentration=0,
            psychomotor=0,
            self_harm_thoughts=0,
        )
    )
    assert res_15.raw_value == 15
    assert res_15.risk_level == "Moderately severe"

    res_20 = calculator.calculate(
        Phq9Data(
            little_interest=3,
            feeling_down=3,
            sleep_trouble=3,
            tired_energy=3,
            appetite=3,
            feeling_bad=3,
            concentration=2,
            psychomotor=0,
            self_harm_thoughts=0,
        )
    )
    assert res_20.raw_value == 20
    assert res_20.risk_level == "Severe"


def test_phq9_question_nine_flag_independent_of_total() -> None:
    calculator = PHQ9Calculator()
    result = calculator.calculate(_data_with_scores(self_harm_thoughts=1))

    assert result.raw_value == 1
    assert result.risk_level == "None / minimal"
    assert result.contributing_factors["self_harm_thoughts"] == 1
    assert result.contributing_factors["self_harm_flag"] == 1
    assert result.explanation is not None
