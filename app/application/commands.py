from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class CreateHospitalCommand:
    name: str
    address: str
    phone: str
    creation_batch_id: UUID | None = None
