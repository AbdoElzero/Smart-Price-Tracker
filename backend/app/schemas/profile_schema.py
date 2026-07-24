from marshmallow import Schema, fields, validate


class UpdateProfileSchema(Schema):
    name = fields.String(required=False, validate=validate.Length(min=2, max=150))
    preferred_country_id = fields.Integer(required=False, allow_none=True)


class ChangePasswordSchema(Schema):
    current_password = fields.String(required=True)
    new_password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128, error="كلمة السر الجديدة يجب أن تكون 8 أحرف على الأقل"),
    )
