"""Tests for the exceptions implementation."""

import unittest

from funapis_response.exceptions import (
    FunAPIException,
    ValidationError,
    APIError,
    NetworkError,
    IllegalOperationError,
    UnknownError
)
from funapis_response.error_codes import CommonErrorCodes, ErrorCode
from funapis_response.enums import ErrorSeverity


class TestExceptions(unittest.TestCase):
    """Test exceptions implementation."""
    
    def test_base_exception(self):
        """Test FunAPIException base class."""
        # Create a custom error code for testing
        error_code = ErrorCode(
            code="FUN123456789",
            severity=ErrorSeverity.ERROR,
            message_template="測試錯誤: {param}"
        )
        
        # Create exception with parameters
        exception = FunAPIException(
            error_code=error_code,
            message_params={"param": "test value"},
            data={"test": "data"}
        )
        
        # Verify exception properties
        self.assertEqual(exception.error_code, error_code)
        self.assertEqual(exception.message, "測試錯誤: test value")
        self.assertEqual(exception.data, {"test": "data"})
        
        # Test converting to response payload
        response = exception.to_response_payload()
        self.assertEqual(response.error_code, "FUN123456789")
        self.assertEqual(response.error_desc, "測試錯誤: test value")
        self.assertEqual(response.data, {"test": "data"})
    
    def test_validation_error(self):
        """Test ValidationError exception."""
        reason = "使用者名稱不能為空"
        exception = ValidationError(reason=reason)
        
        self.assertEqual(exception.error_code, CommonErrorCodes.VALIDATION_ERROR)
        self.assertEqual(exception.message, f"參數驗證失敗: {reason}")
        
        # Verify stack trace handling when include_trace=True
        exception_with_trace = ValidationError(reason=reason, include_trace=True)
        self.assertIsNotNone(exception_with_trace.stack_trace)
    
    def test_api_error(self):
        """Test APIError exception."""
        message = "API 調用超時"
        data = {"endpoint": "/api/test"}
        exception = APIError(message=message, data=data)
        
        self.assertEqual(exception.error_code, CommonErrorCodes.API_ERROR)
        self.assertEqual(exception.message, f"API 調用錯誤: {message}")
        self.assertEqual(exception.data, data)
    
    def test_network_error(self):
        """Test NetworkError exception."""
        message = "連接超時"
        exception = NetworkError(message=message)
        
        self.assertEqual(exception.error_code, CommonErrorCodes.NETWORK_ERROR)
        self.assertEqual(exception.message, f"網路連接錯誤: {message}")
    
    def test_illegal_operation_error(self):
        """Test IllegalOperationError exception."""
        reason = "無權限執行此操作"
        exception = IllegalOperationError(reason=reason)
        
        self.assertEqual(exception.error_code, CommonErrorCodes.ILLEGAL_OPERATION)
        self.assertEqual(exception.message, f"非法操作: {reason}")
    
    def test_unknown_error(self):
        """Test UnknownError exception."""
        # Without custom message
        exception = UnknownError()
        self.assertEqual(exception.error_code, CommonErrorCodes.UNKNOWN_ERROR)
        self.assertEqual(exception.message, "未知錯誤: 發生未預期的錯誤")
        
        # With custom message
        message = "系統發生未知錯誤"
        exception = UnknownError(message=message)
        self.assertEqual(exception.message, f"未知錯誤: {message}")


if __name__ == "__main__":
    unittest.main()
