"""Error code registry implementation."""

from typing import Dict, Optional, List

from funapis_response.error_codes.base import ErrorCode


class ErrorCodeRegistry:
    """
    錯誤碼註冊表，提供更高級的查詢功能
    
    這個類提供對由 ErrorCode._registry 支援的錯誤碼註冊表的高級查詢，
    如果將來需要擴展錯誤碼註冊表的功能，可以在此處實現。
    """
    
    @staticmethod
    def get_by_code(code: str) -> Optional[ErrorCode]:
        """
        根據錯誤碼獲取錯誤碼實例
        
        Args:
            code: 錯誤碼字符串
            
        Returns:
            ErrorCode 實例，如果不存在則返回 None
        """
        return ErrorCode.get_by_code(code)
    
    @staticmethod
    def get_all_codes() -> List[ErrorCode]:
        """
        獲取所有註冊的錯誤碼
        
        Returns:
            ErrorCode 實例列表
        """
        return list(ErrorCode._registry.values())
    
    @staticmethod
    def get_registry() -> Dict[str, ErrorCode]:
        """
        獲取整個錯誤碼註冊表
        
        Returns:
            錯誤碼註冊表的副本
        """
        return ErrorCode._registry.copy()
