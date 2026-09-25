"""Cross-score invariant test verifying risk direction across all 9 calculators."""

from __future__ import annotations

from typing import Any

import pytest

from app.domain.calculators.audit_c import AuditCCalculator
from app.domain.calculators.eoss import EOSSCalculator
from app.domain.calculators.findrisc import FINDRISCCalculator
from app.domain.calculators.metabolic_syndrome import MetabolicSyndromeCalculator
from app.domain.calculators.nordic_nmq import NordicNMQCalculator
from app.domain.calculators.phq9 import PHQ9Calculator
from app.domain.calculators.pss10 import PSS10Calculator
from app.domain.calculators.score2 import SCORE2Calculator
from app.domain.calculators.stop_bang import STOPBANGCalculator
from app.domain.entities.audit_c_data import AuditCData
from app.domain.entities.eoss_data import EOSSData
from app.domain.entities.findrisc_data import FindriscData
from app.domain.entities.metabolic_syndrome_data import MetabolicSyndromeData
from app.domain.entities.nordic_nmq_data import (
    NMQ_ANATOMICAL_ZONES,
    NordicNmqData,
    ZoneNmqData,
)
from app.domain.entities.phq9_data import PHQ9_ITEM_FIELDS, Phq9Data
from app.domain.entities.pss10_data import Pss10Data
from app.domain.entities.score2_data import Score2Data
from app.domain.entities.stop_bang_data import StopBangData
from app.domain.services.risk_score_calculator import RiskScoreCalculator
from app.domain.value_objects.score_result import CalculationStatus


@pytest.mark.parametrize(
    "calculator,best_case_data,worst_case_data",
    [
        (
            AuditCCalculator(),
            AuditCData(frequency=0, quantity=0, heavy_drinking=0, sex="M"),
            AuditCData(frequency=4, quantity=4, heavy_drinking=4, sex="M"),
        ),
        (
            EOSSCalculator(),
            EOSSData(
                physical_health_stage=0, mental_health_stage=0, functional_stage=0
            ),
            EOSSData(
                physical_health_stage=4, mental_health_stage=4, functional_stage=4
            ),
        ),
        (
            FINDRISCCalculator(),
            FindriscData(
                age=25,
                weight=60.0,
                height=1.75,
                sex="M",
                waist_circumference=85.0,
                daily_physical_activity=True,
                fruits_vegetables=True,
                hypertension_medication=False,
                previous_high_glucose=False,
                family_diabetes="no",
            ),
            FindriscData(
                age=70,
                weight=120.0,
                height=1.65,
                sex="M",
                waist_circumference=115.0,
                daily_physical_activity=False,
                fruits_vegetables=False,
                hypertension_medication=True,
                previous_high_glucose=True,
                family_diabetes="first_degree",
            ),
        ),
        (
            MetabolicSyndromeCalculator(),
            MetabolicSyndromeData(
                sex="M",
                waist_circumference=85.0,
                triglycerides=100.0,
                hdl_cholesterol=55.0,
                systolic_blood_pressure=115.0,
                diastolic_blood_pressure=75.0,
                hypertension_medication=False,
                fasting_glucose=85.0,
                glucose_lowering_medication=False,
            ),
            MetabolicSyndromeData(
                sex="M",
                waist_circumference=115.0,
                triglycerides=250.0,
                hdl_cholesterol=30.0,
                systolic_blood_pressure=155.0,
                diastolic_blood_pressure=95.0,
                hypertension_medication=True,
                fasting_glucose=130.0,
                glucose_lowering_medication=True,
            ),
        ),
        (
            NordicNMQCalculator(),
            NordicNmqData(
                zones={
                    zone: ZoneNmqData(
                        trouble_last_12_months=False,
                        prevented_work_last_12_months=False,
                        trouble_last_7_days=False,
                    )
                    for zone in NMQ_ANATOMICAL_ZONES
                }
            ),
            NordicNmqData(
                zones={
                    zone: ZoneNmqData(
                        trouble_last_12_months=True,
                        prevented_work_last_12_months=True,
                        trouble_last_7_days=True,
                    )
                    for zone in NMQ_ANATOMICAL_ZONES
                }
            ),
        ),
        (
            PHQ9Calculator(),
            Phq9Data(**dict.fromkeys(PHQ9_ITEM_FIELDS, 0)),
            Phq9Data(**dict.fromkeys(PHQ9_ITEM_FIELDS, 3)),
        ),
        (
            PSS10Calculator(),
            Pss10Data(
                pss10_q1=0,
                pss10_q2=0,
                pss10_q3=0,
                pss10_q4=4,
                pss10_q5=4,
                pss10_q6=0,
                pss10_q7=4,
                pss10_q8=4,
                pss10_q9=0,
                pss10_q10=0,
            ),
            Pss10Data(
                pss10_q1=4,
                pss10_q2=4,
                pss10_q3=4,
                pss10_q4=0,
                pss10_q5=0,
                pss10_q6=4,
                pss10_q7=0,
                pss10_q8=0,
                pss10_q9=4,
                pss10_q10=4,
            ),
        ),
        (
            SCORE2Calculator(),
            Score2Data(
                age=40,
                sex="F",
                smoker=False,
                systolic_blood_pressure=100.0,
                total_cholesterol=3.5,
                hdl_cholesterol=2.0,
                risk_region="low",
            ),
            Score2Data(
                age=69,
                sex="M",
                smoker=True,
                systolic_blood_pressure=180.0,
                total_cholesterol=9.0,
                hdl_cholesterol=0.7,
                risk_region="very_high",
            ),
        ),
        (
            STOPBANGCalculator(),
            StopBangData(
                snoring=False,
                tired=False,
                observed_apnea=False,
                hypertension_medication=False,
                weight=60.0,
                height=1.75,
                age=30,
                neck_circumference=32.0,
                sex="F",
            ),
            StopBangData(
                snoring=True,
                tired=True,
                observed_apnea=True,
                hypertension_medication=True,
                weight=120.0,
                height=1.65,
                age=55,
                neck_circumference=46.0,
                sex="M",
            ),
        ),
    ],
    ids=[
        "audit_c",
        "eoss",
        "findrisc",
        "metabolic_syndrome",
        "nordic_nmq",
        "phq9",
        "pss10",
        "score2",
        "stop_bang",
    ],
)
def test_score_risk_direction_invariant(
    calculator: RiskScoreCalculator[Any],
    best_case_data: Any,
    worst_case_data: Any,
) -> None:
    """Verifies that for all 9 calculators, worst clinical case yields high
    normalized risk, best case yields low normalized risk, and directional
    monotonicity is preserved.
    """
    result_best = calculator.calculate(best_case_data)
    result_worst = calculator.calculate(worst_case_data)

    assert result_best.status == CalculationStatus.CALCULATED
    assert result_worst.status == CalculationStatus.CALCULATED

    assert result_best.normalized_value is not None
    assert result_worst.normalized_value is not None

    assert result_best.normalized_value < 15.0
    assert result_worst.normalized_value > 85.0
    assert result_worst.normalized_value > result_best.normalized_value
