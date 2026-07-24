"""
Favorites API Endpoints:
    GET   /api/v1/favorites               - قائمة المنتجات المفضَّلة الكاملة
    GET   /api/v1/favorites/ids           - قائمة معرّفات المنتجات المفضَّلة فقط (خفيفة)
    POST  /api/v1/favorites/<id>/toggle   - إضافة/إزالة منتج من المفضلة
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.favorite_service import FavoriteService
from app.schemas.product_schema import ProductListItemSchema

favorites_bp = Blueprint("favorites", __name__, url_prefix="/api/v1/favorites")

favorite_service = FavoriteService()
product_list_schema = ProductListItemSchema()


@favorites_bp.route("", methods=["GET"])
@jwt_required()
def list_favorites():
    """
    قائمة المنتجات المفضَّلة للمستخدم الحالي
    ---
    tags:
      - Favorites
    security:
      - Bearer: []
    responses:
      200:
        description: قائمة المنتجات المفضَّلة
    """
    user_id = int(get_jwt_identity())
    products = favorite_service.list_favorites(user_id)
    return jsonify({"data": product_list_schema.dump(products, many=True)}), 200


@favorites_bp.route("/ids", methods=["GET"])
@jwt_required()
def list_favorite_ids():
    """
    قائمة معرّفات المنتجات المفضَّلة فقط (لتظليل القلب بسرعة في الواجهة)
    ---
    tags:
      - Favorites
    security:
      - Bearer: []
    responses:
      200:
        description: قائمة المعرّفات
    """
    user_id = int(get_jwt_identity())
    ids = favorite_service.list_favorite_ids(user_id)
    return jsonify({"data": ids}), 200


@favorites_bp.route("/<int:product_id>/toggle", methods=["POST"])
@jwt_required()
def toggle_favorite(product_id):
    """
    إضافة/إزالة منتج من المفضلة (Toggle)
    ---
    tags:
      - Favorites
    security:
      - Bearer: []
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
    responses:
      200:
        description: تم تبديل حالة المفضلة، يرجع {"favorited": true|false}
      404:
        description: المنتج غير موجود
    """
    user_id = int(get_jwt_identity())
    is_favorited = favorite_service.toggle(user_id, product_id)
    return jsonify({"favorited": is_favorited}), 200
