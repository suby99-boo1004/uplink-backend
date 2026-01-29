from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# 역할 우선순위(권한 비교용)
ROLE_ORDER = {
    "guest": 0,
    "external": 1,
    "staff": 2,
    "operator": 3,
    "admin": 4,
}

def require_role(min_role: str):
    """min_role 이상만 접근 허용.
    예) @require_role("operator") => operator/admin만 통과
    JWT payload에 role 키가 들어있다는 가정.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = (claims.get("role") or "guest").lower()
            if ROLE_ORDER.get(role, -1) < ROLE_ORDER.get(min_role, 999):
                return jsonify({"detail": "권한이 없습니다.", "required": min_role, "role": role}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
