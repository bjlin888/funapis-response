"""API-related exceptions implementation."""

import traceback
from typing import Optional, Dict, Any

from funapis_response.error_codes.common import CommonErrorCodes
from funapis_response.exceptions.base import FunAPIException


class ValidationError(FunAPIException):
    """參數驗證錯誤"""
    
    def __init__(
        self,
        reason: str,
        data: Optional[Any] = None,
        include_trace: bool = False
    ):
        stack_trace = traceback.format_exc() if include_trace else None
        super().__init__(
            error_code=CommonErrorCodes.VALIDATION_ERROR,
            message_params={"reason": reason},
            data=data,
            stack_trace=stack_trace
        )
        
class EntityNotFoundError(FunAPIException):
    """參數驗證錯誤"""
    
    def __init__(
        self,
        identifier: str,
        entity_name: str,
        data: Optional[Any] = None,
        include_trace: bool = False
    ):
        stack_trace = traceback.format_exc() if include_trace else None
        super().__init__(
            error_code=CommonErrorCodes.ENTITY_NOT_FOUND_ERROR,
            message_params={"entity_name": {entity_name}, "identifier": identifier},
            data=data,
            stack_trace=stack_trace
        )        


class APIError(FunAPIException):
    """API 調用錯誤"""
    
    def __init__(
        self,
        message: str,
        data: Optional[Any] = None,
        include_trace: bool = True
    ):
        stack_trace = traceback.format_exc() if include_trace else None
        super().__init__(
            error_code=CommonErrorCodes.API_ERROR,
            message_params={"message": message},
            data=data,
            stack_trace=stack_trace
        )


class NetworkError(FunAPIException):
    """網路連接錯誤"""
    
    def __init__(
        self,
        message: str,
        data: Optional[Any] = None,
        include_trace: bool = True
    ):
        stack_trace = traceback.format_exc() if include_trace else None
        super().__init__(
            error_code=CommonErrorCodes.NETWORK_ERROR,
            message_params={"message": message},
            data=data,
            stack_trace=stack_trace
        )


class IllegalOperationError(FunAPIException):
    """非法操作錯誤"""
    
    def __init__(
        self,
        reason: str,
        data: Optional[Any] = None,
        include_trace: bool = False
    ):
        stack_trace = traceback.format_exc() if include_trace else None
        super().__init__(
            error_code=CommonErrorCodes.ILLEGAL_OPERATION,
            message_params={"reason": reason},
            data=data,
            stack_trace=stack_trace
        )


class UnknownError(FunAPIException):
    """未知錯誤"""
    
    def __init__(
        self,
        message: Optional[str] = None,
        data: Optional[Any] = None,
        include_trace: bool = True
    ):
        message = message or "發生未預期的錯誤"
        stack_trace = traceback.format_exc() if include_trace else None
        super().__init__(
            error_code=CommonErrorCodes.UNKNOWN_ERROR,
            message_params={"message": message},
            data=data,
            stack_trace=stack_trace
        )
