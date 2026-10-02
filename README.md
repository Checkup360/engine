# Checkup360 Engine (Risk Scoring Engine)

Deterministic health risk calculation microservice for **Checkup360**, built with **FastAPI** and managed via **uv**.

The engine computes clinically validated risk scores (such as FINDRISC and STOP-BANG) based on patient anthropometrics, lifestyle habits, and medical history.

---

## Architecture

The scoring engine strictly enforces **Hexagonal Architecture (Ports and Adapters)**:

- **Domain (`app/domain`):** Entities, Value Objects, and the pure Python `ScoringEngine`. Completely decoupled from web frameworks and external libraries (no FastAPI, Pydantic, or DB imports).
- **Application (`app/application`):** Use cases and internal DTOs orchestrating scoring logic.
- **Infrastructure (`app/infrastructure`):** External adapters, serialization, and configurations.
- **Presentation (`app/presentation`):** FastAPI controllers, HTTP request/response schemas, and dependency injection.

---

## Prerequisites

- **Python**: `>=3.12`
- **uv** (Astral): Fast Python package and virtual environment manager.

Install `uv` if not already installed:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

---

## Getting Started

### 1. Setup Environment

```bash
cd engine
uv venv
uv sync
```

### 2. Environment Variables

Copy the example environment file and configure settings as needed (documented in `.env.example`):

```bash
cp .env.example .env
```

---

## Running the Development Server

Start the local dev server using the provided `Makefile`:

```bash
make dev
```

*(Or directly: `uv run fastapi dev app/presentation/main.py --port 8001`)*

The service will run at:
`http://localhost:8001`
- **Interactive Swagger UI:** `http://localhost:8001/docs`
- **ReDoc Documentation:** `http://localhost:8001/redoc`

---

## Testing and Quality Assurance

```bash
# Run pytest with code coverage
make test

# Lint codebase (Ruff)
make lint

# Format code (Ruff)
make format

# Run full pre-commit pipeline (format + lint + test)
make pre-commit
```

---

## API Usage

The main endpoint to compute health scores is `POST /risk-scores/{score_id}`.

**Score direction:** every response exposes `health_index`, a 0–100 value where
**higher means healthier**. Calculators internally express clinical severity as
`risk_value` (higher is riskier); the inversion happens only in
`ScoreResult.health_index`. `risk_value` is never exposed by the API.

**Health topics:** every calculator declares the health topic it informs
(`RiskScoreCalculator.topic`: a stable `key` plus a readable `label`), exposed
by `GET /risk-scores/catalog` as `topic_key` and `topic_label`. The key is what
organizations weight and enable, and what content is tagged with. Adding a new
calculator with its topic is enough for it to appear as a content category in
the backend, the CMS and the member app.

### Available Risk Models (`score_id`):
- `findrisc`: 10-year risk assessment for Type 2 Diabetes Mellitus (Finnish Diabetes Risk Score).
- `stop_bang`: STOP-BANG screening questionnaire for Obstructive Sleep Apnea (OSA) risk.

### Example 1: Compute FINDRISC Score

```bash
curl -X 'POST' \
  'http://localhost:8001/risk-scores/findrisc' \
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

### Example 2: Compute STOP-BANG Score

```bash
curl -X 'POST' \
  'http://localhost:8001/risk-scores/stop_bang' \
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

---

## Releases

Tagging a commit with a semantic version (e.g., `git tag v0.1.0 && git push origin v0.1.0`) automatically triggers the GitHub Actions workflow to build and publish the container image to GitHub Container Registry (GHCR).
