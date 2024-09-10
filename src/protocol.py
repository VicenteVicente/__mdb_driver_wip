from enum import Enum, auto

DRIVER_PREAMBLE_BYTES = b"MDB_DRVR"
SERVER_PREAMBLE_BYTES = b"MDB_SRVR"

DEFAULT_SOCKET_TIMEOUT = 10.0


class ModelId(Enum):
    QUAD_MODEL_ID = 0
    RDF_MODEL_ID = auto()

    TOTAL = auto()


class DataType(Enum):
    NULL = 0
    BOOL_FALSE = auto()
    BOOL_TRUE = auto()
    UINT8 = auto()
    UINT16 = auto()
    UINT32 = auto()
    UINT64 = auto()
    INT64 = auto()
    FLOAT = auto()
    DOUBLE = auto()
    DECIMAL = auto()
    STRING = auto()
    STRING_LANG = auto()
    STRING_DATATYPE = auto()
    IRI = auto()
    NAMED_NODE = auto()
    EDGE = auto()
    ANON = auto()
    DATE = auto()
    TIME = auto()
    DATETIME = auto()
    PATH = auto()
    LIST = auto()
    MAP = auto()

    TOTAL = auto()


class RequestType(Enum):
    QUERY = 0
    CATALOG = auto()
    CANCEL = auto()
    UPDATE = auto()
    AUTH = auto()

    TOTAL = auto()


class ResponseType(Enum):
    SUCCESS = 0
    ERROR = auto()
    RECORD = auto()
    VARIABLES = auto()

    TOTAL = auto()
