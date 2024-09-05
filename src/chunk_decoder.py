from enum import Enum

from iobuffer import IOBuffer
from millenniumdb_error import MillenniumDBError


class ChunkDecoder:
    _SEAL = 0x00_00

    class State(Enum):
        READING_HEADER_FIRST_BYTE = 1
        READING_HEADER_SECOND_BYTE = 2
        READING_BODY = 3

    def __init__(self, on_decode) -> None:
        self._on_decode = on_decode
        self._current_state = ChunkDecoder.State.READING_HEADER_FIRST_BYTE
        self._current_chunk_remaining = 0
        self._current_decoded_slices = []

    def decode(self, iobuffer: IOBuffer):
        while iobuffer.has_remaining():
            match self._current_state:
                case ChunkDecoder.State.READING_HEADER_FIRST_BYTE:
                    self._handle_header_first_byte(iobuffer)
                    break
                case ChunkDecoder.State.READING_HEADER_SECOND_BYTE:
                    self._handle_header_second_byte(iobuffer)
                    break
                case ChunkDecoder.State.READING_BODY:
                    self._handle_body(iobuffer)
                    break
                case _:
                    raise MillenniumDBError(
                        "ChunkDecoder Error: Invalid state with code"
                        f" 0x{int(self._current_state.value)}"
                    )

    def _handle_header_first_byte(self, iobuffer: IOBuffer):
        if iobuffer.remaining() > 1:
            self._current_chunk_remaining = iobuffer.read_uint16()
            self._handle_decoded_header()
        else:
            self._current_chunk_remaining = 0
            self._current_chunk_remaining |= iobuffer.read_uint8() << 8
            self._current_state = ChunkDecoder.State.READING_HEADER_SECOND_BYTE

    def _handle_header_second_byte(self, iobuffer: IOBuffer):
        self._current_chunk_remaining |= iobuffer.read_uint8()
        self._handle_decoded_header()

    def _join_decoded_body(self):
        if len(self._current_decoded_slices) == 1:
            return self._current_decoded_slices[0]
        pass  # TODO: Implement this

    def _handle_decoded_header(self):
        if self._current_chunk_remaining == ChunkDecoder._SEAL:
            body = self._join_decoded_body()
            self._current_decoded_slices = []
            self._current_state = ChunkDecoder.State.READING_HEADER_FIRST_BYTE
            self._on_decode(body)
        else:
            self._current_state = ChunkDecoder.State.READING_BODY

    def _handle_body(self, iobuffer: IOBuffer):
        remaining = iobuffer.remaining()
        if self._current_chunk_remaining > remaining:
            self._current_decoded_slices.append(iobuffer.read_slice(remaining))
            self._current_chunk_remaining -= remaining
        else:
            self._current_decoded_slices.append(
                iobuffer.read_slice(self._current_chunk_remaining)
            )
            self._current_state = ChunkDecoder.State.READING_HEADER_FIRST_BYTE
