import struct
from typing import Union

from .millenniumdb_error import MillenniumDBError


class IOBuffer:
    def __init__(self, arg: Union[bytes, int]):
        if isinstance(arg, (bytes, bytearray)):
            self.buffer = arg
        elif isinstance(arg, int):
            self.buffer = bytearray(arg)
        else:
            raise MillenniumDBError(
                f"IOBuffer Error: Invalid argument with type {type(arg).__name__}"
            )

        self._current_position = 0

    def _update_current_position(self, num_bytes: int) -> int:
        if self._current_position + num_bytes > len(self):
            raise MillenniumDBError(
                "IOBuffer Error: Attempted to perform an operation past the end of the"
                " buffer"
            )

        previous_position = self._current_position
        self._current_position += num_bytes
        return previous_position

    def read_uint8(self) -> int:
        return self.buffer[self._update_current_position(1)]

    def read_uint16(self) -> int:
        return int.from_bytes(
            self.buffer[self._update_current_position(2) : self._current_position],
            "big",
        )

    def read_uint32(self) -> int:
        return int.from_bytes(
            self.buffer[self._update_current_position(4) : self._current_position],
            "big",
        )

    def read_uint64(self) -> int:
        return int.from_bytes(
            self.buffer[self._update_current_position(8) : self._current_position],
            "big",
        )

    def read_int64(self) -> int:
        return int.from_bytes(
            self.buffer[self._update_current_position(8) : self._current_position],
            "big",
            signed=True,
        )

    def read_float(self) -> float:
        return struct.unpack(
            ">f", self.buffer[self._update_current_position(4) : self._current_position]
        )[0]

    def read_double(self) -> float:
        return struct.unpack(
            ">d", self.buffer[self._update_current_position(8) : self._current_position]
        )[0]

    def read_string(self, num_bytes: int) -> str:
        with memoryview(self.buffer) as view:
            return str(
                view[self._update_current_position(num_bytes) : self._current_position],
                "utf-8",
            )

    def write_uint8(self, value: int) -> None:
        self.buffer[self._update_current_position(1)] = value

    def write_uint16(self, value: int) -> None:
        self.buffer[self._update_current_position(2) : self._current_position] = (
            value.to_bytes(2, "big")
        )

    def write_uint32(self, value: int) -> None:
        self.buffer[self._update_current_position(4) : self._current_position] = (
            value.to_bytes(4, "big")
        )

    def write_bytes(self, value: bytes) -> None:
        self.buffer[
            self._update_current_position(len(value)) : self._current_position
        ] = value

    def used(self) -> int:
        return self._current_position

    def remaining(self) -> int:
        return len(self) - self._current_position

    def has_remaining(self) -> bool:
        return self.remaining() > 0

    def reset(self) -> None:
        self._current_position = 0

    def __len__(self):
        return len(self.buffer)
