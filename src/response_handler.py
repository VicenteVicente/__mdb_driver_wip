from typing import Callable, Dict

import protocol
from millenniumdb_error import MillenniumDBError


class ResponseHandler:
    def __init__(self):
        self._current_observer: Dict[str, Callable] = None
        self._pending_observers: List[Dict[str, Callable]] = []

    def handle(self, message: Dict[str, object]) -> None:
        if not isinstance(message, dict):
            raise MillenniumDBError(
                "ResponseHandler Error: Response was expected to be an object, but got"
                f" {type(message)} instead."
            )

        if not "type" in message:
            raise MillenniumDBError(
                'ResponseHandler Error: Response object is missing "type" property'
            )

        if not isinstance(message["type"], int):
            raise MillenniumDBError(
                'ResponseHandler Error: "type" property is expected to be an integer,'
                f' but got {type(message["type"])} instead.'
            )

        if not "payload" in message:
            raise MillenniumDBError(
                'ResponseHandler Error: Response object is missing "payload" property'
            )

        match message["type"]:
            case protocol.ResponseType.SUCCESS.value:
                self._callback("on_success", message["payload"])
                self._next_observer()

            case protocol.ResponseType.ERROR.value:
                self._callback("on_error", MillenniumDBError(message["payload"]))
                self._next_observer()

            case protocol.ResponseType.RECORD.value:
                self._callback("on_record", message["payload"])

            case protocol.ResponseType.VARIABLES.value:
                variables = message["payload"]["variables"]
                query_preamble = message["payload"]["queryPreamble"]
                self._callback("on_variables", variables, query_preamble)
                self._next_observer()

            case _:
                raise MillenniumDBError(
                    "ResponseHandler Error: Unknown ResponseType with code:"
                    f" 0x{message['type']:02x}"
                )

    def add_observer(self, observer: Dict[str, Callable]) -> None:
        if self._current_observer is None:
            self._current_observer = observer
        else:
            self._pending_observers.append(observer)

    def _callback(self, callback_key: str, *args, **kwargs) -> None:
        if (
            self._current_observer is not None
            and callback_key in self._current_observer
        ):
            self._current_observer[callback_key](*args, **kwargs)

    def _next_observer(self):
        if len(self._pending_observers) > 0:
            self._current_observer = self._pending_observers.pop(0)
        else:
            self._current_observer = None
