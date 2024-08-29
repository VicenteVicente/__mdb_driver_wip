from typing import List


class GraphNode:
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id


class GraphEdge:
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id


class GraphAnon:
    def __init__(self, id: str):
        self.id = id

    def __str__(self):
        return self.id


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


class GraphPathSegment:
    def __init__(self, from_: object, to: object, type: object, reverse: bool) -> None:
        self.from_ = from_
        self.to = to
        self.type = type
        self.reverse = reverse


class GraphPath:
    def __init__(
        self,
        start: object,
        end: object,
        segments: List[GraphPathSegment],
    ) -> None:
        self.start = start
        self.end = end
        self.segments = segments
        self.length = len(segments)


class IRI:
    def __init__(self, iri: str):
        self.iri = iri

    def __str__(self):
        return self.iri


class StringLang:
    def __init__(self, str: str, lang: str):
        self.str = str
        self.lang = lang

    def __str__(self):
        return f'"{self.str}"@{self.lang}'


class StringDataType:
    def __init__(self, str: str, datatype: str):
        self.str = str
        self.datatype = IRI(datatype)

    def __str__(self):
        return f'"{self.str}"^^<{str(self.datatype)}>'
