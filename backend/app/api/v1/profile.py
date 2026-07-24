"""
Profile API Endpoints:
    PUT  /api/v1/profile           - تعديل الاسم/الدولة المفضّلة
    PUT  /api/v1/profile/password  - تغيير كلمة السر
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.profile_schema import UpdateProfileSchema, ChangePasswordSchema
from app.schemas.auth_schema import UserResponseSchema
from app.services.profile_service import ProfileService

profile_bp = Blueprint("profile", __name__, url_prefix="/api/v1/profile")

profile_service = ProfileService()
update_schema = UpdateProfileSchema()
password_schema = ChangePasswordSchema()
user_schema = UserResponseSchema()


@profile_bp.route("", methods=["PUT"])
@jwt_required()
def update_profile():
    """
    تعديل بيانات الملف الشخصي (الاسم، الدولة المفضّلة)
    ---
    tags:
      - Profile
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:
              type: string
            preferred_country_id:
              type: integer
    responses:
      200:
        description: تم تحديث البيانات بنجاح
    """
    user_id = int(get_jwt_identity())
    data = update_schema.load(request.get_json() or {})
    user = profile_service.update_profile(user_id, data)
    return jsonify({"user": user_schema.dump(user)}), 200


@profile_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():
    """
    تغيير كلمة السر
    ---
    tags:
      - Profile
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required: [current_password, new_password]
          properties:
            current_password:
              type: string
            new_password:
              type: string
    responses:
      200:
        description: تم تغيير كلمة السر بنجاح
      401:
        description: كلمة السر الحالية غير صحيحة، أو الحساب عبر Google بدون كلمة سر
    """
    user_id = int(get_jwt_identity())
    data = password_schema.load(request.get_json() or {})
    profile_service.change_password(user_id, data)
    return jsonify({"message": "تم تغيير كلمة السر بنجاح"}), 200


@profile_bp.route("/avatar", methods=["POST"])
@jwt_required()
def upload_avatar():
    """
    رفع/تحديث صورة الملف الشخصي
    ---
    tags:
      - Profile
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: formData
        name: avatar
        type: file
        required: true
        description: ملف صورة (png, jpg, jpeg, webp) بحد أقصى 5 ميجابايت
    responses:
      200:
        description: تم تحديث صورة الملف الشخصي بنجاح
      422:
        description: صورة غير صالحة أو صيغة غير مدعومة
    """
    user_id = int(get_jwt_identity())
    file_storage = request.files.get("avatar")
    user = profile_service.update_avatar(user_id, file_storage)
    return jsonify({"user": user_schema.dump(user)}), 200
