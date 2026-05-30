from app.adapters.persistence.sqlalchemy.models import HospitalRecord
from app.db.base import Base
from app.db.session import engine


def create_db_and_tables() -> None:
    _ = HospitalRecord
    Base.metadata.create_all(bind=engine)
