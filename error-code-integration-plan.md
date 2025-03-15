# funapis-response 錯誤碼機制整合方案

## 概述
本文檔詳細說明如何將結構化的錯誤碼機制整合到現有的 funapis-response 專案中。方案將保持與現有 API 的兼容性，同時擴展功能以支持更強大的錯誤處理能力。

## 1. 專案結構分析

現有的 funapis-response 專案提供了標準化的 API 響應格式，主要組件包括：

- **ResponsePayload**: 不可變響應類，包含消息 ID、錯誤碼、錯誤描述等
- **ResponsePayloadBuilder**: 構建 ResponsePayload 的建造者模式實現
- **錯誤碼格式**: 使用 `FUNxxyyzzz` 格式的字符串表示錯誤

目前，錯誤碼僅作為字符串處理，缺乏結構化管理和分類功能。

## 2. 整合目標

1. 實現結構化的錯誤碼管理
2. 支持錯誤碼的分類和分層管理
3. 提供與例外處理機制的無縫集成
4. 保持與現有 API 的向後兼容性
5. 簡化開發人員使用體驗

## 3. 實現方案

### 3.1 新增檔案結構

```
funapis_response/
├── ...
├── error_codes/
│   ├── __init__.py
│   ├── base.py             # 錯誤碼基礎類
│   ├── common.py           # 通用錯誤碼
│   └── registry.py         # 錯誤碼註冊表
├── exceptions/
│   ├── __init__.py
│   ├── base.py             # 基礎例外類
│   └── api_exceptions.py   # API 相關例外
└── ...
```

### 3.2 錯誤碼基礎類設計

在 `error_codes/base.py` 中實現一個基礎的錯誤碼類，提供以下功能：

- 錯誤碼格式驗證
- 與嚴重程度 (ErrorSeverity) 的整合
- 錯誤描述的國際化支持
- 標準化的字串表示法

```python
# error_codes/base.py
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
```

### 3.3 通用錯誤碼實現

在 `error_codes/common.py` 中實現通用錯誤碼：

```python
# error_codes/common.py
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
```

### 3.4 例外機制整合

在 `exceptions/base.py` 中實現與錯誤碼整合的基礎例外類：

```python
# exceptions/base.py
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
```

在 `exceptions/api_exceptions.py` 中實現常用的 API 例外：

```python
# exceptions/api_exceptions.py
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
```

### 3.5 擴展 ResponsePayloadBuilder

擴展 `ResponsePayloadBuilder` 以支持直接從錯誤碼或例外創建響應：

```python
# core/builder.py 擴展
from typing import Optional, Any, Dict

from funapis_response.error_codes.base import ErrorCode
from funapis_response.error_codes.common import CommonErrorCodes
from funapis_response.exceptions.base import FunAPIException


class ResponsePayloadBuilder:
    # ... 保留現有方法 ...
    
    def with_error(self, error_code: ErrorCode, **message_params) -> 'ResponsePayloadBuilder':
        """
        使用錯誤碼和訊息參數設置錯誤信息
        
        Args:
            error_code: ErrorCode 實例
            **message_params: 用於格式化錯誤訊息的參數
            
        Returns:
            Self for method chaining
        """
        self._error_code = error_code.code
        self._error_desc = error_code.get_message(**message_params)
        return self
    
    @classmethod
    def from_exception(cls, exception: FunAPIException) -> 'ResponsePayloadBuilder':
        """
        從例外創建響應構建器
        
        Args:
            exception: FunAPIException 實例
            
        Returns:
            ResponsePayloadBuilder 實例
        """
        builder = cls()
        builder.with_error_code(exception.error_code.code)
        builder.with_error_desc(exception.message)
        
        if exception.data:
            builder.with_data(exception.data)
        
        if exception.stack_trace:
            builder.with_stack_trace(exception.stack_trace)
        
        return builder
    
    @classmethod
    def success(cls, data: Optional[Any] = None) -> 'ResponsePayloadBuilder':
        """
        創建成功響應構建器
        
        Args:
            data: 響應數據
            
        Returns:
            ResponsePayloadBuilder 實例
        """
        builder = cls()
        builder.with_error(CommonErrorCodes.SUCCESS)
        
        if data:
            builder.with_data(data)
        
        return builder
```

### 3.6 初始化和匯出

更新相關的 `__init__.py` 檔案以匯出新增的類和函數：

```python
# error_codes/__init__.py
from funapis_response.error_codes.base import ErrorCode
from funapis_response.error_codes.common import CommonErrorCodes

__all__ = ["ErrorCode", "CommonErrorCodes"]
```

```python
# exceptions/__init__.py
from funapis_response.exceptions.base import FunAPIException
from funapis_response.exceptions.api_exceptions import (
    ValidationError,
    APIError,
    IllegalOperationError,
    UnknownError
)

__all__ = [
    "FunAPIException",
    "ValidationError",
    "APIError",
    "IllegalOperationError",
    "UnknownError"
]
```

```python
# 更新主 __init__.py
# 在現有導入基礎上添加
from funapis_response.error_codes import ErrorCode, CommonErrorCodes
from funapis_response.exceptions import (
    FunAPIException,
    ValidationError,
    APIError,
    IllegalOperationError,
    UnknownError
)

# 添加到 __all__
__all__ += [
    "ErrorCode",
    "CommonErrorCodes",
    "FunAPIException",
    "ValidationError",
    "APIError",
    "IllegalOperationError",
    "UnknownError"
]
```

## 4. 測試計劃

為確保整合的正確性，需要添加以下測試案例：

1. 錯誤碼註冊和查詢測試
2. 錯誤碼格式驗證測試
3. 訊息格式化測試
4. 例外處理和轉換測試
5. 擴展 ResponsePayloadBuilder 功能測試

```python
# tests/test_error_codes.py
import unittest
from funapis_response.error_codes import ErrorCode, CommonErrorCodes
from funapis_response.enums import ErrorSeverity


class TestErrorCodes(unittest.TestCase):
    
    def test_error_code_validation(self):
        """測試錯誤碼格式驗證"""
        # 有效錯誤碼
        valid_code = "FUN123456789"
        self.assertTrue(ErrorCode._validate_code_format(valid_code))
        
        # 無效錯誤碼
        invalid_codes = ["FUN12345678", "ABC123456789", "FUN1234567890", "FUNabcdefghi"]
        for code in invalid_codes:
            self.assertFalse(ErrorCode._validate_code_format(code))
    
    def test_error_code_registry(self):
        """測試錯誤碼註冊表"""
        code = CommonErrorCodes.SUCCESS.code
        retrieved = ErrorCode.get_by_code(code)
        self.assertEqual(retrieved, CommonErrorCodes.SUCCESS)
    
    def test_message_formatting(self):
        """測試訊息格式化"""
        validation_error = CommonErrorCodes.VALIDATION_ERROR
        message = validation_error.get_message(reason="字段不能為空")
        self.assertEqual(message, "參數驗證失敗: 字段不能為空")
        
        # 缺少參數
        message = validation_error.get_message()
        self.assertTrue("缺少格式化參數" in message)
```

```python
# tests/test_exceptions.py
import unittest
from funapis_response.exceptions import ValidationError, APIError
from funapis_response.error_codes import CommonErrorCodes


class TestExceptions(unittest.TestCase):
    
    def test_validation_error(self):
        """測試驗證錯誤例外"""
        reason = "用戶名不能為空"
        error = ValidationError(reason=reason)
        
        self.assertEqual(error.error_code, CommonErrorCodes.VALIDATION_ERROR)
        self.assertEqual(error.message, f"參數驗證失敗: {reason}")
    
    def test_exception_to_response(self):
        """測試例外轉換為響應"""
        reason = "必需參數缺失"
        data = {"field": "username"}
        error = ValidationError(reason=reason, data=data)
        
        response = error.to_response_payload()
        self.assertEqual(response.error_code, CommonErrorCodes.VALIDATION_ERROR.code)
        self.assertEqual(response.error_desc, f"參數驗證失敗: {reason}")
        self.assertEqual(response.data, data)
```

```python
# tests/test_builder_extensions.py
import unittest
from funapis_response.core.builder import ResponsePayloadBuilder
from funapis_response.error_codes import CommonErrorCodes
from funapis_response.exceptions import ValidationError


class TestBuilderExtensions(unittest.TestCase):
    
    def test_with_error(self):
        """測試直接使用錯誤碼構建"""
        reason = "必需參數缺失"
        response = ResponsePayloadBuilder()\
            .with_error(CommonErrorCodes.VALIDATION_ERROR, reason=reason)\
            .build()
        
        self.assertEqual(response.error_code, CommonErrorCodes.VALIDATION_ERROR.code)
        self.assertEqual(response.error_desc, f"參數驗證失敗: {reason}")
    
    def test_from_exception(self):
        """測試從例外構建"""
        reason = "必需參數缺失"
        data = {"field": "username"}
        error = ValidationError(reason=reason, data=data)
        
        response = ResponsePayloadBuilder.from_exception(error).build()
        self.assertEqual(response.error_code, CommonErrorCodes.VALIDATION_ERROR.code)
        self.assertEqual(response.error_desc, f"參數驗證失敗: {reason}")
        self.assertEqual(response.data, data)
    
    def test_success_builder(self):
        """測試成功響應構建器"""
        data = {"id": 1, "name": "Test"}
        response = ResponsePayloadBuilder.success(data).build()
        
        self.assertEqual(response.error_code, CommonErrorCodes.SUCCESS.code)
        self.assertEqual(response.error_desc, "操作成功")
        self.assertEqual(response.data, data)
```

## 5. 使用範例

### 5.1 基本使用

```python
from funapis_response import (
    ResponsePayloadBuilder,
    CommonErrorCodes,
    ValidationError
)

# 使用錯誤碼構建成功響應
success_response = ResponsePayloadBuilder.success({"id": 1, "name": "Test"}).build()

# 使用錯誤碼構建錯誤響應
error_response = ResponsePayloadBuilder()\
    .with_error(CommonErrorCodes.VALIDATION_ERROR, reason="用戶名不能為空")\
    .build()

# 使用例外處理
try:
    # 業務邏輯...
    if not username:
        raise ValidationError(reason="用戶名不能為空")
except ValidationError as e:
    # 直接從例外創建響應
    error_response = e.to_response_payload()
```

### 5.2 與 Flask 整合

```python
from flask import Flask, jsonify
from funapis_response import (
    FunAPIException,
    ValidationError,
    APIError,
    UnknownError
)

app = Flask(__name__)

# 註冊例外處理器
@app.errorhandler(FunAPIException)
def handle_fun_api_exception(error):
    response = error.to_response_payload().to_dict()
    return jsonify(response), 400

@app.errorhandler(Exception)
def handle_general_exception(error):
    # 將未捕獲的例外轉換為 UnknownError
    fun_error = UnknownError(str(error))
    response = fun_error.to_response_payload().to_dict()
    return jsonify(response), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    
    # 驗證
    if not data or 'username' not in data:
        raise ValidationError(reason="用戶名是必需的")
    
    # 業務邏輯...
    
    # 成功響應
    return jsonify(ResponsePayloadBuilder.success({"id": 1, "username": data['username']}).build().to_dict())
```

## 6. 部署和發布計劃

1. 在開發分支上實現整個方案
2. 執行所有測試確保兼容性
3. 更新版本號 (建議使用語義化版本)
4. 更新文檔和使用說明
5. 合併到主分支並發布新版本

## 7. 兼容性和遷移指南

為確保現有代碼能順利遷移到新版本，建議使用以下方法：

1. 保留原有的字符串錯誤碼功能，同時引入新的錯誤碼類型
2. 對於常用錯誤碼，提供預定義的常量，降低遷移難度
3. 提供詳細的遷移文檔和使用示例

## 8. 結論

這個整合方案提供了一個系統化的錯誤處理機制，與 funapis-response 項目無縫集成。它既保持了向後兼容性，又擴展了錯誤處理能力，使開發人員能夠更加高效地管理和處理錯誤情況。通過結構化的錯誤碼和例外機制，應用程序可以提供更一致、更詳細的錯誤信息，從而改善用戶體驗和問題排查流程。
