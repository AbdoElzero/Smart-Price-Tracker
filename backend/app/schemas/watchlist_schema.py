from marshmallow import Schema, fields
from app.schemas.product_schema import ProductListItemSchema


class WatchlistUpsertSchema(Schema):
    target_price = fields.Decimal(required=False, allow_none=True, places=2)
    notify_on_any_drop = fields.Boolean(required=False, load_default=True)


class WatchlistItemSchema(Schema):
    id = fields.Integer()
    target_price = fields.Decimal(as_string=True, allow_none=True)
    notify_on_any_drop = fields.Boolean()
    created_at = fields.DateTime()
    product = fields.Nested(ProductListItemSchema)
