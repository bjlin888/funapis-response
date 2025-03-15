"""Error code base implementation."""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, ClassVar, Dict

from funapis_response.enums import ErrorSeverity


@dataclass(frozen=True)
class ErrorCode:
    """錯誤碼基礎類"""
    code: str
    severity: ErrorSeverity
    message_template: str
    
    # 類變量，用於保存所有錯誤碼實例的映射
    _registry: ClassVar[Dict[str, 'ErrorCode']] = {}
    
    def __post_init__(self):
        """驗證錯誤碼格式並註冊實例"""
        if not self._validate_code_format(self.code):
            raise ValueError(f"Invalid error code format: {self.code}. Must be in FUNxxyyzzz format.")
        
        # 註冊錯誤碼
        ErrorCode._registry[self.code] = self
    
    @staticmethod
    def _validate_code_format(code: str) -> bool:
        """驗證錯誤碼格式 (FUNxxyyzzz)"""
        pattern = r'^FUN\d{9}$'
        return bool(re.match(pattern, code))
    
    def get_message(self, **kwargs) -> str:
        """
        根據提供的參數獲取格式化錯誤訊息
        
        Args:
            **kwargs: 用於格式化消息模板的參數
            
        Returns:
            格式化後的錯誤訊息
        """
        try:
            return self.message_template.format(**kwargs)
        except KeyError as e:
            return f"{self.message_template} (缺少格式化參數: {e})"
        except Exception:
            return self.message_template
    
    @classmethod
    def get_by_code(cls, code: str) -> Optional['ErrorCode']:
        """
        根據錯誤碼獲取錯誤碼實例
        
        Args:
            code: 錯誤碼字符串
            
        Returns:
            ErrorCode 實例，如果不存在則返回 None
        """
        return cls._registry.get(code)
