from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError
from .socket_connection import SocketConnection

# Decode the incoming chunks from the server


class ChunkDecoder:
    SEAL = 0x00_00

    def __init__(self, connection: SocketConnection, iobuffer: IOBuffer):
        self._connection = connection  # The Socket connection
        self._iobuffer = iobuffer  # The IOBuffer of the incoming data

    # Initialize the decoding loop until the SEAL is received
    def decode(self):
        current_pos = 0
        while True:
            try:
                # Determine the size of the next chunk
                chunk_size_bytes = self._connection.recvall(2)
                chunk_size = chunk_size_bytes[0] << 8 | chunk_size_bytes[1]

                # All chunks were received
                if chunk_size == ChunkDecoder.SEAL:
                    return

                # Calculate the remaining space in the buffer
                remaining = len(self._iobuffer) - current_pos
                if chunk_size > remaining:
                    # Extend the buffer if the chunk size is larger than the remaining space
                    self._iobuffer.buffer.extend(bytearray(chunk_size - remaining))

                with memoryview(self._iobuffer.buffer) as view:
                    # Fill the buffer with the chunk data
                    self._connection.recvall_into(
                        view[current_pos : current_pos + chunk_size],
                        chunk_size,
                    )
                current_pos += chunk_size
            except Exception as e:
                raise MillenniumDBError(
                    "ChunkDecoder Error: could not decode chunk"
                ) from e
