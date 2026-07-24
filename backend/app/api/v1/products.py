"""
Products API Endpoints - مُحدَّث بدعم فلاتر متقدمة.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

from app.services.product_service import ProductService
from app.schemas.product_schema import (
    ProductListItemSchema, ProductDetailSchema, PaginationMetaSchema
)

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

product_service = ProductService()
list_schema = ProductListItemSchema()
detail_schema = ProductDetailSchema()
meta_schema = PaginationMetaSchema()


@products_bp.route("", methods=["GET"])
def list_products():
    """
    قائمة المنتجات مع فلاتر متقدمة
    ---
    tags:
      - Products
    parameters:
      - in: query
        name: q
        type: string
      - in: query
        name: category
        type: string
      - in: query
        name: brand
        type: string
      - in: query
        name: brands
        type: string
        description: عدة علامات تجارية مفصولة بفاصلة (brand_ids)
      - in: query
        name: min_price
        type: number
      - in: query
        name: max_price
        type: number
      - in: query
        name: sort
        type: string
        enum: [newest, name_asc, name_desc, price_asc, price_desc]
      - in: query
        name: page
        type: integer
      - in: query
        name: per_page
        type: integer
    responses:
      200:
        description: قائمة المنتجات
    """
    items, meta = product_service.list_products(request.args)
    return jsonify({
        "data": list_schema.dump(items, many=True),
        "meta": meta_schema.dump(meta),
    }), 200


@products_bp.route("/compare", methods=["GET"])
def compare_products():
    """مقارنة عدة منتجات
    ---
    tags:
      - Products
    parameters:
      - in: query
        name: ids
        type: string
        required: true
    responses:
      200:
        description: تفاصيل المنتجات للمقارنة
    """
    raw_ids = request.args.get("ids", "")
    ids = [i.strip() for i in raw_ids.split(",") if i.strip()]
    products = product_service.compare(ids)
    return jsonify({"data": detail_schema.dump(products, many=True)}), 200


@products_bp.route("/<string:slug>", methods=["GET"])
def get_product(slug):
    """تفاصيل منتج واحد
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: slug
        type: string
        required: true
    responses:
      200:
        description: تفاصيل المنتج
      404:
        description: المنتج غير موجود
    """
    product = product_service.get_by_slug(slug)
    return jsonify({"data": detail_schema.dump(product)}), 200


@products_bp.route("/<int:product_id>/price-history", methods=["GET"])
def get_price_history(product_id):
    """تاريخ الأسعار للرسم البياني
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
      - in: query
        name: days
        type: integer
      - in: query
        name: store_id
        type: integer
    responses:
      200:
        description: بيانات تاريخ الأسعار
    """
    from app.models import Price, PriceHistory

    days = min(max(int(request.args.get("days", 90)), 7), 365)
    store_id = request.args.get("store_id", type=int)
    since = datetime.utcnow() - timedelta(days=days)

    prices_query = Price.query.filter_by(product_id=product_id)
    if store_id:
        prices_query = prices_query.filter_by(store_id=store_id)
    prices = prices_query.all()

    if not prices:
        return jsonify({"data": [], "stores": [], "stats": {}, "days": days}), 200

    all_records = []
    stores_info = []

    for price in prices:
        store_name = price.store.name_ar if price.store else "متجر"
        currency_symbol = price.currency.symbol if price.currency else ""

        if price.store_id not in [s["id"] for s in stores_info]:
            stores_info.append({
                "id": price.store_id,
                "name": store_name,
                "current_price": str(price.current_price),
                "currency_symbol": currency_symbol,
                "in_stock": price.in_stock,
            })

        history = (
            PriceHistory.query
            .filter(PriceHistory.price_id == price.id, PriceHistory.recorded_at >= since)
            .order_by(PriceHistory.recorded_at.asc())
            .all()
        )
        for h in history:
            all_records.append({
                "date": h.recorded_at.strftime("%Y-%m-%d"),
                "price": float(h.recorded_price),
                "store_id": price.store_id,
                "store_name": store_name,
                "currency_symbol": currency_symbol,
            })

        all_records.append({
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "price": float(price.current_price),
            "store_id": price.store_id,
            "store_name": store_name,
            "currency_symbol": currency_symbol,
        })

    if not store_id and len(prices) > 1:
        chart_data = _group_by_store(all_records)
    else:
        chart_data = _group_by_date(all_records)

    all_prices = [r["price"] for r in all_records]
    stats = {}
    if all_prices:
        stats = {
            "min": min(all_prices),
            "max": max(all_prices),
            "avg": round(sum(all_prices) / len(all_prices), 2),
            "currency_symbol": all_records[0]["currency_symbol"] if all_records else "",
        }

    return jsonify({
        "data": chart_data,
        "stores": stores_info,
        "stats": stats,
        "days": days,
    }), 200


def _group_by_date(records):
    from collections import defaultdict
    by_date = defaultdict(list)
    for r in records:
        by_date[r["date"]].append(r["price"])
    return [{"date": d, "price": min(p)} for d, p in sorted(by_date.items())]


def _group_by_store(records):
    from collections import defaultdict
    by_store = defaultdict(lambda: defaultdict(list))
    for r in records:
        by_store[r["store_name"]][r["date"]].append(r["price"])
    result = {}
    for store_name, dates in by_store.items():
        result[store_name] = [
            {"date": d, "price": min(p)} for d, p in sorted(dates.items())
        ]
    return result
