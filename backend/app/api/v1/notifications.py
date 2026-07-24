"""
Notifications API Endpoints:
    GET    /api/v1/notifications                  - قائمة الإشعارات (مع عدد غير المقروء)
    GET    /api/v1/notifications/unread-count      - عدد غير المقروء فقط (خفيف للـ Navbar)
    PUT    /api/v1/notifications/<id>/read         - تعليم إشعار واحد كمقروء
    PUT    /api/v1/notifications/read-all          - تعليم كل الإشعارات كمقروءة
    DELETE /api/v1/notifications/<id>              - حذف إشعار
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.notification_service import NotificationService
from app.schemas.notification_schema import NotificationItemSchema, NotificationsMetaSchema

notifications_bp = Blueprint("notifications", __name__, url_prefix="/api/v1/notifications")

notification_service = NotificationService()
item_schema = NotificationItemSchema()
meta_schema = NotificationsMetaSchema()


@notifications_bp.route("", methods=["GET"])
@jwt_required()
def list_notifications():
    """
    قائمة إشعارات المستخدم الحالي
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: query
        name: page
        type: integer
      - in: query
        name: per_page
        type: integer
    responses:
      200:
        description: قائمة الإشعارات مع بيانات التصفّح وعدد غير المقروء
    """
    user_id = int(get_jwt_identity())
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 20)), 1), 50)

    items, meta = notification_service.list_for_user(user_id, page, per_page)
    return (
        jsonify({"data": item_schema.dump(items, many=True), "meta": meta_schema.dump(meta)}),
        200,
    )


@notifications_bp.route("/unread-count", methods=["GET"])
@jwt_required()
def unread_count():
    """
    عدد الإشعارات غير المقروءة فقط (لعرض عداد في الـ Navbar)
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    responses:
      200:
        description: العدد
    """
    user_id = int(get_jwt_identity())
    count = notification_service.unread_count(user_id)
    return jsonify({"unread_count": count}), 200


@notifications_bp.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_as_read(notification_id):
    """
    تعليم إشعار واحد كمقروء
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200:
        description: تم التعليم كمقروء
      403:
        description: لا تملك صلاحية الوصول لهذا الإشعار
      404:
        description: الإشعار غير موجود
    """
    user_id = int(get_jwt_identity())
    notification = notification_service.mark_as_read(user_id, notification_id)
    return jsonify({"data": item_schema.dump(notification)}), 200


@notifications_bp.route("/read-all", methods=["PUT"])
@jwt_required()
def mark_all_as_read():
    """
    تعليم كل إشعارات المستخدم كمقروءة
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    responses:
      200:
        description: تم تعليم الكل كمقروء
    """
    user_id = int(get_jwt_identity())
    notification_service.mark_all_as_read(user_id)
    return jsonify({"message": "تم تعليم كل الإشعارات كمقروءة"}), 200


@notifications_bp.route("/<int:notification_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notification_id):
    """
    حذف إشعار
    ---
    tags:
      - Notifications
    security:
      - Bearer: []
    parameters:
      - in: path
        name: notification_id
        type: integer
        required: true
    responses:
      200:
        description: تم الحذف بنجاح
      403:
        description: لا تملك صلاحية الوصول لهذا الإشعار
      404:
        description: الإشعار غير موجود
    """
    user_id = int(get_jwt_identity())
    notification_service.delete(user_id, notification_id)
    return jsonify({"message": "تم حذف الإشعار"}), 200
