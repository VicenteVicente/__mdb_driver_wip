from functools import wraps
from urllib.parse import urlparse

from .catalog import Catalog
from .millenniumdb_error import MillenniumDBError
from .result import Result
from .session import Session


# Ensure that the driver is open before executing a function
def _ensure_driver_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._open:
            raise MillenniumDBError("Driver Error: driver is closed")
        return func(self, *args, **kwargs)

    return wrapper


# A driver that manages sessions and connections sending
# queries and receiving results from the MillenniumDB server
class Driver:
    def __init__(self, url: str):
        parsed_url = urlparse(url)
        self._open = True
        self._host = parsed_url.hostname
        self._port = parsed_url.port
        self._sessions = []

    @_ensure_driver_open
    # Get the catalog of the MillenniumDB server
    def catalog(self) -> Catalog:
        with self.session() as session:
            return session.catalog()

    @_ensure_driver_open
    # Cancel a running query on the server
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
