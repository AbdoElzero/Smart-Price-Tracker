"""
Marshmallow Schemas للتحقق من صحة بيانات الإدخال (Validation)
وتنسيق بيانات الإخراج (Serialization) لكل ما يخص Authentication.
"""
from marshmallow import Schema, fields, validate


class RegisterSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=2, max=150))
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128, error="كلمة السر يجب أن تكون 8 أحرف على الأقل"),
    )
    preferred_country_id = fields.Integer(required=False, allow_none=True)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


class GoogleLoginSchema(Schema):
    id_token = fields.String(required=True)


class UserResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    email = fields.Email()
    avatar_url = fields.String(allow_none=True)
    role = fields.Method("get_role")
    is_verified = fields.Boolean()
    preferred_country_id = fields.Integer(allow_none=True)
    has_password = fields.Method("get_has_password")
    created_at = fields.DateTime()

    def get_role(self, obj):
        return obj.role.value if obj.role else None

    def get_has_password(self, obj):
        return obj.password_hash is not None
