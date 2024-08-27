from enum import Enum, auto

DEFAULT_FETCH_SIZE = 1024

class ModelId(Enum):
    QUAD_MODEL_ID = 0
    RDF_MODEL_ID = auto()

    TOTAL = auto()

class DataType(Enum):
    NULL_ = 0
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

class ResponseType(Enum):
    SUCCESS = 0
    ERROR = auto()
    RECORD = auto()

    TOTAL = auto()
