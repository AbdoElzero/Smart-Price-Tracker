from marshmallow import Schema, fields


class NotificationItemSchema(Schema):
    id = fields.Integer()
    type = fields.Method("get_type")
    title = fields.String()
    message = fields.String()
    is_read = fields.Boolean()
    related_product_id = fields.Integer(allow_none=True)
    created_at = fields.DateTime()

    def get_type(self, obj):
        return obj.type.value if obj.type else None


class NotificationsMetaSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()
    total_pages = fields.Integer()
    unread_count = fields.Integer()
