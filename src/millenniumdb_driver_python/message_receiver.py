from .chunk_decoder import ChunkDecoder
from .iobuffer import IOBuffer
from .message_decoder import MessageDecoder
from .socket_connection import SocketConnection


class MessageReceiver:
    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection):
        self._receiver_buffer = IOBuffer()
        self._chunk_decoder = ChunkDecoder(connection, self._receiver_buffer)
        self._message_decoder = MessageDecoder(self._receiver_buffer)

    def receive(self) -> object:
        # Decode chunks
        self._chunk_decoder.decode()

        # Decode message
        res = self._message_decoder.decode()

        # Reset receiver buffer for the next message
        self._receiver_buffer.reset()

        return res
