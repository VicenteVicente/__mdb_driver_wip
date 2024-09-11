from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError
from .socket_connection import SocketConnection


class ChunkDecoder:
    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection, iobuffer: IOBuffer):
        self._connection = connection
        self._iobuffer = iobuffer

    def decode(self):
        current_pos = 0
        while True:
            try:
                chunk_size_bytes = self._connection.recvall(2)
                chunk_size = chunk_size_bytes[0] << 8 | chunk_size_bytes[1]

                # All chunks were received
                if chunk_size == ChunkDecoder.SEAL:
                    return

                remaining = len(self._iobuffer) - current_pos
                if chunk_size > remaining:
                    self._iobuffer.buffer.extend(bytearray(chunk_size - remaining))

                with memoryview(self._iobuffer.buffer) as view:
                    self._connection.recvall_into(
                        view[current_pos : current_pos + chunk_size],
                        chunk_size,
                    )
                current_pos += chunk_size

            except Exception as e:
                raise MillenniumDBError(
                    "ChunkDecoder Error: could not decode chunk"
                ) from e
