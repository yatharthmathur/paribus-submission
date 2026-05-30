from collections.abc import Callable
from uuid import uuid4

from app.application.commands import (
    ActivateHospitalsByBatchCommand,
    CreateHospitalCommand,
    DeleteHospitalCommand,
    DeleteHospitalsByBatchCommand,
    UpdateHospitalCommand,
)
from app.application.ports import PhoneNumberValidator, UnitOfWork
from app.domain.exceptions import (
    HospitalBatchNotFoundError,
    HospitalNotFoundError,
    InvalidHospitalDataError,
)
from app.domain.hospital import Hospital, HospitalFilters


class HospitalService:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        phone_number_validator: PhoneNumberValidator,
    ):
        self._uow_factory = uow_factory
        self._phone_number_validator = phone_number_validator

    def create_hospital(self, command: CreateHospitalCommand) -> Hospital:
        hospital = Hospital(
            name=self._validate_name(command.name),
            address=self._validate_address(command.address),
            phone=self._validate_phone(command.phone),
            creation_batch_id=command.creation_batch_id or uuid4(),
        )

        with self._uow_factory() as uow:
            created_hospital = uow.hospitals.add(hospital)
            uow.commit()
            return created_hospital

    def update_hospital(self, command: UpdateHospitalCommand) -> Hospital:
        with self._uow_factory() as uow:
            hospital = uow.hospitals.get_by_id(command.hospital_id)
            if hospital is None or not hospital.active:
                raise HospitalNotFoundError(command.hospital_id)

            hospital.name = self._validate_name(command.name)
            hospital.address = self._validate_address(command.address)
            hospital.phone = self._validate_phone(command.phone)

            updated_hospital = uow.hospitals.update(hospital)
            uow.commit()
            return updated_hospital

    def delete_hospital(self, command: DeleteHospitalCommand) -> None:
        with self._uow_factory() as uow:
            hospital = uow.hospitals.get_by_id(command.hospital_id)
            if hospital is None:
                raise HospitalNotFoundError(command.hospital_id)

            uow.hospitals.delete_by_id(command.hospital_id)
            uow.commit()

    def delete_hospitals_by_batch(self, command: DeleteHospitalsByBatchCommand) -> int:
        with self._uow_factory() as uow:
            deleted_count = uow.hospitals.delete_by_batch_id(command.batch_id)
            if deleted_count == 0:
                raise HospitalBatchNotFoundError(command.batch_id)

            uow.commit()
            return deleted_count

    def activate_hospitals_by_batch(self, command: ActivateHospitalsByBatchCommand) -> int:
        with self._uow_factory() as uow:
            activated_count = uow.hospitals.activate_by_batch_id(command.batch_id)
            if activated_count == 0:
                raise HospitalBatchNotFoundError(command.batch_id)

            uow.commit()
            return activated_count

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
    def _validate_name(name: str) -> str:
        normalized_name = name.strip()
        if not normalized_name:
            raise InvalidHospitalDataError("Hospital name cannot be blank")
        return normalized_name

    @staticmethod
    def _validate_address(address: str) -> str:
        normalized_address = address.strip()
        if not normalized_address:
            raise InvalidHospitalDataError("Hospital address cannot be blank")
        return normalized_address

    def _validate_phone(self, phone: str) -> str:
        normalized_phone = phone.strip()
        if not normalized_phone:
            raise InvalidHospitalDataError("Hospital phone cannot be blank")
        return self._phone_number_validator.normalize(normalized_phone)
