from functools import wraps

from catalog import Catalog
from message_receiver import MessageReceiver
from millenniumdb_error import MillenniumDBError
from request_builder import RequestBuilder
from response_handler import ResponseHandler
from result import Result
from socket_connection import SocketConnection


def _ensure_session_open(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self._open:
            raise MillenniumDBError("Session Error: session is closed")
        return func(self, *args, **kwargs)

    return wrapper


class Session:

    def __init__(self, host: str, port: int):
        self._open = True
        self._connection = SocketConnection(host, port)
        self._message_receiver = MessageReceiver(self._connection)
        self._response_handler = ResponseHandler()

    @_ensure_session_open
    def run(self, query: str) -> Result:
        return Result(
            self._connection, self._message_receiver, self._response_handler, query
        )

    @_ensure_session_open
    def catalog(self):
        return Catalog(self._connection, self._message_receiver, self._response_handler)

    @_ensure_session_open
    def _cancel(self, result: Result) -> None:
        if result._query_preamble is None:
            raise MillenniumDBError("Session Error: query has not been executed yet")

        self._connection.sendall(
            RequestBuilder.cancel(
                result._query_preamble["workerIndex"],
                result._query_preamble["cancellationToken"],
            )
        )

    def close(self):
        if self._open:
            self._open = False
            self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()