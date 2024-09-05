import protocol
from iobuffer import IOBuffer


class RequestBuilder:
    @staticmethod
    def encode_string(string: str) -> bytearray:
        return bytearray(string, "utf-8")

    @staticmethod
    def run(query: str) -> IOBuffer:
        queryBytes = RequestBuilder.encode_string(query)
        queryBytesLength = len(queryBytes)
        buffer = bytearray(10 + queryBytesLength)
        iobuffer = IOBuffer(buffer)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.RUN.value)
        iobuffer.write_uint8(protocol.DataType.STRING.value)
        iobuffer.write_uint32(queryBytesLength)
        iobuffer.write_bytes(queryBytes)
        iobuffer.reset()
        return iobuffer

    @staticmethod
    def catalog() -> IOBuffer:
        buffer = bytearray(5)
        iobuffer = IOBuffer(buffer)
        iobuffer.write_uint32(len(iobuffer) - 4)
        iobuffer.write_uint8(protocol.RequestType.CATALOG.value)
        iobuffer.reset()
        return iobuffer
