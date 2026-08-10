import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.api.routers import version

load_dotenv()

app = FastAPI(
    title="Motor",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("PUBLIC_WEB_ORIGIN", "http://localhost:8000")],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(version.router)


@app.get("/")
def root() -> dict[str, bool]:
    return {"ok": True}
