from fastapi import APIRouter

router = APIRouter(prefix="/version", tags=["version"])


@router.get("")
def get_version() -> dict[str, str]:
    return {"version": "0.1.0"}
