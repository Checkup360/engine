# Motor - Risk Scoring Engine

Motor is a production-grade occupational health platform focused on deterministic health scoring. It follows Clean/Hexagonal Architecture to decouple business rules from infrastructure and presentation frameworks.

## API Usage

The primary endpoint for calculating health risk scores is `/risk-scores`.

### 1. Calculate All Scores

To calculate all available risk scores (e.g., FINDRISC, STOP-BANG), send a `POST` request with the patient's health data. The scoring engine will automatically determine if it has enough data for each calculator.

**Endpoint**: `POST /risk-scores`

```bash
curl -X 'POST' \
  'http://localhost:8000/risk-scores' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 45,
  "sex": "M",
  "weight": 90,
  "height": 1.75,
  "waist_circumference": 100,
  "daily_physical_activity": false,
  "fruits_vegetables": false,
  "hypertension_medication": false,
  "previous_high_glucose": false,
  "family_diabetes": "none",
  "snoring": true,
  "tired": true,
  "observed_apnea": false,
  "neck_circumference": 42
}'
```

### 2. Calculate Specific Scores (Parameterized)

If you only want to evaluate specific risk models (saving computation time), you can parameterize the request using the `target_scores` query parameter. You can provide this parameter multiple times for multiple scores.

**Endpoint**: `POST /risk-scores?target_scores={score_id}`

**Example: Calculate only STOP-BANG**

```bash
curl -X 'POST' \
  'http://localhost:8000/risk-scores?target_scores=stop_bang' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 45,
  "sex": "M",
  "weight": 90,
  "height": 1.75,
  "snoring": true,
  "tired": true,
  "observed_apnea": false,
  "hypertension_medication": false,
  "neck_circumference": 42
}'
```

**Example: Calculate FINDRISC and STOP-BANG explicitly**

```bash
curl -X 'POST' \
  'http://localhost:8000/risk-scores?target_scores=findrisc&target_scores=stop_bang' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 45,
  "sex": "M",
  "weight": 90,
  "height": 1.75
}'
```

### Available Score IDs
- `findrisc`: FINDRISC diabetes risk (Type 2).
- `stop_bang`: STOP-BANG risk for sleep apnea screening.

## Architecture

This project strictly adheres to Hexagonal Architecture (Ports and Adapters):
- **Domain**: Contains Entities, Value Objects, and the pure Python `ScoringEngine`.
- **Application**: Contains Use Cases and DTOs that orchestrate the domain.
- **Infrastructure**: Adapters for databases, email, etc.
- **Presentation**: FastAPI controllers, dependency injection, and HTTP models.

Business logic is strictly isolated in the Domain layer and never leaks into Presentation or Infrastructure.
