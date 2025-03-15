"""
範例：展示如何將 funapis-response 與 Flask 框架整合
"""

from flask import Flask, request, jsonify

from funapis_response import (
    ResponsePayloadBuilder,
    FunAPIException,
    ValidationError,
    APIError,
    UnknownError,
    ErrorCode,
    ErrorSeverity,
    UserLevel
)

app = Flask(__name__)

# 自定義錯誤碼
USER_NOT_FOUND = ErrorCode(
    code="FUN123400001",
    severity=ErrorSeverity.WARNING,
    message_template="使用者 '{username}' 不存在"
)

USER_UNAUTHORIZED = ErrorCode(
    code="FUN123400002",
    severity=ErrorSeverity.ERROR,
    message_template="使用者沒有訪問 '{resource}' 的權限"
)


# 自定義例外
class UserNotFoundError(FunAPIException):
    def __init__(self, username, **kwargs):
        super().__init__(
            error_code=USER_NOT_FOUND,
            message_params={"username": username},
            **kwargs
        )


class UnauthorizedError(FunAPIException):
    def __init__(self, resource, **kwargs):
        super().__init__(
            error_code=USER_UNAUTHORIZED,
            message_params={"resource": resource},
            **kwargs
        )


# 註冊全局例外處理器
@app.errorhandler(FunAPIException)
def handle_fun_api_exception(error):
    """處理所有 FunAPIException 子類"""
    response = error.to_response_payload()
    
    # 將響應物件轉換為字典，根據當前使用者級別決定是否包含堆疊追蹤
    # 這裡使用開發者級別以便於演示查看堆疊追蹤
    response_dict = response.to_dict(UserLevel.DEVELOPER)
    
    # 根據錯誤嚴重程度設置 HTTP 狀態碼
    if error.error_code.severity == ErrorSeverity.WARNING:
        status_code = 400
    elif error.error_code.severity == ErrorSeverity.ERROR:
        status_code = 403
    elif error.error_code.severity == ErrorSeverity.FATAL:
        status_code = 500
    else:
        status_code = 200
    
    return jsonify(response_dict), status_code


@app.errorhandler(Exception)
def handle_general_exception(error):
    """處理所有未捕獲的例外"""
    # 將未捕獲的例外轉換為 UnknownError
    fun_error = UnknownError(str(error))
    response = fun_error.to_response_payload()
    response_dict = response.to_dict(UserLevel.DEVELOPER)
    
    return jsonify(response_dict), 500


# 示例路由
@app.route('/api/users', methods=['GET'])
def get_users():
    """獲取使用者列表"""
    users = [
        {"id": 1, "username": "user1"},
        {"id": 2, "username": "user2"}
    ]
    
    return jsonify(
        ResponsePayloadBuilder.success(users).build().to_dict()
    )


@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    """根據使用者名稱獲取使用者"""
    if username not in ['user1', 'user2']:
        raise UserNotFoundError(username=username)
    
    user = {"id": 1, "username": username}
    return jsonify(
        ResponsePayloadBuilder.success(user).build().to_dict()
    )


@app.route('/api/users', methods=['POST'])
def create_user():
    """創建新使用者"""
    data = request.json
    
    # 參數驗證
    if not data:
        raise ValidationError(reason="請求內容不能為空")
    
    if 'username' not in data:
        raise ValidationError(reason="使用者名稱是必需的")
    
    if len(data['username']) < 3:
        raise ValidationError(reason="使用者名稱必須至少包含 3 個字符")
    
    # 創建新使用者
    user = {
        "id": 3,
        "username": data['username']
    }
    
    return jsonify(
        ResponsePayloadBuilder.success(user).build().to_dict()
    ), 201


@app.route('/api/admin/users', methods=['GET'])
def admin_get_users():
    """管理員獲取使用者列表 - 需要權限檢查"""
    # 模擬權限檢查
    is_admin = request.headers.get('X-Role') == 'admin'
    
    if not is_admin:
        raise UnauthorizedError(resource="admin/users")
    
    users = [
        {"id": 1, "username": "user1", "role": "user"},
        {"id": 2, "username": "user2", "role": "user"},
        {"id": 3, "username": "admin", "role": "admin"}
    ]
    
    return jsonify(
        ResponsePayloadBuilder.success(users).build().to_dict()
    )


@app.route('/api/error/demo', methods=['GET'])
def error_demo():
    """演示未捕獲例外的處理"""
    # 故意製造一個未捕獲的例外
    1 / 0  # 除以零錯誤
    
    # 不會執行到這裡
    return jsonify({"message": "This will never be returned"})


if __name__ == "__main__":
    print("=== Flask 整合 funapis-response 示例 ===")
    print("請使用 API 測試工具 (如 Postman, curl 等) 測試以下端點:")
    print("GET  /api/users           - 獲取所有使用者")
    print("GET  /api/users/<username> - 獲取特定使用者")
    print("POST /api/users           - 創建新使用者")
    print("GET  /api/admin/users     - 獲取管理員使用者列表 (需要 X-Role: admin 標頭)")
    print("GET  /api/error/demo      - 觸發未捕獲例外")
    print("\n啟動 Flask 服務器...")
    
    app.run(debug=True, port=5000)
