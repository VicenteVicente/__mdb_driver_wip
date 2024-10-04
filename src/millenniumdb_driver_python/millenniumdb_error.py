class MillenniumDBError(Exception):
    pass


class ResultError(MillenniumDBError):
    def __init__(self, result: "Result", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result: "Result" = result
