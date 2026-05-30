from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID


@dataclass(slots=True)
class Hospital:
    name: str
    address: str
    phone: str
    creation_batch_id: UUID
    active: bool = True
    id: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(slots=True, frozen=True)
class HospitalFilters:
    creation_batch_id: UUID | None = None
