"""
معالجات استجابات JWT المخصّصة (رسائل عربية واضحة بدل رسائل flask-jwt-extended الافتراضية).
"""
from flask import jsonify
from app.extensions import jwt


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "انتهت صلاحية التوكن، يرجى تسجيل الدخول من جديد"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "توكن غير صالح"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "التوكن مطلوب للوصول لهذا المسار"}), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "تم إلغاء هذا التوكن"}), 401
