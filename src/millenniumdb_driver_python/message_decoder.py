from decimal import Decimal
from typing import Dict, List

from . import protocol
from .graph_objects import (
    IRI,
    DateTime,
    GraphAnon,
    GraphEdge,
    GraphNode,
    GraphPath,
    GraphPathSegment,
    SimpleDate,
    StringDatatype,
    StringLang,
    Time,
)
from .iobuffer import IOBuffer
from .millenniumdb_error import MillenniumDBError


# Represents the decoder of the incoming messages
class MessageDecoder:
    def __init__(self, iobuffer: IOBuffer):
        self._iobuffer = iobuffer  # The IOBuffer of the incoming data

    # Decode the incoming message
    def decode(self) -> object:
        type_ = self._iobuffer.read_uint8()

        match type_:

            case protocol.DataType.NULL.value:
                return None

            case protocol.DataType.BOOL_FALSE.value:
                return False

            case protocol.DataType.BOOL_TRUE.value:
                return True

            case protocol.DataType.UINT8.value:
                return self._iobuffer.read_uint8()

            case protocol.DataType.UINT32.value:
                return self._iobuffer.read_uint32()

            case protocol.DataType.UINT64.value:
                return self._iobuffer.read_uint64()

            case protocol.DataType.INT64.value:
                return self._iobuffer.read_int64()

            case protocol.DataType.FLOAT.value:
                return self._iobuffer.read_float()

            case protocol.DataType.DOUBLE.value:
                return self._iobuffer.read_double()

            case protocol.DataType.DECIMAL.value:
                decimal_string = self._decode_string()
                return Decimal(decimal_string)

            case protocol.DataType.STRING.value:
                return self._decode_string()

            case protocol.DataType.STRING_LANG.value:
                str_ = self._decode_string()
                lang = self._decode_string()
                return StringLang(str_, lang)

            case protocol.DataType.STRING_DATATYPE.value:
                str_ = self._decode_string()
                datatype = self._decode_string()
                return StringDatatype(str_, datatype)

            case protocol.DataType.IRI.value:
                iri = self._decode_string()
                return IRI(iri)

            case protocol.DataType.LIST.value:
                return self._decode_list()

            case protocol.DataType.MAP.value:
                return self._decode_map()

            case protocol.DataType.NAMED_NODE.value:
                node_id = self._decode_string()
                return GraphNode(node_id)

            case protocol.DataType.EDGE.value:
                edge_id = self._decode_string()
                return GraphEdge(edge_id)

            case protocol.DataType.ANON.value:
                anon_id = self._decode_string()
                return GraphAnon(anon_id)

            case protocol.DataType.DATE.value:
                year = self._iobuffer.read_int64()
                month = self._iobuffer.read_int64()
                day = self._iobuffer.read_int64()
                tz_minute_offset = self._iobuffer.read_int64()
                return SimpleDate(year, month, day, tz_minute_offset)

            case protocol.DataType.TIME.value:
                hour = self._iobuffer.read_int64()
                minute = self._iobuffer.read_int64()
                second = self._iobuffer.read_int64()
                tz_minute_offset = self._iobuffer.read_int64()
                return Time(hour, minute, second, tz_minute_offset)

            case protocol.DataType.DATETIME.value:
                year = self._iobuffer.read_int64()
                month = self._iobuffer.read_int64()
                day = self._iobuffer.read_int64()
                hour = self._iobuffer.read_int64()
                minute = self._iobuffer.read_int64()
                second = self._iobuffer.read_int64()
                tz_minute_offset = self._iobuffer.read_int64()
                return DateTime(
                    year, month, day, hour, minute, second, tz_minute_offset
                )

            case protocol.DataType.PATH.value:
                path_length = self._iobuffer.read_uint32()
                if path_length == 0:
                    node = self.decode()
                    return GraphPath(node, node, [])
                path_segments = []
                from_ = self.decode()
                start = from_
                for _ in range(path_length):
                    reverse = (
                        self._iobuffer.read_uint8() == protocol.DataType.BOOL_TRUE.value
                    )
                    type_ = self.decode()
                    to = self.decode()
                    path_segments.append(GraphPathSegment(from_, to, type_, reverse))
                    from_ = to
                end = from_
                return GraphPath(start, end, path_segments)

            case _:
                raise MillenniumDBError(
                    f"MessageDecoder Error: Unhandled DataType with code: 0x{type_:02x}"
                )

    def _decode_string(self) -> str:
        size = self._iobuffer.read_uint32()
        return self._iobuffer.read_string(size)

    def _decode_list(self) -> List:
        size = self._iobuffer.read_uint32()
        return [self.decode() for _ in range(size)]

    def _decode_map(self) -> Dict[str, object]:
        size = self._iobuffer.read_uint32()
        res = {}
        for _ in range(size):
            key_type = self._iobuffer.read_uint8()
            if key_type != protocol.DataType.STRING.value:
                raise MillenniumDBError(
                    "MessageDecoder Error: Map keys must be a string"
                )
            key = self._decode_string()
            value = self.decode()
            res[key] = value
        return res
