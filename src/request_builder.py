from iobuffer import IOBuffer
from protocol import Protocol


class RequestBuilder:
    @staticmethod
    def encode_string(string: str) -> bytearray:
        return bytearray(string, "utf-8")

    @staticmethod
    def run(query: str) -> IOBuffer:
        queryBytes = RequestBuilder.encode_string(query)
        queryBytesLength = len(queryBytes)
        buffer = bytearray(6 + queryBytesLength)
        iobuffer = IOBuffer(buffer)
        iobuffer.write_uint8(Protocol.RequestType.RUN)
        iobuffer.write_uint8(Protocol.DataTypes.STRING)
        iobuffer.write_uint32(queryBytesLength)
        iobuffer.write_bytes(queryBytes)
        iobuffer.reset()
        return iobuffer

    @staticmethod
    def catalog() -> IOBuffer:
        buffer = bytearray(1)
        iobuffer = IOBuffer(buffer)
        iobuffer.write_uint8(Protocol.RequestType.CATALOG)
        iobuffer.reset()
        return iobuffer

    @staticmethod
    def cancel(worker_index: int, cancellation_token: str) -> IOBuffer:
        cancellation_token_bytes = RequestBuilder.encode_string(cancellation_token)
        cancellation_token_bytes_length = len(cancellation_token_bytes)
        buffer = bytearray(6 + cancellation_token_bytes_length)
        iobuffer = IOBuffer(buffer)
        iobuffer.write_uint8(Protocol.RequestType.CANCEL)
        iobuffer.write_uint8(Protocol.DataTypes.UINT8)
        iobuffer.write_uint32(worker_index)
        iobuffer.write_uint8(Protocol.DataTypes.STRING)
        iobuffer.write_uint32(cancellation_token_bytes_length)
        iobuffer.write_bytes(cancellation_token_bytes)
        iobuffer.reset()
        return iobuffer
