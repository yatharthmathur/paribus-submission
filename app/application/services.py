from collections.abc import Callable
from uuid import uuid4

from app.application.commands import CreateHospitalCommand
from app.application.ports import UnitOfWork
from app.domain.exceptions import HospitalNotFoundError, InvalidHospitalDataError
from app.domain.hospital import Hospital, HospitalFilters


class HospitalService:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]):
        self._uow_factory = uow_factory

    def create_hospital(self, command: CreateHospitalCommand) -> Hospital:
        self._validate_create_command(command)

        hospital = Hospital(
            name=command.name.strip(),
            address=command.address.strip(),
            phone=command.phone.strip(),
            creation_batch_id=command.creation_batch_id or uuid4(),
        )

        with self._uow_factory() as uow:
            created_hospital = uow.hospitals.add(hospital)
            uow.commit()
            return created_hospital

    def list_hospitals(self, filters: HospitalFilters | None = None) -> list[Hospital]:
        with self._uow_factory() as uow:
            return uow.hospitals.list(filters)

    def get_hospital(self, hospital_id: int) -> Hospital:
        with self._uow_factory() as uow:
            hospital = uow.hospitals.get_by_id(hospital_id)
            if hospital is None:
                raise HospitalNotFoundError(hospital_id)
            return hospital

    @staticmethod
    def _validate_create_command(command: CreateHospitalCommand) -> None:
        if not command.name.strip():
            raise InvalidHospitalDataError("Hospital name cannot be blank")
        if not command.address.strip():
            raise InvalidHospitalDataError("Hospital address cannot be blank")
        if not command.phone.strip():
            raise InvalidHospitalDataError("Hospital phone cannot be blank")
