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
        try:
            # Get first chunk size
            self._connection.recvall_into(self._iobuffer, 2)
            chunk_size = self._iobuffer.pop_uint16()

            # Decode all the chunks until we reach the SEAL
            while chunk_size != ChunkDecoder.SEAL:
                # Receive current chunk and next chunk size in the same recv call
                self._connection.recvall_into(
                    self._iobuffer,
                    chunk_size + 2,
                )
                chunk_size = self._iobuffer.pop_uint16()

        except Exception as e:
            raise MillenniumDBError("ChunkDecoder Error: could not decode chunk") from e
