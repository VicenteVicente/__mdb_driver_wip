import struct


# Read/write buffer for internal usage. No errors raised because we assume correct usage
class IOBuffer:
    DEFAULT_INITIAL_BUFFER_SIZE = 4096

    def __init__(self, initial_buffer_size: int = DEFAULT_INITIAL_BUFFER_SIZE):
        self.buffer = bytearray(initial_buffer_size)
        self.used = 0
        self._current_read_position = 0

    def extend(self, num_bytes: int) -> None:
        self.buffer += bytearray(num_bytes)

    def reset(self) -> None:
        self.used = 0
        self._current_read_position = 0

    def __len__(self):
        return len(self.buffer)

    def read_uint8(self) -> int:
        return self.buffer[self._update_current_read_position(1)]

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
        return self.read_bytes(num_bytes).decode("utf-8")

    def read_bytes(self, num_bytes: int) -> bytearray:
        return self.buffer[
            self._update_current_read_position(num_bytes) : self._current_read_position
        ]

    def write_uint8(self, value: int) -> None:
        self.buffer[self._update_used(1)] = value

    def write_uint32(self, value: int) -> None:
        self.buffer[self._update_used(4) : self._current_read_position] = (
            value.to_bytes(4, "big", signed=False)
        )

    def write_bytes(self, value: bytes) -> None:
        self.buffer[self._update_used(len(value)) : self._current_read_position] = value

    # Pop an uint16 from the end of the used buffer, removing its used bytes
    def pop_uint16(self) -> int:
        res = self.buffer[self.used - 2] << 8 | self.buffer[self.used - 1]
        self.used -= 2
        return res

    def _update_current_read_position(self, num_bytes: int) -> int:
        previous_read_position = self._current_read_position
        self._current_read_position += num_bytes
        return previous_read_position

    def _update_used(self, num_bytes: int) -> None:
        previous_used = self.used
        self.used += num_bytes
        return previous_used
