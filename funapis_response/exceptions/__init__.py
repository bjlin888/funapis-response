"""Exceptions package."""

from funapis_response.exceptions.base import FunAPIException
from funapis_response.exceptions.api_exceptions import (
    ValidationError,
    APIError,
    NetworkError,
    IllegalOperationError,
    UnknownError,
    EntityNotFoundError
)

__all__ = [
    "FunAPIException",
    "ValidationError",
    "APIError",
    "NetworkError",
    "IllegalOperationError",
    "UnknownError",
    "EntityNotFoundError"
]
