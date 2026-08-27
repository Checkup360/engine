import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    InvalidHealthDataError,
    ScoreCalculatorNotFoundError,
)
from app.presentation.api.routers import risk_score, version

load_dotenv()

app = FastAPI(
    title="Engine",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("PUBLIC_WEB_ORIGIN", "http://localhost:8000")],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ScoreCalculatorNotFoundError)
def score_calculator_not_found_handler(
    request: Request, exc: ScoreCalculatorNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidHealthDataError)
def invalid_health_data_handler(
    request: Request, exc: InvalidHealthDataError
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


app.include_router(version.router)
app.include_router(risk_score.router)


@app.get("/")
def root() -> dict[str, bool]:
    return {"ok": True}
