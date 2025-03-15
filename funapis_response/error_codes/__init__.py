"""Error codes package."""

from funapis_response.error_codes.base import ErrorCode
from funapis_response.error_codes.common import CommonErrorCodes
from funapis_response.error_codes.registry import ErrorCodeRegistry

__all__ = ["ErrorCode", "CommonErrorCodes", "ErrorCodeRegistry"]
