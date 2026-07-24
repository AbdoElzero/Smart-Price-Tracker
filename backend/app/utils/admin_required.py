"""
Decorator للتحقق من صلاحية المشرف (Admin) على مستوى كل endpoint.
الاستخدام:
    @jwt_required()
    @admin_required
    def my_admin_endpoint():
        ...
"""
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models import User, UserRole
from app.errors.exceptions import ForbiddenError


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        if not user or user.role != UserRole.ADMIN:
            raise ForbiddenError("هذه اللوحة متاحة للمشرفين فقط")
        return fn(*args, **kwargs)
    return wrapper
