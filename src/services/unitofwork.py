from sqlalchemy.orm import Session  # type: ignore
from src.utils.setup import default_session_factory
from src.adapters.repository import (
    SQLScreenRepository,
    SQLStudyRepository,
    SQLScreenStudyRepository,
)


class SQLUnitOfWork:
    def __init__(self, session_factory=default_session_factory):
        self._session_factory = session_factory()

    def __enter__(self) -> "SQLUnitOfWork":
        self._session: Session = self._session_factory()
        self._screens = SQLScreenRepository(self._session)
        self._studies = SQLStudyRepository(self._session)
        self._screen_studies = SQLScreenStudyRepository(self._session)
        return self

    def __exit__(self, *args):
        self.rollback()
        self._session.close()

    @property
    def screens(self) -> SQLScreenRepository:
        return self._screens

    @property
    def studies(self) -> SQLStudyRepository:
        return self._studies

    @property
    def screen_studies(self) -> SQLScreenStudyRepository:
        return self._screen_studies

    def commit(self):
        self._commit()

    def _commit(self):
        self._session.commit()

    def rollback(self):
        self._session.rollback()
