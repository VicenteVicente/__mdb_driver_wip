from typing import List


class GraphNode:
    """
    Represents a node in the graph
    """

    def __init__(self, id: str):
        """
        attributes:
        id (str): The node identifier
        """
        self.id = id

    def __str__(self):
        return self.id

    def __repr__(self) -> str:
        return f"GraphNode<{str(self)}>"


class GraphEdge:
    """
    Represents an edge in the graph
    """

    def __init__(self, id: str):
        """
        attributes:
        id (str): The edge identifier
        """
        self.id = id

    def __str__(self):
        return self.id

    def __repr__(self) -> str:
        return f"GraphEdge<{str(self)}>"


class GraphAnon:
    """
    Represents an anonymous node in the graph
    """

    def __init__(self, id: str):
        """
        attributes:
        id (str): The anonymous node identifier
        """
        self.id = id

    def __str__(self):
        return self.id

    def __repr__(self) -> str:
        return f"GraphAnon<{str(self)}>"


class SimpleDate:
    def __init__(self, year: int, month: int, day: int, tzMinuteOffset: int):
        self.year = year
        self.month = month
        self.day = day
        self.tzMinuteOffset = tzMinuteOffset

    def __str__(self):
        year = str(self.year)
        month = str(self.month).zfill(2)
        day = str(self.day).zfill(2)
        res = f"{year}-{month}-{day}"
        if self.tzMinuteOffset == 0:
            res += "Z"
        else:
            tzHour = self.tzMinuteOffset // 60
            tzMin = self.tzMinuteOffset % 60
            res += "-" if self.tzMinuteOffset < 0 else "+"
            res += str(abs(tzHour)).zfill(2) + ":"
            res += str(abs(tzMin)).zfill(2)
        return res

    def __repr__(self) -> str:
        return f"SimpleDate<{str(self)}>"


class Time:
    def __init__(self, hour: int, minute: int, second: int, tzMinuteOffset: int):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tzMinuteOffset = tzMinuteOffset

    def __str__(self):
        hour = str(self.hour).zfill(2)
        minute = str(self.minute).zfill(2)
        second = str(self.second).zfill(2)
        res = f"{hour}:{minute}:{second}"
        if self.tzMinuteOffset == 0:
            res += "Z"
        else:
            tzHour = self.tzMinuteOffset // 60
            tzMin = self.tzMinuteOffset % 60
            res += "-" if self.tzMinuteOffset < 0 else "+"
            res += str(abs(tzHour)).zfill(2) + ":"
            res += str(abs(tzMin)).zfill(2)
        return res

    def __repr__(self) -> str:
        return f"Time<{str(self)}>"


class DateTime:
    def __init__(
        self,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        second: int,
        tzMinuteOffset: int,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.tzMinuteOffset = tzMinuteOffset

    def __str__(self) -> str:
        year = str(self.year)
        month = str(self.month).zfill(2)
        day = str(self.day).zfill(2)
        hour = str(self.hour).zfill(2)
        minute = str(self.minute).zfill(2)
        second = str(self.second).zfill(2)
        res = f"{year}-{month}-{day}T{hour}:{minute}:{second}"
        if self.tzMinuteOffset == 0:
            res += "Z"
        else:
            tzHour = self.tzMinuteOffset // 60
            tzMin = self.tzMinuteOffset % 60
            res += "-" if self.tzMinuteOffset < 0 else "+"
            res += str(abs(tzHour)).zfill(2) + ":"
            res += str(abs(tzMin)).zfill(2)
        return res

    def __repr__(self) -> str:
        return f"DateTime<{str(self)}>"


class GraphPathSegment:
    """
    Represents a segment in the path
    """

    def __init__(self, from_: object, to: object, type: object, reverse: bool) -> None:
        """
        attributes:
        from_ (object): The starting node of the segment
        to (object): The ending node of the segment
        type (object): The type of the segment
        """
        self.from_ = from_
        self.to = to
        self.type = type

        # Whether the segment is in reverse direction,
        # for example the segment should be printed
        # as `(to)<-[type]-(from)` instead of `(from)-[type]->(to)`
        self.reverse = reverse


class GraphPath:
    """
    Represents a path in the graph
    """

    def __init__(
        self,
        start: object,
        end: object,
        segments: List[GraphPathSegment],
    ) -> None:
        """
        attributes:
        start (object): The starting node of the path
        end (object): The ending node of the path
        segments (List[GraphPathSegment]): The segments of the path
        length (int): The number of segments in the path
        """
        self.start = start
        self.end = end
        self.segments = segments
        self.length = len(segments)

    def __repr__(self) -> str:
        return f"GraphPath<length={self.length}>"

    def __len__(self) -> int:
        return self.length


class IRI:
    def __init__(self, iri: str):
        self.iri = iri

    def __str__(self):
        return self.iri

    def __repr__(self):
        return f"IRI<{str(self)}>"


class StringLang:
    def __init__(self, str: str, lang: str):
        self.str = str
        self.lang = lang

    def __str__(self):
        return f'"{self.str}"@{self.lang}'

    def __repr__(self):
        return f"StringLang<{str(self)}>"


class StringDatatype:
    def __init__(self, str: str, datatype: str):
        self.str = str
        self.datatype = IRI(datatype)

    def __str__(self):
        return f'"{self.str}"^^<{str(self.datatype)}>'

    def __repr__(self):
        return f"StringDatatype<{str(self)}>"
