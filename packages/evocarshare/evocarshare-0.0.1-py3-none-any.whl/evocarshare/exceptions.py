from typing import Any


class EvoApiCallError(Exception):
    def __init__(self, status: int, url: str, payload: Any):
        super().__init__(status, url, payload)
        self.status = status
        self.url = url

        self.payload = payload

    def __str__(self) -> str:
        return f"(status:{self.status} url:{self.url.__repr__()} payload:{self.payload.__repr__()})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self!s}"


class EvoProgramError(Exception):
    pass
