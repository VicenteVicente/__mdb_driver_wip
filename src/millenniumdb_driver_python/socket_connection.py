import socket
from typing import Any, Callable, Union

from . import protocol
from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError


class SocketConnection:
    def __init__(
        self,
        host: str,
        port: int,
    ):
        self._timeout = protocol.DEFAULT_SOCKET_TIMEOUT
        self._socket = self._create_socket(host, port)
        self._handshake()

    def sendall(self, iobuffer: IOBuffer) -> None:
        return self._wait_operation(self._socket.sendall, iobuffer.buffer)

    def recvall(self, num_bytes: int) -> bytearray:
        buffer = bytearray(num_bytes)
        self.recvall_into(buffer, num_bytes)
        return buffer

    def recvall_into(
        self, buffer: Union[bytes, bytearray, memoryview], num_bytes: int
    ) -> None:
        total_bytes_recv = 0
        with memoryview(buffer) as view:
            while total_bytes_recv < num_bytes:
                num_bytes_recv = self._wait_operation(
                    self._socket.recv_into,
                    view[total_bytes_recv:num_bytes],
                    num_bytes - total_bytes_recv,
                )

                if num_bytes_recv == 0:
                    raise MillenniumDBError("SocketConnection Error: no data received")

                total_bytes_recv += num_bytes_recv

    def close(self) -> None:
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        try:
            self._socket.close()
        except OSError:
            pass

    def _handshake(self) -> None:
        self._wait_operation(self._socket.sendall, protocol.DRIVER_PREAMBLE_BYTES)
        response = self._wait_operation(self._socket.recv, 8)
        if response != protocol.SERVER_PREAMBLE_BYTES:
            raise MillenniumDBError("SocketConnection Error: handshake failed")

    def _wait_operation(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        try:
            self._socket.settimeout(self._timeout)
            return func(*args, **kwargs)
        except socket.timeout as e:
            raise MillenniumDBError("SocketConnection Error: socket timed out") from e
        except Exception as e:
            raise MillenniumDBError(
                "SocketConnection Error: socket operation failed"
            ) from e

    def _create_socket(self, host: str, port: int) -> socket.socket:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self._timeout)
            sock.connect((host, port))
            return sock
        except socket.timeout as e:
            raise MillenniumDBError(
                "SocketConnection Error: socket timed out while establishing connection"
            ) from e
        except Exception as e:
            raise MillenniumDBError(
                f"SocketConnection Error: could not connect to {host}:{port}"
            ) from e