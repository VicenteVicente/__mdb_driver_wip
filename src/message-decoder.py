import protocol
import struct

def MessageDecoder(iobuffer: bytearray) -> str:
    type = iobuffer[0]

    match type:

        case protocol.DataType.NULL_.value:
            return 'null'
        
        case protocol.DataType.BOOL_FALSE.value:
            return 'false'
        
        case protocol.DataType.BOOL_TRUE.value:
            return 'true'
        
        case protocol.DataType.UINT8.value:
            return iobuffer[0]
        
        case protocol.DataType.UINT16.value:
            return 'uint16'
        
        case protocol.DataType.UINT32.value:
            return struct.unpack('<I', iobuffer[0:4])[0]
        
        case protocol.DataType.UINT64.value:
            return struct.unpack('<Q', iobuffer[0:8])[0]
        
        case protocol.DataType.INT64.value:
            return struct.unpack('<q', iobuffer[0:8])[0]
        
        case protocol.DataType.FLOAT.value:
            return struct.unpack('<f', iobuffer[0:4])[0]
        
        case protocol.DataType.DOUBLE.value:
            return struct.unpack('<d', iobuffer[0:8])[0]
        
        case protocol.DataType.DECIMAL.value:
            return
