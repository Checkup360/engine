dev:
	uv run fastapi dev app/presentation/main.py --port 8001

test:
	COVERAGE_CORE=sysmon uv run pytest

lint:
	uv run ruff check .

format:
	uv run ruff format .
