"""
مهمة Celery: تحديث توقعات الذكاء الاصطناعي (كل 6 ساعات).
"""
import logging
from app.extensions import celery
from app.models import Product

logger = logging.getLogger(__name__)


@celery.task(name="app.tasks.prediction_tasks.task_update_all_predictions")
def task_update_all_predictions():
    logger.info("🧠 بدء مهمة تحديث التوقعات...")

    from app.services.prediction_service import PredictionService
    prediction_service = PredictionService()

    products = Product.query.filter_by(is_active=True).all()
    updated = skipped = 0
    errors = []

    for product in products:
        try:
            result = prediction_service.analyze_and_save(product.id)
            if result:
                updated += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append(product.id)
            logger.error(f"  ❌ {product.name_ar}: {e}")

    logger.info(f"✅ التوقعات: {updated} مُحدَّث، {skipped} متجاوز، {len(errors)} خطأ")

    if updated > 0:
        from app.tasks.notification_tasks import task_check_watchlist_and_notify
        task_check_watchlist_and_notify.delay()

    return {"status": "completed", "updated": updated, "skipped": skipped}


@celery.task(name="app.tasks.prediction_tasks.task_update_single_product_prediction")
def task_update_single_product_prediction(product_id):
    from app.services.prediction_service import PredictionService
    try:
        result = PredictionService().analyze_and_save(product_id)
        return {"status": "ok", "product_id": product_id,
                "recommendation": result.recommendation.value if result else None}
    except Exception as e:
        return {"status": "error", "product_id": product_id, "error": str(e)}
