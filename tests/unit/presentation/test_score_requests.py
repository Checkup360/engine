import pytest
from pydantic import ValidationError

from app.domain.entities.eoss_data import EOSSData
from app.domain.entities.findrisc_data import FindriscData
from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData
from app.domain.entities.phq9_data import PHQ9_ITEM_FIELDS, Phq9Data
from app.domain.entities.stop_bang_data import StopBangData
from app.presentation.api.request_models.scores.audit_c_request import AuditCRequest
from app.presentation.api.request_models.scores.eoss_request import EOSSRequest
from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
from app.presentation.api.request_models.scores.metabolic_syndrome_request import (
    MetabolicSyndromeRequest,
)
from app.presentation.api.request_models.scores.phq9_request import Phq9Request
from app.presentation.api.request_models.scores.score2_request import Score2Request
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


def test_eoss_request_to_domain() -> None:
    data = EOSSRequest(
        physical_health_stage=1,
        mental_health_stage=2,
        functional_stage=0,
    ).to_domain()

    assert isinstance(data, EOSSData)
    assert data.mental_health_stage == 2


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
    with pytest.raises(ValidationError) as exc_info:
        StopBangRequest.model_validate({"age": 50})

    errors = exc_info.value.errors()
    missing_fields = {e["loc"][0] for e in errors}
    assert "snoring" in missing_fields
    assert "neck_circumference" in missing_fields


@pytest.mark.parametrize(
    "sex_input,expected_sex",
    [("m", "M"), ("f", "F"), ("M", "M"), ("F", "F")],
)
@pytest.mark.parametrize(
    "model_cls,base_payload",
    [
        (
            AuditCRequest,
            {"frequency": 1, "quantity": 1, "heavy_drinking": 1},
        ),
        (
            FindriscRequest,
            {
                "age": 45,
                "weight": 85.0,
                "height": 1.80,
                "waist_circumference": 96.0,
                "daily_physical_activity": True,
                "fruits_vegetables": True,
                "hypertension_medication": False,
                "previous_high_glucose": False,
                "family_diabetes": "no",
            },
        ),
        (
            StopBangRequest,
            {
                "snoring": True,
                "tired": True,
                "observed_apnea": False,
                "hypertension_medication": True,
                "weight": 90.0,
                "height": 1.75,
                "age": 52,
                "neck_circumference": 42.0,
            },
        ),
        (
            Score2Request,
            {
                "age": 50,
                "smoker": False,
                "systolic_blood_pressure": 120.0,
                "total_cholesterol": 5.0,
                "hdl_cholesterol": 1.2,
                "risk_region": "moderate",
            },
        ),
        (
            MetabolicSyndromeRequest,
            {
                "waist_circumference": 105.0,
                "triglycerides": 180.0,
                "hdl_cholesterol": 38.0,
                "systolic_blood_pressure": 128.0,
                "diastolic_blood_pressure": 82.0,
                "hypertension_medication": False,
                "fasting_glucose": 95.0,
                "glucose_lowering_medication": False,
            },
        ),
    ],
)
def test_score_requests_normalize_sex_and_pass_to_domain(
    model_cls: type, base_payload: dict, sex_input: str, expected_sex: str
) -> None:
    payload = {**base_payload, "sex": sex_input}
    req = model_cls.model_validate(payload)
    assert req.sex == expected_sex
    domain_entity = req.to_domain()
    assert domain_entity.sex == expected_sex


@pytest.mark.parametrize("invalid_sex", ["x", "male", "FEMALE", 1, None])
@pytest.mark.parametrize(
    "model_cls,base_payload",
    [
        (AuditCRequest, {"frequency": 1, "quantity": 1, "heavy_drinking": 1}),
        (
            FindriscRequest,
            {
                "age": 45,
                "weight": 85.0,
                "height": 1.80,
                "waist_circumference": 96.0,
                "daily_physical_activity": True,
                "fruits_vegetables": True,
                "hypertension_medication": False,
                "previous_high_glucose": False,
                "family_diabetes": "no",
            },
        ),
        (
            StopBangRequest,
            {
                "snoring": True,
                "tired": True,
                "observed_apnea": False,
                "hypertension_medication": True,
                "weight": 90.0,
                "height": 1.75,
                "age": 52,
                "neck_circumference": 42.0,
            },
        ),
        (
            Score2Request,
            {
                "age": 50,
                "smoker": False,
                "systolic_blood_pressure": 120.0,
                "total_cholesterol": 5.0,
                "hdl_cholesterol": 1.2,
                "risk_region": "moderate",
            },
        ),
        (
            MetabolicSyndromeRequest,
            {
                "waist_circumference": 105.0,
                "triglycerides": 180.0,
                "hdl_cholesterol": 38.0,
                "systolic_blood_pressure": 128.0,
                "diastolic_blood_pressure": 82.0,
                "hypertension_medication": False,
                "fasting_glucose": 95.0,
                "glucose_lowering_medication": False,
            },
        ),
    ],
)
def test_score_requests_reject_invalid_sex(
    model_cls: type, base_payload: dict, invalid_sex: object
) -> None:
    with pytest.raises(ValidationError):
        model_cls.model_validate({**base_payload, "sex": invalid_sex})
