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


class MessageDecoder:
    def __init__(self, iobuffer: IOBuffer):
        self._iobuffer = iobuffer

    def decode(self) -> object:
        type = self._iobuffer.read_uint8()

        match type:

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
                decimal_string = self._decode_string(self._iobuffer)
                return Decimal(decimal_string)

            case protocol.DataType.STRING.value:
                return self._decode_string(self._iobuffer)

            case protocol.DataType.STRING_LANG.value:
                str = self._decode_string(self._iobuffer)
                lang = self._decode_string(self._iobuffer)
                return StringLang(str, lang)

            case protocol.DataType.STRING_DATATYPE.value:
                str = self._decode_string(self._iobuffer)
                datatype = self._decode_string(self._iobuffer)
                return StringDatatype(str, datatype)

            case protocol.DataType.IRI.value:
                iri = self._decode_string(self._iobuffer)
                return IRI(iri)

            case protocol.DataType.LIST.value:
                return self._decode_list(self._iobuffer)

            case protocol.DataType.MAP.value:
                return self._decode_map(self._iobuffer)

            case protocol.DataType.NAMED_NODE.value:
                nodeId = self._decode_string(self._iobuffer)
                return GraphNode(nodeId)

            case protocol.DataType.EDGE.value:
                edgeId = self._decode_string(self._iobuffer)
                return GraphEdge(edgeId)

            case protocol.DataType.ANON.value:
                anonId = self._decode_string(self._iobuffer)
                return GraphAnon(anonId)

            case protocol.DataType.DATE.value:
                year = self.decode()
                month = self.decode()
                day = self.decode()
                tzMinuteOffset = self.decode()
                return SimpleDate(year, month, day, tzMinuteOffset)

            case protocol.DataType.TIME.value:
                hour = self.decode()
                minute = self.decode()
                second = self.decode()
                tzMinuteOffset = self.decode()
                return Time(hour, minute, second, tzMinuteOffset)

            case protocol.DataType.DATETIME.value:
                year = self.decode()
                month = self.decode()
                day = self.decode()
                hour = self.decode()
                minute = self.decode()
                second = self.decode()
                tzMinuteOffset = self.decode()
                return DateTime(year, month, day, hour, minute, second, tzMinuteOffset)

            case protocol.DataType.PATH.value:
                pathLength = self._iobuffer.read_uint32()
                if pathLength == 0:
                    node = self.decode()
                    return GraphPath(node, node, [])
                pathSegments = []
                from_ = self.decode()
                start = from_
                for _ in range(pathLength):
                    reverse = self.decode()
                    type = self.decode()
                    to = self.decode()
                    pathSegments.append(GraphPathSegment(from_, to, type, reverse))
                    from_ = to
                end = from_
                return GraphPath(start, end, pathSegments)

            case _:
                raise MillenniumDBError(
                    f"MessageDecoder Error: Unhandled DataType with code: 0x{type:02x}"
                )

    def _decode_string(self, iobuffer: IOBuffer) -> str:
        size = self._iobuffer.read_uint32()
        return self._iobuffer.read_string(size)

    def _decode_list(self, iobuffer: IOBuffer) -> List:
        size = self._iobuffer.read_uint32()
        return [self.decode() for _ in range(size)]

    def _decode_map(self, iobuffer: IOBuffer) -> Dict[str, object]:
        size = self._iobuffer.read_uint32()
        res = {}
        for _ in range(size):
            key_type = self._iobuffer.read_uint8()
            if key_type != protocol.DataType.STRING.value:
                raise MillenniumDBError(
                    "MessageDecoder Error: Map keys must be a string"
                )
            key = self._decode_string(self._iobuffer)
            value = self.decode()
            res[key] = value
        return res
