from millenniumdb_error import MillenniumDBError
from typing import Dict, TypeVar

Value = TypeVar("Value")

RecordShape = Dict[str, Value]


class Record:
    def __init__(self, variables, values, variableToIndex):
        if len(variables) != len(values):
            raise MillenniumDBError(
                "Record Error: Number of variables does not match the number of values"
            )

        self._variables = variables
        self._values = values
        self._variableToIndex = variableToIndex
        self.length = len(variables)

    def entries(self):
        for _ in range(self.length):
            yield (self._variables[_], self._values[_])

    def values(self):
        for value in self._values:
            yield value

    def __iter__(self):
        yield from self.values()

    def get(self, key):
        index = key if isinstance(key, int) else self._variableToIndex.get(key, -1)
        if index < 0 or index > len(self._values) - 1:
            raise MillenniumDBError(f"Record Error: Index {index} is out of bounds")
        return self._values[index]

    def has(self, key) -> bool:
        index = key if isinstance(key, int) else self._variableToIndex.get(key, -1)
        return index >= 0 and index < len(self._values)

    def toObject(self):
        res = {}
        for _ in range(self.length):
            res[self._variables[_]] = self._values[_]
        return res
