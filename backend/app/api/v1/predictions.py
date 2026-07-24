"""
Predictions API Endpoints:
    GET  /api/v1/products/<product_id>/prediction  - جلب التوصية لمنتج معيّن
    POST /api/v1/products/<product_id>/prediction/analyze - تشغيل التحليل الآن
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.prediction_service import PredictionService
from app.schemas.prediction_schema import PredictionSchema
from app.models import UserRole

predictions_bp = Blueprint("predictions", __name__, url_prefix="/api/v1/products")

prediction_service = PredictionService()
prediction_schema = PredictionSchema()


@predictions_bp.route("/<int:product_id>/prediction", methods=["GET"])
def get_prediction(product_id):
    """
    جلب آخر توصية محفوظة لمنتج معيّن
    ---
    tags:
      - Predictions
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
    responses:
      200:
        description: التوصية (recommendation, label_ar, icon, color, reason_ar, confidence_score)
      204:
        description: لا توجد توصية محفوظة بعد (بيانات غير كافية)
    """
    prediction = prediction_service.get_for_product(product_id)
    if not prediction:
        return jsonify({"data": None, "message": "لا توجد بيانات تاريخية كافية لتقديم توصية حاليًا"}), 200

    return jsonify({"data": prediction_schema.dump(prediction)}), 200


@predictions_bp.route("/<int:product_id>/prediction/analyze", methods=["POST"])
@jwt_required()
def run_analysis(product_id):
    """
    تشغيل التحليل يدويًا لمنتج معيّن (للمشرفين فقط في الوضع الحالي)
    ---
    tags:
      - Predictions
    security:
      - Bearer: []
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
    responses:
      200:
        description: تم التحليل وحُفظت النتيجة
      204:
        description: بيانات غير كافية
    """
    from app.models import User
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user or user.role != UserRole.ADMIN:
        from app.errors.exceptions import ForbiddenError
        raise ForbiddenError("هذا الإجراء متاح للمشرفين فقط")

    prediction = prediction_service.analyze_and_save(product_id)
    if not prediction:
        return jsonify({"data": None, "message": "بيانات غير كافية لإجراء التحليل"}), 200

    return jsonify({"data": prediction_schema.dump(prediction)}), 200
