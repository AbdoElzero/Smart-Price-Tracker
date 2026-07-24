from marshmallow import Schema, fields


class CategoryBriefSchema(Schema):
    id = fields.Integer()
    name_ar = fields.String()
    name_en = fields.String()
    slug = fields.String()
    icon = fields.String(allow_none=True)


class BrandBriefSchema(Schema):
    id = fields.Integer()
    name_ar = fields.String()
    name_en = fields.String()
    slug = fields.String()
    logo_url = fields.String(allow_none=True)


class ProductImageSchema(Schema):
    id = fields.Integer()
    image_url = fields.String()
    is_primary = fields.Boolean()


class PriceBriefSchema(Schema):
    store_name = fields.Method("get_store_name")
    store_slug = fields.Method("get_store_slug")
    country_code = fields.Method("get_country_code")
    current_price = fields.Decimal(as_string=True)
    old_price = fields.Decimal(as_string=True, allow_none=True)
    currency_symbol = fields.Method("get_currency_symbol")
    in_stock = fields.Boolean()
    product_url = fields.String()

    def get_store_name(self, obj):
        return obj.store.name_ar if obj.store else None

    def get_store_slug(self, obj):
        return obj.store.slug if obj.store else None

    def get_country_code(self, obj):
        return obj.country.code if obj.country else None

    def get_currency_symbol(self, obj):
        return obj.currency.symbol if obj.currency else None


class ProductListItemSchema(Schema):
    id = fields.Integer()
    name_ar = fields.String()
    name_en = fields.String()
    slug = fields.String()
    is_active = fields.Boolean()  # ← مهم للوحة التحكم
    brand = fields.Nested(BrandBriefSchema)
    category = fields.Nested(CategoryBriefSchema)
    primary_image = fields.Method("get_primary_image")
    lowest_price = fields.Method("get_lowest_price")

    def get_primary_image(self, obj):
        image = obj.images.filter_by(is_primary=True).first() or obj.images.first()
        return image.image_url if image else None

    def get_lowest_price(self, obj):
        prices = obj.prices.filter_by(in_stock=True).all()
        if not prices:
            return None
        cheapest = min(prices, key=lambda p: p.current_price)
        return {
            "amount": str(cheapest.current_price),
            "currency_symbol": cheapest.currency.symbol if cheapest.currency else "",
            "store_name": cheapest.store.name_ar if cheapest.store else "",
        }


class ProductDetailSchema(ProductListItemSchema):
    description_ar = fields.String(allow_none=True)
    description_en = fields.String(allow_none=True)
    model_number = fields.String(allow_none=True)
    images = fields.Method("get_images")
    specifications = fields.Method("get_specifications")
    prices = fields.Method("get_prices")

    def get_images(self, obj):
        return ProductImageSchema(many=True).dump(obj.images.order_by("sort_order").all())

    def get_specifications(self, obj):
        specs = obj.specifications.order_by("sort_order").all()
        grouped = {}
        for s in specs:
            grouped.setdefault(s.group_name, []).append({"key": s.key_ar, "value": s.value_ar})
        return grouped

    def get_prices(self, obj):
        return PriceBriefSchema(many=True).dump(obj.prices.all())


class PaginationMetaSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total = fields.Integer()
    total_pages = fields.Integer()
