from millenniumdb_error import MillenniumDBError
from typing import Dict, TypeVar

Value = TypeVar("Value")

RecordShape = Dict[str, Value]


class Record:
    def __init__(self, keys, values, keyToIndex):
        if len(keys) != len(values):
            raise MillenniumDBError(
                "Record Error: Number of variables does not match the number of values"
            )

        self._keys = keys
        self._values = values
        self._keyToIndex = keyToIndex
        self.length = len(keys)

    def entries(self):
        for _ in range(self.length):
            yield (self._keys[_], self._values[_])

    def values(self):
        for value in self._values:
            yield value

    def __iter__(self):
        yield from self.values()

    def get(self, key):
        index = self._keyToIndex.get(key)
        if key in self._keyToIndex:
            return self._values[self._keyToIndex[key]]
        else:
            return None
