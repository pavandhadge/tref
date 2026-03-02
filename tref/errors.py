from __future__ import annotations


class TrefError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class ValidationError(TrefError):
    pass


class UpdateError(TrefError):
    pass


class FreshnessError(TrefError):
    pass


class DetectionError(TrefError):
    pass
