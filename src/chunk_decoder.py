from iobuffer import IOBuffer
from millenniumdb_error import MillenniumDBError
from socket_connection import SocketConnection


class ChunkDecoder:
    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection, iobuffer: IOBuffer):
        self._connection = connection
        self._iobuffer = iobuffer

    def decode(self):
        while True:
            try:
                chunk_size_bytes = self._connection.recvall(2)
                chunk_size = chunk_size_bytes[0] << 8 | chunk_size_bytes[1]

                # All chunks were received
                if chunk_size == ChunkDecoder.SEAL:
                    return

                self._connection.recvall_into(self._iobuffer, chunk_size)

            except Exception as e:
                raise MillenniumDBError(
                    "ChunkDecoder Error: could not decode chunk"
                ) from e
