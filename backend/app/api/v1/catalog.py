"""
Catalog API Endpoints:
    GET  /api/v1/categories  - قائمة التصنيفات الرئيسية وفروعها
    GET  /api/v1/brands      - قائمة العلامات التجارية
    GET  /api/v1/countries   - قائمة الدول المدعومة
"""
from flask import Blueprint, jsonify

from app.services.catalog_service import CatalogService
from app.schemas.catalog_schema import CategorySchema, BrandSchema, CountrySchema

catalog_bp = Blueprint("catalog", __name__, url_prefix="/api/v1")

catalog_service = CatalogService()


@catalog_bp.route("/categories", methods=["GET"])
def list_categories():
    """
    قائمة التصنيفات الرئيسية مع فروعها
    ---
    tags:
      - Catalog
    responses:
      200:
        description: قائمة التصنيفات
    """
    categories = catalog_service.list_categories()
    return jsonify({"data": CategorySchema(many=True).dump(categories)}), 200


@catalog_bp.route("/brands", methods=["GET"])
def list_brands():
    """
    قائمة العلامات التجارية
    ---
    tags:
      - Catalog
    responses:
      200:
        description: قائمة العلامات التجارية
    """
    brands = catalog_service.list_brands()
    return jsonify({"data": BrandSchema(many=True).dump(brands)}), 200


@catalog_bp.route("/countries", methods=["GET"])
def list_countries():
    """
    قائمة الدول المدعومة
    ---
    tags:
      - Catalog
    responses:
      200:
        description: قائمة الدول
    """
    countries = catalog_service.list_countries()
    return jsonify({"data": CountrySchema(many=True).dump(countries)}), 200
