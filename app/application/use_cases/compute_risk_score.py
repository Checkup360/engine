"""Use case for computing the overall risk score."""

from __future__ import annotations

from app.application.dto.risk_score_dto import ComputeRiskScoreCommand
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.services.scoring_engine import ScoringEngine
from app.domain.value_objects.score_result import ScoreResult


class ComputeRiskScoreUseCase:
    """
    Orchestrates the risk scoring process for a specific model.
    """

    def __init__(self, engine: ScoringEngine) -> None:
        self._engine = engine

    def execute(self, command: ComputeRiskScoreCommand) -> ScoreResult:
        """
        Executes the scoring engine for the requested score_id
        with the provided health data.
        """
        # Map Command -> Domain Entity
        health_data = EmployeeHealthData(
            age=command.age,
            sex=command.sex,
            weight=command.weight,
            height=command.height,
            waist_circumference=command.waist_circumference,
            systolic_blood_pressure=command.systolic_blood_pressure,
            total_cholesterol=command.total_cholesterol,
            hdl=command.hdl,
            triglycerides=command.triglycerides,
            smoker=command.smoker,
            daily_physical_activity=command.daily_physical_activity,
            fruits_vegetables=command.fruits_vegetables,
            hypertension_medication=command.hypertension_medication,
            previous_high_glucose=command.previous_high_glucose,
            family_diabetes=command.family_diabetes,
            snoring=command.snoring,
            tired=command.tired,
            observed_apnea=command.observed_apnea,
            neck_circumference=command.neck_circumference,
        )

        # Execute Domain Logic
        return self._engine.compute_score(score_id=command.score_id, data=health_data)
