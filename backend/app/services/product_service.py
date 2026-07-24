import math
from app.repositories.product_repository import ProductRepository
from app.errors.exceptions import NotFoundError


class ProductService:
    def __init__(self):
        self.product_repo = ProductRepository()

    def list_products(self, args):
        page = max(int(args.get("page", 1)), 1)
        per_page = min(max(int(args.get("per_page", 12)), 1), 50)
        query = args.get("q")
        category_slug = args.get("category")
        brand_slug = args.get("brand")
        sort = args.get("sort", "newest")

        # فلاتر متقدمة
        min_price = float(args["min_price"]) if args.get("min_price") else None
        max_price = float(args["max_price"]) if args.get("max_price") else None

        # علامات تجارية متعددة
        brand_ids = None
        if args.get("brands"):
            try:
                brand_ids = [int(i) for i in args["brands"].split(",") if i.strip()]
            except ValueError:
                brand_ids = None

        items, total = self.product_repo.search(
            query=query,
            category_slug=category_slug,
            brand_slug=brand_slug,
            brand_ids=brand_ids,
            min_price=min_price,
            max_price=max_price,
            page=page,
            per_page=per_page,
            sort=sort,
        )

        meta = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": math.ceil(total / per_page) if total else 0,
        }
        return items, meta

    def get_by_slug(self, slug):
        product = self.product_repo.find_by_slug(slug)
        if not product:
            raise NotFoundError("المنتج غير موجود")
        return product

    def compare(self, ids):
        cleaned_ids = []
        for raw_id in ids[:4]:
            try:
                cleaned_ids.append(int(raw_id))
            except (TypeError, ValueError):
                continue
        return self.product_repo.find_by_ids(cleaned_ids)
