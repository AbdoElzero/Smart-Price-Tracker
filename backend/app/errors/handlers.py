"""
تسجيل معالجات الأخطاء الموحّدة على مستوى التطبيق بالكامل،
بحيث ترجع كل الأخطاء بصيغة JSON ثابتة: {"error": "...", ...}
"""
from flask import jsonify
from marshmallow import ValidationError as MarshmallowValidationError
from app.errors.exceptions import AppError


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(MarshmallowValidationError)
    def handle_marshmallow_error(error):
        return jsonify({"error": "بيانات غير صحيحة", "details": error.messages}), 422

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"error": "المسار المطلوب غير موجود"}), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({"error": "الطريقة (Method) غير مسموحة لهذا المسار"}), 405

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({"error": "حدث خطأ داخلي في السيرفر"}), 500
