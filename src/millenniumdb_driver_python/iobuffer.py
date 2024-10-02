import struct


# The class IOBuffer can be used to read and write data to and from a binary buffer
class IOBuffer:
    DEFAULT_INITIAL_BUFFER_SIZE = 4096

    def __init__(self, initial_buffer_size: int = DEFAULT_INITIAL_BUFFER_SIZE):
        # Data itself. Should not be manipulated appart from extend method
        self._buffer = bytearray(initial_buffer_size)
        self._current_read_position = 0
        # Data view, this is what will be sliced, written and read
        self.view = memoryview(self._buffer)
        self.num_used_bytes = 0

    def extend(self, num_bytes: int) -> None:
        self._buffer += bytearray(num_bytes)
        self.view = memoryview(self._buffer)

    def reset(self) -> None:
        self.num_used_bytes = 0
        self._current_read_position = 0

    def __len__(self):
        return len(self._buffer)

    def read_uint8(self) -> int:
        return self.view[self._update_current_read_position(1)]

    def read_uint32(self) -> int:
        return int.from_bytes(self.read_bytes(4), "big", signed=False)

    def read_uint64(self) -> int:
        return int.from_bytes(self.read_bytes(8), "big", signed=False)

    def read_int64(self) -> int:
        return int.from_bytes(self.read_bytes(8), "big", signed=True)

    def read_float(self) -> float:
        return struct.unpack(">f", self.read_bytes(4))[0]

    def read_double(self) -> float:
        return struct.unpack(">d", self.read_bytes(8))[0]

    def read_string(self, num_bytes: int) -> str:
        return str(self.read_bytes(num_bytes), "utf-8")

    def read_bytes(self, num_bytes: int) -> memoryview:
        return self.view[
            self._update_current_read_position(num_bytes) : self._current_read_position
        ]

    def write_uint8(self, value: int) -> None:
        self.view[self._update_num_used_bytes(1)] = value

    def write_uint32(self, value: int) -> None:
        self.view[self._update_num_used_bytes(4) : self.num_used_bytes] = (
            value.to_bytes(4, "big", signed=False)
        )

    def write_bytes(self, value: bytes) -> None:
        self.view[self._update_num_used_bytes(len(value)) : self.num_used_bytes] = value

    # Pop an uint16 from the end of the used buffer, removing its used bytes
    def pop_uint16(self) -> int:
        res = (
            self.view[self.num_used_bytes - 2] << 8 | self.view[self.num_used_bytes - 1]
        )
        self.num_used_bytes -= 2
        return res

    def _update_current_read_position(self, num_bytes: int) -> int:
        previous_read_position = self._current_read_position
        self._current_read_position += num_bytes
        return previous_read_position

    def _update_num_used_bytes(self, num_bytes: int) -> None:
        previous_used_bytes = self.num_used_bytes
        self.num_used_bytes += num_bytes
        return previous_used_bytes
