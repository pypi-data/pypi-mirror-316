from dataclasses import dataclass


@dataclass
class Error(Exception):
    message: str
    code: str


class ErrorGroup(ExceptionGroup): ...
