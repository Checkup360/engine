# Engine - Risk Scoring Engine

Engine is a production-grade occupational health platform focused on deterministic health scoring. It follows Clean/Hexagonal Architecture to decouple business rules from infrastructure and presentation frameworks.

## API Usage

The primary endpoint for calculating a health risk score is `POST /risk-scores/{score_id}`.

### Calculate a Specific Risk Score

Send a `POST` request with the model identifier in the path (`findrisc`, `stop_bang`) along with the patient's health data in the JSON body. The score result for that specific model is returned directly.

**Endpoint**: `POST /risk-scores/{score_id}`

#### Example: Calculate STOP-BANG

```bash
curl -X 'POST' \
  'http://localhost:8000/risk-scores/stop_bang' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "age": 55,
  "sex": "M",
  "weight": 95,
  "height": 1.75,
  "snoring": true,
  "tired": true,
  "observed_apnea": false,
  "hypertension_medication": true,
  "neck_circumference": 43
}'
```

#### Example: Calculate FINDRISC

```bash
curl -X 'POST' \
  'http://localhost:8000/risk-scores/findrisc' \
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
  "family_diabetes": "none"
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
