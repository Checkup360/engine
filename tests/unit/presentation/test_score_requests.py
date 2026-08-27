"""Unit tests for score-specific request models."""

from app.domain.entities.findrisc_data import FindriscData
from app.domain.entities.stop_bang_data import StopBangData
from app.presentation.api.request_models.scores.findrisc_request import (
    FindriscRequest,
)
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
        family_diabetes="none",
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
    assert data.family_diabetes == "none"


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
