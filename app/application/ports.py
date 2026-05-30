from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from app.domain.hospital import Hospital, HospitalFilters


class HospitalRepository(ABC):
    @abstractmethod
    def add(self, hospital: Hospital) -> Hospital:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, hospital_id: int) -> Hospital | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, filters: HospitalFilters) -> list[Hospital]:
        raise NotImplementedError


class UnitOfWork(ABC):
    @property
    @abstractmethod
    def hospitals(self) -> HospitalRepository:
        raise NotImplementedError

    @abstractmethod
    def __enter__(self) -> Self:
        raise NotImplementedError

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
