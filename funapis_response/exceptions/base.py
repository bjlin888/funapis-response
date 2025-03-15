"""Base exception classes for funapis-response."""

import traceback
from typing import Optional, Dict, Any

from funapis_response.core.payload import ResponsePayload
from funapis_response.core.builder import ResponsePayloadBuilder
from funapis_response.error_codes.base import ErrorCode
from funapis_response.enums import UserLevel


class FunAPIException(Exception):
    """與 funapis-response 整合的基礎例外類"""
    
    def __init__(
        self,
        error_code: ErrorCode,
        message_params: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        stack_trace: Optional[str] = None
    ):
        self.error_code = error_code
        self.message_params = message_params or {}
        self.data = data
        self.stack_trace = stack_trace
        
        # 生成錯誤訊息
        self.message = error_code.get_message(**self.message_params)
        super().__init__(self.message)
    
    def to_response_payload(self) -> ResponsePayload:
        """
        將例外轉換為響應載荷
        
        Returns:
            ResponsePayload 實例
        """
        builder = ResponsePayloadBuilder()
        builder.with_error_code(self.error_code.code)
        builder.with_error_desc(self.message)
        
        if self.data:
            builder.with_data(self.data)
        
        if self.stack_trace:
            builder.with_stack_trace(self.stack_trace)
        
        return builder.build()
    
    @staticmethod
    def get_current_stack_trace() -> str:
        """
        獲取當前堆疊追蹤
        
        Returns:
            堆疊追蹤字符串
        """
        return traceback.format_exc()
