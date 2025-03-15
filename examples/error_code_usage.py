"""
範例：展示如何使用 funapis-response 的錯誤碼機制
"""

from funapis_response import (
    ResponsePayloadBuilder,
    CommonErrorCodes,
    ValidationError,
    APIError,
    ErrorCode,
    ErrorSeverity
)

# 1. 基本使用 - 成功響應
def basic_usage_success():
    # 使用 success() 便捷方法
    success_response = ResponsePayloadBuilder.success(
        {"id": 1, "name": "測試使用者"}
    ).build()
    
    print("成功響應:")
    print(f"錯誤碼: {success_response.error_code}")
    print(f"錯誤描述: {success_response.error_desc}")
    print(f"數據: {success_response.data}")
    print()


# 2. 基本使用 - 錯誤響應
def basic_usage_error():
    # 使用 with_error() 方法
    error_response = ResponsePayloadBuilder()\
        .with_error(CommonErrorCodes.VALIDATION_ERROR, reason="使用者名稱不能為空")\
        .build()
    
    print("錯誤響應:")
    print(f"錯誤碼: {error_response.error_code}")
    print(f"錯誤描述: {error_response.error_desc}")
    print()


# 3. 使用例外處理
def exception_handling():
    try:
        username = ""
        if not username:
            raise ValidationError(reason="使用者名稱不能為空", include_trace=True)
        
        # 業務邏輯...
    
    except ValidationError as e:
        # 從例外創建響應
        error_response = e.to_response_payload()
        
        print("從例外創建的響應:")
        print(f"錯誤碼: {error_response.error_code}")
        print(f"錯誤描述: {error_response.error_desc}")
        print(f"堆疊追蹤長度: {len(error_response._stack_trace) if error_response._stack_trace else 0}")
        print()


# 4. 自定義錯誤碼
def custom_error_codes():
    # 創建自定義錯誤碼
    USER_NOT_FOUND = ErrorCode(
        code="FUN123456001",
        severity=ErrorSeverity.WARNING,
        message_template="使用者 '{username}' 不存在"
    )
    
    # 使用自定義錯誤碼
    response = ResponsePayloadBuilder()\
        .with_error(USER_NOT_FOUND, username="test_user")\
        .build()
    
    print("自定義錯誤碼響應:")
    print(f"錯誤碼: {response.error_code}")
    print(f"錯誤描述: {response.error_desc}")
    print()


# 5. 使用自定義例外
def custom_exception():
    # 定義自定義例外
    class UserNotFoundError(APIError):
        def __init__(self, username, **kwargs):
            super().__init__(
                message=f"使用者 '{username}' 不存在", 
                **kwargs
            )
    
    # 使用自定義例外
    try:
        raise UserNotFoundError("test_user")
    except UserNotFoundError as e:
        response = e.to_response_payload()
        
        print("自定義例外響應:")
        print(f"錯誤碼: {response.error_code}")
        print(f"錯誤描述: {response.error_desc}")
        print()


if __name__ == "__main__":
    print("=== funapis-response 錯誤碼機制使用範例 ===\n")
    basic_usage_success()
    basic_usage_error()
    exception_handling()
    custom_error_codes()
    custom_exception()
