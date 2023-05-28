from typing import Any


class SkinportException(Exception):
    pass


class HTTPException(SkinportException):
    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self.data = data
        self.errors = data.get("errors", [])
        self.message = "\n ".join(self.errors)
        print(self.message)
