from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status

from app.api.dependencies import get_hospital_service
from app.application.commands import (
    ActivateHospitalsByBatchCommand,
    DeleteHospitalCommand,
    DeleteHospitalsByBatchCommand,
)
from app.application.services import HospitalService
from app.core.config import settings
from app.domain.hospital import HospitalFilters
from app.schemas.hospital import HospitalCreate, HospitalRead, HospitalUpdate

router = APIRouter()


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


@router.put("/hospitals/{hospital_id}", response_model=HospitalRead, tags=["hospitals"])
def update_hospital(
    hospital_id: int,
    payload: HospitalUpdate,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> HospitalRead:
    hospital = service.update_hospital(payload.to_command(hospital_id))
    return HospitalRead.from_domain(hospital)


@router.delete(
    "/hospitals/{hospital_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["hospitals"]
)
def delete_hospital(
    hospital_id: int,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> Response:
    service.delete_hospital(DeleteHospitalCommand(hospital_id=hospital_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/hospitals/batch/{batch_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["hospitals"]
)
def delete_hospitals_by_batch(
    batch_id: UUID,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> Response:
    service.delete_hospitals_by_batch(DeleteHospitalsByBatchCommand(batch_id=batch_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/hospitals/batch/{batch_id}/activate",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["hospitals"],
)
def activate_hospitals_by_batch(
    batch_id: UUID,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> Response:
    service.activate_hospitals_by_batch(ActivateHospitalsByBatchCommand(batch_id=batch_id))
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/hospitals", response_model=list[HospitalRead], tags=["hospitals"])
def list_hospitals(
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> list[HospitalRead]:
    hospitals = service.list_hospitals()
    return [HospitalRead.from_domain(hospital) for hospital in hospitals]


@router.get("/hospitals/{hospital_id}", response_model=HospitalRead, tags=["hospitals"])
def get_hospital(
    hospital_id: int,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> HospitalRead:
    hospital = service.get_hospital(hospital_id)
    return HospitalRead.from_domain(hospital)


@router.get("/hospitals/batch/{batch_id}", response_model=list[HospitalRead], tags=["hospitals"])
def get_hospitals_by_batch_id(
    batch_id: UUID,
    service: Annotated[HospitalService, Depends(get_hospital_service)],
) -> list[HospitalRead]:
    hospitals = service.list_hospitals(HospitalFilters(creation_batch_id=batch_id))
    return [HospitalRead.from_domain(hospital) for hospital in hospitals]
