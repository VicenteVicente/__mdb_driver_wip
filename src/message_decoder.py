import protocol
from decimal import Decimal
from iobuffer import IOBuffer

class MessageDecoder:
    def decode(self, iobuffer: IOBuffer) -> str:
        type = iobuffer.read_uint8()

        match type:

            case protocol.DataType.NULL.value:
                return None
            
            case protocol.DataType.BOOL_FALSE.value:
                return False
            
            case protocol.DataType.BOOL_TRUE.value:
                return True
            
            case protocol.DataType.UINT8.value:
                return iobuffer.read_uint8()
            
            case protocol.DataType.UINT32.value:
                return iobuffer.read_uint32()
            
            case protocol.DataType.UINT64.value:
                return iobuffer.read_uint64()
            
            case protocol.DataType.INT64.value:
                return iobuffer.read_int64()
            
            case protocol.DataType.FLOAT.value:
                return iobuffer.read_float()
            
            case protocol.DataType.DOUBLE.value:
                return iobuffer.read_double()
            
            case protocol.DataType.DECIMAL.value:
                decimal_string = self._decode_string(iobuffer)
                return Decimal(decimal_string)

    def _decode_string(self, iobuffer: IOBuffer) -> str:
        size = iobuffer.read_uint32()
        return iobuffer.read_string(size)
