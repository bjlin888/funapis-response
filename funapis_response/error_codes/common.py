"""Common error codes implementation."""

from funapis_response.error_codes.base import ErrorCode
from funapis_response.enums import ErrorSeverity


class CommonErrorCodes:
    """通用錯誤碼定義"""
    
    # 成功
    SUCCESS = ErrorCode(
        code="FUN006600001",
        severity=ErrorSeverity.INFO,
        message_template="操作成功"
    )
    
    # Entity Not Error
    ENTITY_NOT_FOUND_ERROR = ErrorCode(
        code="FUN999800001",
        severity=ErrorSeverity.WARNING,
        message_template="找不到指定的資料列：{entity_id}"
    )    
    
    # 參數驗證錯誤
    VALIDATION_ERROR = ErrorCode(
        code="FUN999999993",
        severity=ErrorSeverity.WARNING,
        message_template="參數驗證失敗: {reason}"
    )
    
    # API 錯誤
    API_ERROR = ErrorCode(
        code="FUN999999994",
        severity=ErrorSeverity.ERROR,
        message_template="API 調用錯誤: {message}"
    )
    
    # 網路錯誤
    NETWORK_ERROR = ErrorCode(
        code="FUN999999995",
        severity=ErrorSeverity.ERROR,
        message_template="網路連接錯誤: {message}"
    )
    
    # 非法操作
    ILLEGAL_OPERATION = ErrorCode(
        code="FUN999900001",
        severity=ErrorSeverity.ERROR,
        message_template="非法操作: {reason}"
    )
    
    # 未知錯誤
    UNKNOWN_ERROR = ErrorCode(
        code="FUN999999999",
        severity=ErrorSeverity.FATAL,
        message_template="未知錯誤: {message}"
    )
