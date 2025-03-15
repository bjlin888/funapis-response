"""Tests for ResponsePayloadBuilder extensions."""

import unittest

from funapis_response.core.builder import ResponsePayloadBuilder
from funapis_response.error_codes import CommonErrorCodes
from funapis_response.exceptions import ValidationError


class TestBuilderExtensions(unittest.TestCase):
    """Test builder extensions implementation."""
    
    def test_with_error(self):
        """Test with_error method."""
        reason = "必需參數缺失"
        
        response = ResponsePayloadBuilder()\
            .with_error(CommonErrorCodes.VALIDATION_ERROR, reason=reason)\
            .build()
        
        self.assertEqual(response.error_code, CommonErrorCodes.VALIDATION_ERROR.code)
        self.assertEqual(response.error_desc, f"參數驗證失敗: {reason}")
    
    def test_from_exception(self):
        """Test from_exception method."""
        reason = "必需參數缺失"
        data = {"field": "username"}
        exception = ValidationError(reason=reason, data=data, include_trace=True)
        
        response = ResponsePayloadBuilder.from_exception(exception).build()
        
        self.assertEqual(response.error_code, CommonErrorCodes.VALIDATION_ERROR.code)
        self.assertEqual(response.error_desc, f"參數驗證失敗: {reason}")
        self.assertEqual(response.data, data)
        self.assertIsNotNone(response._stack_trace)
    
    def test_success_builder(self):
        """Test success method."""
        data = {"id": 1, "name": "Test"}
        response = ResponsePayloadBuilder.success(data).build()
        
        self.assertEqual(response.error_code, CommonErrorCodes.SUCCESS.code)
        self.assertEqual(response.error_desc, "操作成功")
        self.assertEqual(response.data, data)
    
    def test_success_builder_without_data(self):
        """Test success method without data."""
        response = ResponsePayloadBuilder.success().build()
        
        self.assertEqual(response.error_code, CommonErrorCodes.SUCCESS.code)
        self.assertEqual(response.error_desc, "操作成功")
        self.assertIsNone(response.data)


if __name__ == "__main__":
    unittest.main()
