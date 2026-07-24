from marshmallow import Schema, fields, validate


class SpecificationInputSchema(Schema):
    group_name = fields.String(required=False, load_default="مواصفات عامة")
    key_ar = fields.String(required=True, validate=validate.Length(min=1, max=150))
    key_en = fields.String(required=False, allow_none=True)
    value_ar = fields.String(required=True, validate=validate.Length(min=1, max=500))
    value_en = fields.String(required=False, allow_none=True)


class AdminProductCreateSchema(Schema):
    name_ar = fields.String(required=True, validate=validate.Length(min=2, max=255))
    name_en = fields.String(required=True, validate=validate.Length(min=2, max=255))
    description_ar = fields.String(required=False, allow_none=True)
    description_en = fields.String(required=False, allow_none=True)
    model_number = fields.String(required=False, allow_none=True)
    brand_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    release_date = fields.Date(required=False, allow_none=True)
    is_active = fields.Boolean(required=False, load_default=True)
    image_url = fields.String(required=False, allow_none=True)
    specifications = fields.List(fields.Nested(SpecificationInputSchema), required=False, load_default=[])


class AdminProductUpdateSchema(Schema):
    name_ar = fields.String(required=False, validate=validate.Length(min=2, max=255))
    name_en = fields.String(required=False, validate=validate.Length(min=2, max=255))
    description_ar = fields.String(required=False, allow_none=True)
    description_en = fields.String(required=False, allow_none=True)
    model_number = fields.String(required=False, allow_none=True)
    brand_id = fields.Integer(required=False)
    category_id = fields.Integer(required=False)
    release_date = fields.Date(required=False, allow_none=True)
    is_active = fields.Boolean(required=False)
    image_url = fields.String(required=False, allow_none=True)
    specifications = fields.List(fields.Nested(SpecificationInputSchema), required=False)


class AdminUserUpdateSchema(Schema):
    is_active = fields.Boolean(required=False)
    role = fields.String(required=False, validate=validate.OneOf(["user", "admin"]))
