"""
Authentication API Endpoints:
    POST   /api/v1/auth/register
    POST   /api/v1/auth/login
    POST   /api/v1/auth/google
    POST   /api/v1/auth/refresh
    GET    /api/v1/auth/me
    POST   /api/v1/auth/logout
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from app.schemas.auth_schema import (
    RegisterSchema,
    LoginSchema,
    GoogleLoginSchema,
    UserResponseSchema,
)
from app.services.auth_service import AuthService
from app.errors.exceptions import NotFoundError

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

auth_service = AuthService()
register_schema = RegisterSchema()
login_schema = LoginSchema()
google_schema = GoogleLoginSchema()
user_schema = UserResponseSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    تسجيل مستخدم جديد
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, email, password]
          properties:
            name:
              type: string
              example: "أحمد محمد"
            email:
              type: string
              example: "ahmed@example.com"
            password:
              type: string
              example: "StrongPass123"
            preferred_country_id:
              type: integer
              example: 1
    responses:
      201:
        description: تم إنشاء الحساب بنجاح، يرجع access_token و refresh_token
      409:
        description: البريد الإلكتروني مستخدم مسبقًا
      422:
        description: بيانات غير صحيحة
    """
    data = register_schema.load(request.get_json() or {})
    tokens, user = auth_service.register(data)
    return jsonify({"user": user_schema.dump(user), **tokens}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    تسجيل الدخول بالبريد الإلكتروني وكلمة السر
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: تم تسجيل الدخول بنجاح
      401:
        description: بيانات الدخول غير صحيحة
    """
    data = login_schema.load(request.get_json() or {})
    tokens, user = auth_service.login(data)
    return jsonify({"user": user_schema.dump(user), **tokens}), 200


@auth_bp.route("/google", methods=["POST"])
def google_login():
    """
    تسجيل الدخول / التسجيل عبر Google
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [id_token]
          properties:
            id_token:
              type: string
              description: ID Token القادم من Google Sign-In في الفرونت إند
    responses:
      200:
        description: تم تسجيل الدخول بنجاح عبر Google
      401:
        description: رمز Google غير صالح
    """
    data = google_schema.load(request.get_json() or {})
    tokens, user = auth_service.login_with_google(data["id_token"])
    return jsonify({"user": user_schema.dump(user), **tokens}), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """
    إصدار access_token جديد باستخدام refresh_token
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: تم إصدار access_token جديد
      401:
        description: refresh_token غير صالح أو منتهي
    """
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    return jsonify({"access_token": new_access_token}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """
    بيانات المستخدم الحالي (المسجَّل دخوله)
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: بيانات المستخدم
      404:
        description: المستخدم غير موجود
    """
    user_id = get_jwt_identity()
    user = auth_service.get_user_by_id(int(user_id))
    if not user:
        raise NotFoundError("المستخدم غير موجود")
    return jsonify({"user": user_schema.dump(user)}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    تسجيل الخروج
    ---
    tags:
      - Authentication
    security:
      - Bearer: []
    responses:
      200:
        description: تم تسجيل الخروج بنجاح
    """
    # في هذا التصميم، يتم حذف التوكن من جهة العميل (Frontend).
    # لإلغاء التوكن من جهة السيرفر أيضًا (Token Blocklist عبر Redis)، يمكن إضافته لاحقًا
    # عند الحاجة لمستوى أمان أعلى (مثل: تسجيل خروج إجباري لمستخدم من الأدمن).
    return jsonify({"message": "تم تسجيل الخروج بنجاح"}), 200
