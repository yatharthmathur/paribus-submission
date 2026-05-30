from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class CreateHospitalCommand:
    name: str
    address: str
    phone: str
    creation_batch_id: UUID | None = None


@dataclass(slots=True, frozen=True)
class UpdateHospitalCommand:
    hospital_id: int
    name: str
    address: str
    phone: str


@dataclass(slots=True, frozen=True)
class DeleteHospitalCommand:
    hospital_id: int


@dataclass(slots=True, frozen=True)
class DeleteHospitalsByBatchCommand:
    batch_id: UUID


@dataclass(slots=True, frozen=True)
class ActivateHospitalsByBatchCommand:
    batch_id: UUID
