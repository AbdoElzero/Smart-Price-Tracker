from marshmallow import Schema, fields


class CategorySchema(Schema):
    id = fields.Integer()
    name_ar = fields.String()
    name_en = fields.String()
    slug = fields.String()
    icon = fields.String(allow_none=True)
    children = fields.Method("get_children")

    def get_children(self, obj):
        children = obj.children.filter_by(is_active=True).order_by("sort_order").all()
        return CategorySchema(many=True, exclude=("children",)).dump(children)


class BrandSchema(Schema):
    id = fields.Integer()
    name_ar = fields.String()
    name_en = fields.String()
    slug = fields.String()
    logo_url = fields.String(allow_none=True)


class CountrySchema(Schema):
    id = fields.Integer()
    code = fields.String()
    name_ar = fields.String()
    name_en = fields.String()
    flag_emoji = fields.String(allow_none=True)
    currency_code = fields.Method("get_currency_code")
    currency_symbol = fields.Method("get_currency_symbol")

    def get_currency_code(self, obj):
        return obj.currency.code if obj.currency else None

    def get_currency_symbol(self, obj):
        return obj.currency.symbol if obj.currency else None
