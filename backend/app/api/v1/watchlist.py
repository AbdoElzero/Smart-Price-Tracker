"""
Watchlist API Endpoints:
    GET    /api/v1/watchlist              - قائمة المتابعة الخاصة بالمستخدم
    POST   /api/v1/watchlist/<product_id> - إضافة/تحديث (سعر مستهدف اختياري)
    DELETE /api/v1/watchlist/<product_id> - إزالة من قائمة المتابعة
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.watchlist_service import WatchlistService
from app.schemas.watchlist_schema import WatchlistUpsertSchema, WatchlistItemSchema

watchlist_bp = Blueprint("watchlist", __name__, url_prefix="/api/v1/watchlist")

watchlist_service = WatchlistService()
upsert_schema = WatchlistUpsertSchema()
item_schema = WatchlistItemSchema()


@watchlist_bp.route("", methods=["GET"])
@jwt_required()
def list_watchlist():
    """
    قائمة المتابعة الخاصة بالمستخدم الحالي
    ---
    tags:
      - Watchlist
    security:
      - Bearer: []
    responses:
      200:
        description: قائمة المتابعة (مع المنتج والسعر المستهدف)
    """
    user_id = int(get_jwt_identity())
    items = watchlist_service.list_for_user(user_id)
    return jsonify({"data": item_schema.dump(items, many=True)}), 200


@watchlist_bp.route("/<int:product_id>", methods=["POST"])
@jwt_required()
def upsert_watchlist(product_id):
    """
    إضافة منتج لقائمة المتابعة أو تحديث السعر المستهدف له
    ---
    tags:
      - Watchlist
    security:
      - Bearer: []
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          type: object
          properties:
            target_price:
              type: number
              description: السعر المستهدف (اختياري) - يُنبَّه المستخدم عند الوصول له
            notify_on_any_drop:
              type: boolean
              description: تنبيه عند أي انخفاض في السعر (حتى لو لم يصل للسعر المستهدف)
    responses:
      200:
        description: تمت الإضافة/التحديث بنجاح
      404:
        description: المنتج غير موجود
    """
    user_id = int(get_jwt_identity())
    data = upsert_schema.load(request.get_json() or {})
    item = watchlist_service.add_or_update(user_id, product_id, data)
    return jsonify({"data": item_schema.dump(item)}), 200


@watchlist_bp.route("/<int:product_id>", methods=["DELETE"])
@jwt_required()
def remove_watchlist(product_id):
    """
    إزالة منتج من قائمة المتابعة
    ---
    tags:
      - Watchlist
    security:
      - Bearer: []
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
    responses:
      200:
        description: تمت الإزالة بنجاح
      404:
        description: المنتج غير موجود في قائمة المتابعة
    """
    user_id = int(get_jwt_identity())
    watchlist_service.remove(user_id, product_id)
    return jsonify({"message": "تمت الإزالة من قائمة المتابعة"}), 200
