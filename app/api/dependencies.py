from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork
from app.adapters.validation.phonenumbers import PhonenumbersPhoneNumberValidator
from app.application.ports import PhoneNumberValidator, UnitOfWork
from app.application.services import HospitalService
from app.db.session import get_session_factory


def get_phone_number_validator() -> PhoneNumberValidator:
    return PhonenumbersPhoneNumberValidator()


def get_hospital_service(
    session_factory: Annotated[sessionmaker[Session], Depends(get_session_factory)],
    phone_number_validator: Annotated[PhoneNumberValidator, Depends(get_phone_number_validator)],
) -> HospitalService:
    def uow_factory() -> UnitOfWork:
        return SqlAlchemyUnitOfWork(session_factory)

    factory: Callable[[], UnitOfWork] = uow_factory
    return HospitalService(factory, phone_number_validator)
