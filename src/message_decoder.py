import protocol
from millenniumdb_error import MillenniumDBError
from decimal import Decimal
from iobuffer import IOBuffer
from graph_objects import (
    DateTime,
    GraphAnon,
    GraphEdge,
    GraphNode,
    GraphPath,
    GraphPathSegment,
    IRI,
    SimpleDate,
    StringDatatype,
    StringLang,
    Time,
)


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

            case protocol.DataType.STRING.value:
                return self._decode_string(iobuffer)

            case protocol.DataType.STRING_LANG.value:
                str = self._decode_string(iobuffer)
                lang = self._decode_string(iobuffer)
                return StringLang(str, lang)

            case protocol.DataType.STRING_DATATYPE.value:
                str = self._decode_string(iobuffer)
                datatype = self._decode_string(iobuffer)
                return StringDatatype(str, datatype)

            case protocol.DataType.IRI.value:
                iri = self._decode_string(iobuffer)
                return IRI(iri)

            case protocol.DataType.LIST.value:
                return self._decode_list(iobuffer)

            case protocol.DataType.MAP.value:
                return self._decode_map(iobuffer)

            case protocol.DataType.NAMED_NODE.value:
                nodeId = self._decode_string(iobuffer)
                return GraphNode(nodeId)

            case protocol.DataType.EDGE.value:
                edgeId = self._decode_string(iobuffer)
                return GraphEdge(edgeId)

            case protocol.DataType.ANON.value:
                anonId = self._decode_string(iobuffer)
                return GraphAnon(anonId)

            case protocol.DataType.DATE.value:
                year = self.decode(iobuffer)
                month = self.decode(iobuffer)
                day = self.decode(iobuffer)
                tzMinuteOffset = self.decode(iobuffer)
                return SimpleDate(year, month, day, tzMinuteOffset)

            case protocol.DataType.TIME.value:
                hour = self.decode(iobuffer)
                minute = self.decode(iobuffer)
                second = self.decode(iobuffer)
                tzMinuteOffset = self.decode(iobuffer)
                return Time(hour, minute, second, tzMinuteOffset)

            case protocol.DataType.DATETIME.value:
                year = self.decode(iobuffer)
                month = self.decode(iobuffer)
                day = self.decode(iobuffer)
                hour = self.decode(iobuffer)
                minute = self.decode(iobuffer)
                second = self.decode(iobuffer)
                tzMinuteOffset = self.decode(iobuffer)
                return DateTime(year, month, day, hour, minute, second, tzMinuteOffset)

            case protocol.DataType.PATH.value:
                pathLength = iobuffer.read_uint32()
                if pathLength == 0:
                    node = self.decode(iobuffer)
                    return GraphPath(node, node, [])
                pathSegments = []
                from_ = self.decode(iobuffer)
                start = from_
                for _ in range(pathLength):
                    reverse = self.decode(iobuffer)
                    type = self.decode(iobuffer)
                    to = self.decode(iobuffer)
                    pathSegments.append(GraphPathSegment(from_, to, type, reverse))
                    from_ = to
                end = from_
                return GraphPath(start, end, pathSegments)

            case _:
                raise MillenniumDBError(
                    f"MessageDecoder Error: Unhandled DataType with code: 0x16"
                )

    def _decode_string(self, iobuffer: IOBuffer) -> str:
        size = iobuffer.read_uint32()
        return iobuffer.read_string(size)

    def _decode_list(self, iobuffer: IOBuffer) -> list:
        size = iobuffer.read_uint32()
        return [self.decode(iobuffer) for _ in range(size)]

    def _decode_map(self, iobuffer: IOBuffer) -> dict:
        size = iobuffer.read_uint32()
        res = {}
        for _ in range(size):
            key_type = iobuffer.read_uint8()
            if key_type != protocol.DataType.STRING.value:
                raise MillenniumDBError(
                    "MessageDecoder Error: Map keys must be a string"
                )
            key = self._decode_string(iobuffer)
            value = self.decode(iobuffer)
            res[key] = value
        return res
