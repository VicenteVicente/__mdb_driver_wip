from typing import Callable, Dict, List

from . import protocol
from .millenniumdb_error import MillenniumDBError


# This class handles the responses coming from the server
class ResponseHandler:
    def __init__(self):
        self._current_observer: Dict[str, Callable] = None
        self._pending_observers: List[Dict[str, Callable]] = []

    # Handle an incoming response
    def handle(self, message: Dict[str, object]) -> None:
        match message["type"]:
            case protocol.ResponseType.SUCCESS:
                self._callback("on_success", message["payload"])
                self._next_observer()

            case protocol.ResponseType.ERROR:
                self._callback("on_error", MillenniumDBError(message["payload"]))
                self._next_observer()

            case protocol.ResponseType.VARIABLES:
                variables = message["payload"]["variables"]
                query_preamble = message["payload"]["queryPreamble"]
                self._callback("on_variables", variables, query_preamble)
                self._next_observer()

            case _:
                raise NotImplementedError

    # Enqueue a new observer for handling a response
    # @param observer that will handle the received data
    def add_observer(self, observer: Dict[str, Callable]) -> None:
        if self._current_observer is None:
            self._current_observer = observer
        else:
            self._pending_observers.append(observer)

    # Call the observer with the given key and arguments
    def _callback(self, callback_key: str, *args, **kwargs) -> None:
        if (
            self._current_observer is not None
            and callback_key in self._current_observer
        ):
            self._current_observer[callback_key](*args, **kwargs)

    # Move to the next observer in the queue
    def _next_observer(self):
        if len(self._pending_observers) > 0:
            self._current_observer = self._pending_observers.pop(0)
        else:
            self._current_observer = None
