"""Tests for the error codes implementation."""

import unittest

from funapis_response.error_codes import ErrorCode, CommonErrorCodes, ErrorCodeRegistry
from funapis_response.enums import ErrorSeverity


class TestErrorCodes(unittest.TestCase):
    """Test error codes implementation."""
    
    def test_error_code_validation(self):
        """Test error code format validation."""
        # Valid error code
        valid_code = "FUN123456789"
        self.assertTrue(ErrorCode._validate_code_format(valid_code))
        
        # Invalid error codes
        invalid_codes = ["FUN12345678", "ABC123456789", "FUN1234567890", "FUNabcdefghi"]
        for code in invalid_codes:
            self.assertFalse(ErrorCode._validate_code_format(code), f"Should reject {code}")
    
    def test_error_code_registry(self):
        """Test error code registry."""
        # The registry should contain CommonErrorCodes
        code = CommonErrorCodes.SUCCESS.code
        retrieved = ErrorCode.get_by_code(code)
        self.assertEqual(retrieved, CommonErrorCodes.SUCCESS)
        
        # Test via registry class
        reg_retrieved = ErrorCodeRegistry.get_by_code(code)
        self.assertEqual(reg_retrieved, CommonErrorCodes.SUCCESS)
        
        # Test get_all_codes method
        all_codes = ErrorCodeRegistry.get_all_codes()
        self.assertIn(CommonErrorCodes.SUCCESS, all_codes)
        self.assertIn(CommonErrorCodes.VALIDATION_ERROR, all_codes)
    
    def test_message_formatting(self):
        """Test message formatting with parameters."""
        validation_error = CommonErrorCodes.VALIDATION_ERROR
        reason = "字段不能為空"
        message = validation_error.get_message(reason=reason)
        self.assertEqual(message, f"參數驗證失敗: {reason}")
        
        # Missing parameters case
        message = validation_error.get_message()
        self.assertTrue("缺少格式化參數" in message)
    
    def test_error_code_creation(self):
        """Test creating a new error code."""
        # Create a new error code
        custom_code = ErrorCode(
            code="FUN987654321",
            severity=ErrorSeverity.WARNING,
            message_template="Custom error: {detail}"
        )
        
        # Verify it was registered
        retrieved = ErrorCode.get_by_code("FUN987654321")
        self.assertEqual(retrieved, custom_code)
        
        # Test message formatting
        message = custom_code.get_message(detail="Something went wrong")
        self.assertEqual(message, "Custom error: Something went wrong")
    
    def test_invalid_error_code_creation(self):
        """Test creating an error code with invalid format."""
        with self.assertRaises(ValueError):
            ErrorCode(
                code="INVALID",
                severity=ErrorSeverity.ERROR,
                message_template="Invalid code"
            )


if __name__ == "__main__":
    unittest.main()
