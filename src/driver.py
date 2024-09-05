import urllib

from session import Session


class Driver:
    def __init__(self, url: str):
        parsed_url = urllib.parse(url)
        self._open = True
        self._host = parsed_url.hostname
        self._port = parsed_url.port
        self._sessions = []

    def catalog(self):
        pass

    def cancel(self):
        pass

    def session(self) -> Session:
        self._ensure_open()
        session = Session(self._host, self._port)
        self._sessions.append(session)
        return session

    def close():
        if self._open:
            self._open = False
            for session in self._sessions:
                session.close()

    def _ensure_open(self) -> None:
        if not self._open:
            raise Exception("Driver Error: driver is closed")
