from fastapi import APIRouter

from app.core.config import settings

router = APIRouter()


@router.get("/", tags=["meta"])
def read_root() -> dict[str, str]:
    return {
        "message": f"Welcome to {settings.app_name}",
        "environment": settings.environment,
        "version": settings.app_version,
    }


@router.get("/health", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "version": settings.app_version,
    }
