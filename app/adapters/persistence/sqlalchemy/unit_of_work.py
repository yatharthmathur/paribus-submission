from types import TracebackType

from app.adapters.persistence.sqlalchemy.repositories import SqlAlchemyHospitalRepository
from app.application.ports import HospitalRepository, UnitOfWork
from sqlalchemy.orm import Session, sessionmaker


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: sessionmaker[Session]):
        self._session_factory = session_factory
        self._session: Session | None = None
        self._hospitals: HospitalRepository | None = None

    @property
    def hospitals(self) -> HospitalRepository:
        if self._hospitals is None:
            raise RuntimeError("Unit of work has not been entered")
        return self._hospitals

    def __enter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_factory()
        self._hospitals = SqlAlchemyHospitalRepository(self._session)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc is not None:
            self.rollback()

        if self._session is not None:
            self._session.close()

        self._session = None
        self._hospitals = None

    def commit(self) -> None:
        if self._session is None:
            raise RuntimeError("Unit of work has not been entered")
        self._session.commit()

    def rollback(self) -> None:
        if self._session is None:
            return
        self._session.rollback()
