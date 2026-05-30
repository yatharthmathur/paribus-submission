from datetime import UTC, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_serializer, field_validator

from app.application.commands import CreateHospitalCommand
from app.domain.hospital import Hospital


class HospitalBase(BaseModel):
    name: str
    address: str
    phone: str
    creation_batch_id: UUID
    active: bool = False


class HospitalCreate(HospitalBase):
    def to_command(self) -> CreateHospitalCommand:
        return CreateHospitalCommand(
            name=self.name,
            address=self.address,
            phone=self.phone,
            creation_batch_id=self.creation_batch_id,
            active=self.active,
        )


class HospitalRead(HospitalBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_domain(cls, hospital: Hospital) -> "HospitalRead":
        return cls.model_validate(hospital)

    @field_validator("created_at", mode="before")
    @classmethod
    def ensure_utc_datetime(cls, value: object) -> object:
        if isinstance(value, datetime) and value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        normalized = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
        return normalized.astimezone(UTC).isoformat().replace("+00:00", "Z")
