from .driver import Driver as _Driver

__version__ = "0.0.1"


def driver(url: str) -> _Driver:
    return _Driver(url)


__all__ = [
    "driver",
]
