import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from energyos.domain.health import DatabaseStatus

logger = logging.getLogger(__name__)


class SqlAlchemyDatabaseProbe:
    def __init__(self, session: Session) -> None:
        self._session = session

    def check(self) -> DatabaseStatus:
        try:
            self._session.execute(text("SELECT 1"))
            version = self._session.execute(text("SELECT postgis_version()")).scalar()
        except SQLAlchemyError:
            logger.warning("database health check failed", exc_info=True)
            self._session.rollback()
            return DatabaseStatus(database="unavailable", postgis="unavailable")
        if version is None or str(version).strip() == "":
            return DatabaseStatus(database="ok", postgis="unavailable")
        return DatabaseStatus(database="ok", postgis="ok")
