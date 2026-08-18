"""Unit tests for the ComputeRiskScoreUseCase."""

from app.application.dto.risk_score_dto import ComputeRiskScoreCommand
from app.application.use_cases.compute_risk_score import ComputeRiskScoreUseCase
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.services.scoring_engine import ScoringEngine
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


class DummyEngine(ScoringEngine):
    def __init__(self) -> None:
        # Override to not require real calculators
        pass

    def compute_scores(
        self, data: EmployeeHealthData, target_scores: list[str] | None = None
    ) -> list[ScoreResult]:
        # Just return a dummy result
        return [
            ScoreResult(
                score_id="dummy",
                score_name="Dummy",
                domain="Test",
                status=CalculationStatus.CALCULATED,
                raw_value=1.0,
            )
        ]


def test_compute_risk_score_use_case_delegates_to_engine() -> None:
    engine = DummyEngine()
    use_case = ComputeRiskScoreUseCase(engine=engine)
    command = ComputeRiskScoreCommand(age=30, sex="M")

    result_dto = use_case.execute(command)

    assert len(result_dto.scores) == 1
    assert result_dto.scores[0].score_id == "dummy"
