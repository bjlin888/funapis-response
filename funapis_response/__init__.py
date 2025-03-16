"""
funapis-response
~~~~~~~~~~~~~~~

A standardized API response payload library for FUN-prefixed error codes.

:copyright: (c) 2024 by FunRaise.
:license: MIT, see LICENSE for more details.
"""

from funapis_response.core.payload import ResponsePayload, PagingPayload, OrderingPayload
from funapis_response.core.validator import PayloadValidator
from funapis_response.core.builder import (
    ResponsePayloadBuilder,
    PagingPayloadBuilder,
    OrderingPayloadBuilder,
)
from funapis_response.enums.types import ErrorSeverity, SortDirection, UserLevel
from funapis_response.error_codes import ErrorCode, CommonErrorCodes, ErrorCodeRegistry
from funapis_response.exceptions import (
    FunAPIException,
    ValidationError,
    APIError,
    NetworkError,
    IllegalOperationError,
    UnknownError,
    EntityNotFoundError
)

__version__ = "0.1.0"
__all__ = [
    "ResponsePayload",
    "PagingPayload",
    "OrderingPayload",
    "ResponsePayloadBuilder",
    "PagingPayloadBuilder",
    "OrderingPayloadBuilder",
    "ErrorSeverity",
    "SortDirection",
    "UserLevel",
    "PayloadValidator",
    "ErrorCode",
    "CommonErrorCodes",
    "ErrorCodeRegistry",
    "FunAPIException",
    "ValidationError",
    "APIError",
    "NetworkError",
    "IllegalOperationError",
    "UnknownError",
    "EntityNotFoundError"
]
