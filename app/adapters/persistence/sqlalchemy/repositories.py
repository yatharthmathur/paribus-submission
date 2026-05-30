from datetime import UTC
from uuid import UUID

from app.adapters.persistence.sqlalchemy.models import HospitalRecord
from app.application.ports import HospitalRepository
from app.domain.hospital import Hospital, HospitalFilters
from sqlalchemy import Select, select
from sqlalchemy.orm import Session


class SqlAlchemyHospitalRepository(HospitalRepository):
    def __init__(self, session: Session):
        self._session = session

    def add(self, hospital: Hospital) -> Hospital:
        record = HospitalRecord(
            name=hospital.name,
            address=hospital.address,
            phone=hospital.phone,
            creation_batch_id=str(hospital.creation_batch_id),
            active=hospital.active,
        )
        self._session.add(record)
        self._session.flush()
        self._session.refresh(record)
        return self._to_domain(record)

    def get_by_id(self, hospital_id: int) -> Hospital | None:
        record = self._session.get(HospitalRecord, hospital_id)
        if record is None or not record.active:
            return None
        return self._to_domain(record)

    def update(self, hospital: Hospital) -> Hospital:
        if hospital.id is None:
            raise ValueError("Hospital id is required for update")

        record = self._session.get(HospitalRecord, hospital.id)
        if record is None or not record.active:
            raise ValueError("Cannot update a missing or inactive hospital")

        record.name = hospital.name
        record.address = hospital.address
        record.phone = hospital.phone
        self._session.flush()
        self._session.refresh(record)
        return self._to_domain(record)

    def delete_by_id(self, hospital_id: int) -> None:
        record = self._session.get(HospitalRecord, hospital_id)
        if record is None or not record.active:
            return

        record.active = False
        self._session.flush()

    def delete_by_batch_id(self, batch_id: UUID) -> int:
        records = list(
            self._session.scalars(
                select(HospitalRecord).where(
                    HospitalRecord.creation_batch_id == str(batch_id), HospitalRecord.active
                )
            ).all()
        )

        for record in records:
            record.active = False

        self._session.flush()
        return len(records)

    def activate_by_batch_id(self, batch_id: UUID) -> int:
        records = list(
            self._session.scalars(
                select(HospitalRecord).where(HospitalRecord.creation_batch_id == str(batch_id))
            ).all()
        )

        for record in records:
            record.active = True

        self._session.flush()
        return len(records)

    def list(self, filters: HospitalFilters | None = None) -> list[Hospital]:
        query: Select[tuple[HospitalRecord]] = (
            select(HospitalRecord).order_by(HospitalRecord.id).where(HospitalRecord.active)
        )

        if filters and filters.creation_batch_id is not None:
            query = query.where(HospitalRecord.creation_batch_id == str(filters.creation_batch_id))

        return [self._to_domain(record) for record in self._session.scalars(query).all()]

    @staticmethod
    def _to_domain(record: HospitalRecord) -> Hospital:
        created_at = record.created_at
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=UTC)

        return Hospital(
            id=record.id,
            name=record.name,
            address=record.address,
            phone=record.phone,
            creation_batch_id=UUID(record.creation_batch_id),
            active=record.active,
            created_at=created_at,
        )
