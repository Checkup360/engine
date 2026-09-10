"""Unit tests for score-specific request models."""

from app.domain.entities.findrisc_data import FindriscData
from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData
from app.domain.entities.phq9_data import PHQ9_ITEM_FIELDS, Phq9Data
from app.domain.entities.stop_bang_data import StopBangData
from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
from app.presentation.api.request_models.scores.metabolic_syndrome_request import (
    MetabolicSyndromeRequest,
)
from app.presentation.api.request_models.scores.phq9_request import Phq9Request
from app.presentation.api.request_models.scores.stop_bang_request import (
    StopBangRequest,
)


def test_findrisc_request_to_domain() -> None:
    req = FindriscRequest(
        age=45,
        sex="M",
        weight=85.0,
        height=1.80,
        waist_circumference=96.0,
        daily_physical_activity=True,
        fruits_vegetables=True,
        hypertension_medication=False,
        previous_high_glucose=False,
        family_diabetes="no",
    )

    data = req.to_domain()

    assert isinstance(data, FindriscData)
    assert data.age == 45
    assert data.sex == "M"
    assert data.weight == 85.0
    assert data.height == 1.80
    assert data.waist_circumference == 96.0
    assert data.daily_physical_activity is True
    assert data.fruits_vegetables is True
    assert data.hypertension_medication is False
    assert data.previous_high_glucose is False
    assert data.family_diabetes == "no"


def test_metabolic_syndrome_request_to_domain() -> None:
    req = MetabolicSyndromeRequest(
        sex="M",
        waist_circumference=105.0,
        triglycerides=180.0,
        hdl_cholesterol=38.0,
        systolic_blood_pressure=128.0,
        diastolic_blood_pressure=82.0,
        hypertension_medication=False,
        fasting_glucose=95.0,
        glucose_lowering_medication=False,
    )

    data = req.to_domain()

    assert isinstance(data, MetabolicSyndromeData)
    assert data.waist_circumference == 105.0
    assert data.hdl_cholesterol == 38.0


def test_stop_bang_request_to_domain() -> None:
    req = StopBangRequest(
        snoring=True,
        tired=True,
        observed_apnea=False,
        hypertension_medication=True,
        weight=90.0,
        height=1.75,
        age=52,
        neck_circumference=42.0,
        sex="M",
    )

    data = req.to_domain()

    assert isinstance(data, StopBangData)
    assert data.snoring is True
    assert data.tired is True
    assert data.observed_apnea is False
    assert data.hypertension_medication is True
    assert data.weight == 90.0
    assert data.height == 1.75
    assert data.age == 52
    assert data.neck_circumference == 42.0
    assert data.sex == "M"


def test_findrisc_request_raises_validation_error_on_missing_fields() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        FindriscRequest.model_validate({"age": 45})

    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "sex" in missing_fields
    assert "weight" in missing_fields


def test_phq9_request_to_domain() -> None:
    payload = dict.fromkeys(PHQ9_ITEM_FIELDS, 1)
    payload["self_harm_thoughts"] = 2
    req = Phq9Request(**payload)

    data = req.to_domain()

    assert isinstance(data, Phq9Data)
    assert data.little_interest == 1
    assert data.self_harm_thoughts == 2


def test_phq9_request_raises_validation_error_on_missing_fields() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        Phq9Request.model_validate({"little_interest": 1})

    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "feeling_down" in missing_fields
    assert "self_harm_thoughts" in missing_fields


def test_stop_bang_request_raises_validation_error_on_missing_fields() -> None:
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError) as exc_info:
        StopBangRequest.model_validate({"age": 50})

    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "snoring" in missing_fields
    assert "neck_circumference" in missing_fields
