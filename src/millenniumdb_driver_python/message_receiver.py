from .chunk_decoder import ChunkDecoder
from .iobuffer import IOBuffer
from .message_decoder import MessageDecoder
from .socket_connection import SocketConnection


class MessageReceiver:
    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection):
        self._buffer = bytearray(1024)
        self._iobuffer = IOBuffer(self._buffer)
        self._chunk_decoder = ChunkDecoder(connection, self._iobuffer)
        self._message_decoder = MessageDecoder(self._iobuffer)

    def receive(self) -> object:
        self._iobuffer.reset()

        # Decode chunks
        self._chunk_decoder.decode()

        # Decode message
        return self._message_decoder.decode()
