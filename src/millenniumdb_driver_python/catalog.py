from . import protocol
from .message_receiver import MessageReceiver
from .millenniumdb_error import MillenniumDBError
from .request_builder import RequestBuilder
from .response_handler import ResponseHandler
from .socket_connection import SocketConnection


# This class represents the catalog of the MillenniumDB server
class Catalog:
    def __init__(
        self,
        connection: SocketConnection,
        message_receiver: MessageReceiver,
        response_handler: ResponseHandler,
    ):
        self._connection = connection  # The Socket connection
        self._message_receiver = message_receiver  # The Receiver of incoming messages
        self._response_handler = response_handler  # The Handler of the responses
        self._model_id = None  # The model ID of the server
        self._version = None  # The version of the server
        self._catalog()  # Get the model ID and version of the server

    @property
    # Get the model ID of the server
    def model_id(self) -> int:
        return self._model_id

    @property
    # Get the version of the server
    def version(self) -> int:
        return self._version

    # Set the model ID and version of the server
    def _catalog(self):
        def on_success(summary) -> None:
            self._model_id = summary["modelId"]
            self._version = summary["version"]

        def on_error(error) -> None:
            raise MillenniumDBError(error)

        # Add success and error observers to the response handler
        self._response_handler.add_observer(
            {"on_success": on_success, "on_error": on_error}
        )
        self._connection.sendall(RequestBuilder.catalog())

        # on_success
        message = self._message_receiver.receive()
        self._response_handler.handle(message)

    def _model_id_to_str(self, model_id: int) -> str:
        match model_id:
            case protocol.ModelId.QUAD_MODEL_ID.value:
                return "quad"

            case protocol.ModelId.RDF_MODEL_ID.value:
                return "rdf"

            case _:
                return "unknown"

    def __repr__(self) -> str:
        return f"Catalog<{self._model_id_to_str(self._model_id)}, v{self._version}>"
