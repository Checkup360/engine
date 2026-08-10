"""Use case for computing the overall risk score."""

from __future__ import annotations

from app.application.dto.risk_score_dto import (
    ComputeRiskScoreCommand,
    RiskAssessmentDTO,
)
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.services.scoring_engine import ScoringEngine


class ComputeRiskScoreUseCase:
    """
    Orchestrates the risk scoring process.
    """

    def __init__(self, engine: ScoringEngine) -> None:
        self._engine = engine

    def execute(self, command: ComputeRiskScoreCommand) -> RiskAssessmentDTO:
        """
        Executes the scoring engine with the provided health data.
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
        results = self._engine.compute_scores(health_data)

        # Return Application DTO
        return RiskAssessmentDTO(scores=results)
