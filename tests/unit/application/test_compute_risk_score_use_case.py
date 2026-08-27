"""Unit tests for the ComputeRiskScoreUseCase."""

from app.application.dto.risk_score_dto import ComputeRiskScoreCommand
from app.application.use_cases.compute_risk_score import ComputeRiskScoreUseCase
from app.domain.entities.employee_health_data import EmployeeHealthData
from app.domain.services.scoring_engine import ScoringEngine
from app.domain.value_objects.score_result import CalculationStatus, ScoreResult


class DummyEngine(ScoringEngine):
    def __init__(self) -> None:
        pass

    def compute_score(self, score_id: str, data: EmployeeHealthData) -> ScoreResult:
        return ScoreResult(
            score_id=score_id,
            score_name=f"Dummy {score_id}",
            domain="Test",
            status=CalculationStatus.CALCULATED,
            raw_value=1.0,
        )


def test_compute_risk_score_use_case_delegates_to_engine() -> None:
    engine = DummyEngine()
    use_case = ComputeRiskScoreUseCase(engine=engine)
    command = ComputeRiskScoreCommand(score_id="findrisc", age=30, sex="M")

    result = use_case.execute(command)

    assert result.score_id == "findrisc"
    assert result.raw_value == 1.0
    assert result.status == CalculationStatus.CALCULATED
