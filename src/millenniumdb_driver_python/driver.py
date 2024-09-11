from functools import wraps
from urllib.parse import urlparse

from .catalog import Catalog
from .millenniumdb_error import MillenniumDBError
from .result import Result
from .session import Session


def _ensure_driver_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._open:
            raise MillenniumDBError("Driver Error: driver is closed")
        return func(self, *args, **kwargs)

    return wrapper


class Driver:
    def __init__(self, url: str):
        parsed_url = urlparse(url)
        self._open = True
        self._host = parsed_url.hostname
        self._port = parsed_url.port
        self._sessions = []

    @_ensure_driver_open
    def catalog(self) -> Catalog:
        with self.session() as session:
            return session.catalog()

    @_ensure_driver_open
    def cancel(self, result: Result) -> None:
        with self.session() as session:
            session._cancel(result)

    @_ensure_driver_open
    def session(self) -> Session:
        session = Session(self._host, self._port, self)
        self._sessions.append(session)
        return session

    def close(self) -> None:
        if self._open:
            self._open = False
            for session in self._sessions:
                session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
