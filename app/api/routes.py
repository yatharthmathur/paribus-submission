from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_hospital_service
from app.application.services import HospitalService
from app.core.config import settings
from app.domain.hospital import HospitalFilters
from app.schemas.hospital import HospitalCreate, HospitalRead

router = APIRouter()
ActiveFilter = Annotated[bool | None, Query()]
BatchFilter = Annotated[UUID | None, Query()]


@router.get("/", tags=["health"])
def healthcheck() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
        "version": settings.app_version,
    }


@router.post(
    "/hospitals",
    response_model=HospitalRead,
    status_code=status.HTTP_201_CREATED,
    tags=["hospitals"],
)
def create_hospital(
    payload: HospitalCreate,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> HospitalRead:
    hospital = service.create_hospital(payload.to_command())
    return HospitalRead.from_domain(hospital)


@router.get("/hospitals", response_model=list[HospitalRead], tags=["hospitals"])
def list_hospitals(
    service: Annotated[HospitalService, Depends(get_hospital_service)],
    active: ActiveFilter = None,
    creation_batch_id: BatchFilter = None,
) -> list[HospitalRead]:
    hospitals = service.list_hospitals(
        HospitalFilters(active=active, creation_batch_id=creation_batch_id)
    )
    return [HospitalRead.from_domain(hospital) for hospital in hospitals]


@router.get("/hospitals/{hospital_id}", response_model=HospitalRead, tags=["hospitals"])
def get_hospital(
    hospital_id: int,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> HospitalRead:
    hospital = service.get_hospital(hospital_id)
    return HospitalRead.from_domain(hospital)
