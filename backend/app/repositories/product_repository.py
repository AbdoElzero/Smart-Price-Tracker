from sqlalchemy import or_, and_
from app.models import Product, Category, Brand, Price
from app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    model = Product

    def find_by_slug(self, slug):
        return Product.query.filter_by(slug=slug, is_active=True).first()

    def find_by_ids(self, ids):
        if not ids:
            return []
        products = Product.query.filter(
            Product.id.in_(ids), Product.is_active.is_(True)
        ).all()
        order_map = {pid: idx for idx, pid in enumerate(ids)}
        return sorted(products, key=lambda p: order_map.get(p.id, len(ids)))

    def search(
        self,
        query=None,
        category_slug=None,
        brand_slug=None,
        brand_ids=None,
        min_price=None,
        max_price=None,
        page=1,
        per_page=12,
        sort="newest",
    ):
        q = Product.query.filter_by(is_active=True)

        # البحث بالنص
        if query:
            like = f"%{query.strip()}%"
            q = q.filter(
                or_(
                    Product.name_ar.ilike(like),
                    Product.name_en.ilike(like),
                    Product.model_number.ilike(like),
                )
            )

        # فلتر الفئة
        if category_slug:
            q = q.join(Category, Product.category_id == Category.id).filter(
                Category.slug == category_slug
            )

        # فلتر علامة تجارية واحدة
        if brand_slug:
            q = q.join(Brand, Product.brand_id == Brand.id).filter(
                Brand.slug == brand_slug
            )

        # فلتر علامات تجارية متعددة (من صفحة الفئات)
        if brand_ids:
            q = q.filter(Product.brand_id.in_(brand_ids))

        # فلتر السعر (نحتاج Join مع جدول الأسعار)
        if min_price is not None or max_price is not None:
            price_filter = [Price.product_id == Product.id, Price.in_stock.is_(True)]
            if min_price is not None:
                price_filter.append(Price.current_price >= min_price)
            if max_price is not None:
                price_filter.append(Price.current_price <= max_price)
            q = q.join(Price, and_(*price_filter))

        # الترتيب
        if sort == "name_asc":
            q = q.order_by(Product.name_ar.asc())
        elif sort == "name_desc":
            q = q.order_by(Product.name_ar.desc())
        elif sort == "price_asc":
            q = (
                q.outerjoin(Price, and_(Price.product_id == Product.id, Price.in_stock.is_(True)))
                .order_by(Price.current_price.asc().nulls_last())
            )
        elif sort == "price_desc":
            q = (
                q.outerjoin(Price, and_(Price.product_id == Product.id, Price.in_stock.is_(True)))
                .order_by(Price.current_price.desc().nulls_last())
            )
        else:
            q = q.order_by(Product.created_at.desc())

        q = q.distinct()
        total = q.count()
        items = q.offset((page - 1) * per_page).limit(per_page).all()
        return items, total
