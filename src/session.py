from message_decoder import MessageDecoder
from request_builder import RequestBuilder
from socket_connection import SocketConnection


class Session:
    def __init__(self, host: str, port: int):
        # self._open = True
        # self._chunk_decoder = ChunkDecoder(this._on_chunks_decoded)
        self._message_decoder = MessageDecoder()
        # self._response_handler = ResponseHandler()
        self._connection = SocketConnection(host, port)

    def run(self, query: str):  # -> Result:
        self._connection.sendall(RequestBuilder.run(query))

        response = []
        data = self._connection.recv()
        while data:
            response.append(data)
            data = self._connection.recv()
        # chunk_decoder.decode(xx)
        # message_decoder.decode(xx)
        # response_handler.handle(xx)

    def catalog(self):
        self._connection.sendall(RequestBuilder.catalog())
        while True:
            data = self._connection.recv()
            print(data)
            if not data:
                print("done")
                break

    def close(self):
        pass
        # if self._open:
        # self._open = False


session = Session("localhost", 1234)
query = "MATCH (?X) RETURN * LIMIT 5"
print(len(query))
session.run(query)
session.catalog()
