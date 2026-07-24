"""
Admin API Endpoints - نسخة محدّثة مع دعم المواصفات وإصلاح الـ Schemas.
"""
import re
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import db
from app.models import (
    Product, User, Notification, Price, Favorite, Watchlist,
    Brand, Category, UserRole, Specification, ProductImage
)
from app.schemas.product_schema import ProductListItemSchema, ProductDetailSchema
from app.schemas.auth_schema import UserResponseSchema
from app.schemas.admin_schema import (
    AdminProductCreateSchema, AdminProductUpdateSchema, AdminUserUpdateSchema
)
from app.utils.admin_required import admin_required
from app.errors.exceptions import NotFoundError

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

product_list_schema = ProductListItemSchema()
product_detail_schema = ProductDetailSchema()
user_schema = UserResponseSchema()
create_schema = AdminProductCreateSchema()
update_schema = AdminProductUpdateSchema()
user_update_schema = AdminUserUpdateSchema()


def _slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"[^\w\-]", "", text)
    return text


# ─── الإحصائيات ─────────────────────────────────────────────────────────────

@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
@admin_required
def get_stats():
    """إحصائيات عامة للوحة التحكم
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: الإحصائيات الكاملة
    """
    stats = {
        "products": {
            "total": Product.query.count(),
            "active": Product.query.filter_by(is_active=True).count(),
            "inactive": Product.query.filter_by(is_active=False).count(),
        },
        "users": {
            "total": User.query.count(),
            "active": User.query.filter_by(is_active=True).count(),
            "admins": User.query.filter_by(role=UserRole.ADMIN).count(),
        },
        "prices": {
            "total": Price.query.count(),
            "in_stock": Price.query.filter_by(in_stock=True).count(),
        },
        "activity": {
            "favorites": Favorite.query.count(),
            "watchlist": Watchlist.query.count(),
            "notifications": Notification.query.count(),
        },
        "brands": Brand.query.count(),
        "categories": Category.query.count(),
    }
    return jsonify({"data": stats}), 200


# ─── إدارة المنتجات ──────────────────────────────────────────────────────────

@admin_bp.route("/products", methods=["GET"])
@jwt_required()
@admin_required
def list_products():
    """قائمة كل المنتجات (بما فيها غير الفعّالة)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: قائمة المنتجات
    """
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)

    q = Product.query.order_by(Product.created_at.desc())
    total = q.count()
    products = q.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        "data": product_list_schema.dump(products, many=True),
        "meta": {"page": page, "per_page": per_page, "total": total}
    }), 200


@admin_bp.route("/products", methods=["POST"])
@jwt_required()
@admin_required
def create_product():
    """إضافة منتج جديد مع مواصفاته
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      201:
        description: تم الإنشاء بنجاح
    """
    data = create_schema.load(request.get_json() or {})

    base_slug = _slugify(data["name_en"])
    slug = base_slug
    counter = 1
    while Product.query.filter_by(slug=slug).first():
        slug = f"{base_slug}-{counter}"
        counter += 1

    product = Product(
        name_ar=data["name_ar"],
        name_en=data["name_en"],
        slug=slug,
        description_ar=data.get("description_ar"),
        description_en=data.get("description_en"),
        model_number=data.get("model_number"),
        brand_id=data["brand_id"],
        category_id=data["category_id"],
        release_date=data.get("release_date"),
        is_active=data.get("is_active", True),
    )
    db.session.add(product)
    db.session.flush()

    # حفظ المواصفات
    _save_specifications(product.id, data.get("specifications", []))

    # حفظ الصورة الرئيسية لو موجودة
    image_url = data.get("image_url")
    if image_url:
        db.session.add(ProductImage(
            product_id=product.id, image_url=image_url, is_primary=True, sort_order=0
        ))

    db.session.commit()
    return jsonify({"data": product_detail_schema.dump(product)}), 201


@admin_bp.route("/products/<int:product_id>", methods=["GET"])
@jwt_required()
@admin_required
def get_product(product_id):
    """جلب تفاصيل منتج واحد (للتعديل)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: تفاصيل المنتج
    """
    product = Product.query.get(product_id)
    if not product:
        raise NotFoundError("المنتج غير موجود")
    return jsonify({"data": product_detail_schema.dump(product)}), 200


@admin_bp.route("/products/<int:product_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_product(product_id):
    """تعديل بيانات منتج مع مواصفاته
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: تم التعديل بنجاح
    """
    product = Product.query.get(product_id)
    if not product:
        raise NotFoundError("المنتج غير موجود")

    data = update_schema.load(request.get_json() or {})

    updatable = ["name_ar", "name_en", "description_ar", "description_en",
                 "model_number", "brand_id", "category_id", "release_date", "is_active"]
    for key in updatable:
        if key in data:
            setattr(product, key, data[key])

    # تحديث المواصفات لو أُرسلت
    if "specifications" in data:
        Specification.query.filter_by(product_id=product.id).delete()
        db.session.flush()
        _save_specifications(product.id, data["specifications"])

    # تحديث الصورة الرئيسية لو أُرسلت
    if "image_url" in data:
        primary = product.images.filter_by(is_primary=True).first()
        if primary:
            primary.image_url = data["image_url"]
        else:
            db.session.add(ProductImage(
                product_id=product.id, image_url=data["image_url"], is_primary=True, sort_order=0
            ))

    db.session.commit()
    return jsonify({"data": product_detail_schema.dump(product)}), 200


@admin_bp.route("/products/<int:product_id>", methods=["DELETE"])
@jwt_required()
@admin_required
def delete_product(product_id):
    """حذف منتج
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: تم الحذف بنجاح
    """
    product = Product.query.get(product_id)
    if not product:
        raise NotFoundError("المنتج غير موجود")
    name = product.name_ar
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"تم حذف '{name}' بنجاح"}), 200


def _save_specifications(product_id, specifications):
    """حفظ قائمة المواصفات لمنتج معيّن."""
    for i, spec in enumerate(specifications):
        if not spec.get("key_ar") or not spec.get("value_ar"):
            continue
        db.session.add(Specification(
            product_id=product_id,
            group_name=spec.get("group_name", "مواصفات عامة"),
            key_ar=spec["key_ar"],
            key_en=spec.get("key_en", spec["key_ar"]),
            value_ar=spec["value_ar"],
            value_en=spec.get("value_en", spec["value_ar"]),
            sort_order=i,
        ))


# ─── إدارة المستخدمين ────────────────────────────────────────────────────────

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def list_users():
    """قائمة كل المستخدمين
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: قائمة المستخدمين
    """
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 20)), 1), 100)

    q = User.query.order_by(User.created_at.desc())
    total = q.count()
    users = q.offset((page - 1) * per_page).limit(per_page).all()

    return jsonify({
        "data": user_schema.dump(users, many=True),
        "meta": {"page": page, "per_page": per_page, "total": total}
    }), 200


@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
@admin_required
def update_user(user_id):
    """تعديل مستخدم (تفعيل/تعطيل أو تغيير الدور)
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: تم التعديل بنجاح
    """
    user = User.query.get(user_id)
    if not user:
        raise NotFoundError("المستخدم غير موجود")

    data = user_update_schema.load(request.get_json() or {})

    if "is_active" in data:
        user.is_active = data["is_active"]
    if "role" in data:
        user.role = UserRole.ADMIN if data["role"] == "admin" else UserRole.USER

    db.session.commit()
    return jsonify({"data": user_schema.dump(user)}), 200


# ─── تشغيل المهام يدوياً ─────────────────────────────────────────────────────

@admin_bp.route("/tasks/run-predictions", methods=["POST"])
@jwt_required()
@admin_required
def run_predictions_task():
    """تشغيل مهمة تحديث التوقعات يدوياً
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: تم الإرسال
    """
    from app.tasks.prediction_tasks import task_update_all_predictions
    task = task_update_all_predictions.delay()
    return jsonify({"message": "تم إرسال مهمة التوقعات", "task_id": task.id}), 200


@admin_bp.route("/tasks/run-notifications", methods=["POST"])
@jwt_required()
@admin_required
def run_notifications_task():
    """تشغيل مهمة فحص الإشعارات يدوياً
    ---
    tags:
      - Admin
    security:
      - Bearer: []
    responses:
      200:
        description: تم الإرسال
    """
    from app.tasks.notification_tasks import task_check_watchlist_and_notify
    task = task_check_watchlist_and_notify.delay()
    return jsonify({"message": "تم إرسال مهمة الإشعارات", "task_id": task.id}), 200
