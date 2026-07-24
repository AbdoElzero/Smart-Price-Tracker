"""
استثناءات مخصّصة للتطبيق، تُستخدم في كل الـ Services بدل رفع أخطاء عامة.
كل استثناء له status_code ورسالة افتراضية بالعربية.
"""


class AppError(Exception):
    status_code = 400
    message = "حدث خطأ غير متوقع"

    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__(message or self.message)
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload or {}

    def to_dict(self):
        result = {"error": self.message}
        result.update(self.payload)
        return result


class ValidationAppError(AppError):
    status_code = 422
    message = "بيانات غير صحيحة"


class AuthError(AppError):
    status_code = 401
    message = "بيانات الدخول غير صحيحة"


class ForbiddenError(AppError):
    status_code = 403
    message = "لا تملك صلاحية الوصول لهذا المورد"


class ConflictError(AppError):
    status_code = 409
    message = "البيانات موجودة مسبقًا"


class NotFoundError(AppError):
    status_code = 404
    message = "العنصر غير موجود"
