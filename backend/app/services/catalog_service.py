from app.models import Category, Brand, Country


class CatalogService:
    def list_categories(self):
        return (
            Category.query.filter_by(is_active=True, parent_id=None)
            .order_by(Category.sort_order)
            .all()
        )

    def list_brands(self):
        return Brand.query.filter_by(is_active=True).order_by(Brand.name_en).all()

    def list_countries(self):
        return Country.query.filter_by(is_active=True).order_by(Country.name_ar).all()
