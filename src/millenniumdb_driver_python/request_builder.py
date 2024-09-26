from . import protocol
from .iobuffer import IOBuffer


class RequestBuilder:
    @staticmethod
    def encode_string(string: str) -> bytes:
        return string.encode("utf-8")

    @staticmethod
    def run(query: str) -> IOBuffer:
        query_bytes = RequestBuilder.encode_string(query)
        query_bytes_length = len(query_bytes)
        iobuffer = IOBuffer(10 + query_bytes_length)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.QUERY)
        iobuffer.write_uint8(protocol.DataType.STRING)
        iobuffer.write_uint32(query_bytes_length)
        iobuffer.write_bytes(query_bytes)
        return iobuffer

    @staticmethod
    def catalog() -> IOBuffer:
        iobuffer = IOBuffer(5)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.CATALOG)
        return iobuffer

    @staticmethod
    def cancel(worker_index: int, cancellation_token: str) -> IOBuffer:
        cancellation_token_bytes = RequestBuilder.encode_string(cancellation_token)
        cancellation_token_bytes_length = len(cancellation_token_bytes)
        iobuffer = IOBuffer(15 + cancellation_token_bytes_length)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.CANCEL)
        iobuffer.write_uint8(protocol.DataType.UINT32)
        iobuffer.write_uint32(worker_index)
        iobuffer.write_uint8(protocol.DataType.STRING)
        iobuffer.write_uint32(cancellation_token_bytes_length)
        iobuffer.write_bytes(cancellation_token_bytes)
        return iobuffer
