"""
مهمة Celery: تحديث الأسعار الدورية (كل ساعة).
تدور على المتاجر المفعَّلة للـ Scraping وتُحدّث الأسعار في قاعدة البيانات.
"""
import logging
from datetime import datetime
from app.extensions import celery, db
from app.models import Store, Price, PriceHistory

logger = logging.getLogger(__name__)


@celery.task(name="app.tasks.price_tasks.task_check_all_prices", bind=True, max_retries=2)
def task_check_all_prices(self):
    logger.info("🔄 بدء مهمة تحديث الأسعار...")

    enabled_stores = Store.query.filter_by(is_scraping_enabled=True, is_active=True).all()

    if not enabled_stores:
        logger.info("⚠️  لا توجد متاجر مفعَّلة للـ Scraping حاليًا.")
        return {"status": "skipped", "reason": "no_enabled_stores"}

    updated_count = 0
    errors = []

    for store in enabled_stores:
        try:
            count = _process_store(store)
            updated_count += count
            logger.info(f"✅ {store.name_ar}: تم تحديث {count} سعر")
        except Exception as e:
            errors.append({"store": store.slug, "error": str(e)})
            logger.error(f"❌ {store.name_ar}: {e}")

    if updated_count > 0:
        task_trigger_post_price_update.delay()

    return {
        "status": "completed",
        "updated_prices": updated_count,
        "stores_processed": len(enabled_stores),
        "errors": errors,
        "timestamp": datetime.utcnow().isoformat(),
    }


def _process_store(store):
    from app.scrapers import get_scraper
    scraper = get_scraper(store.slug)
    if not scraper:
        logger.warning(f"⚠️  لا يوجد Scraper للمتجر: {store.slug}")
        return 0

    prices_data = scraper.fetch_prices()
    count = 0

    for item in prices_data:
        price_record = Price.query.filter_by(
            product_id=item["product_id"],
            store_id=store.id,
            country_id=item["country_id"],
        ).first()

        if price_record and float(price_record.current_price) != float(item["price"]):
            db.session.add(PriceHistory(
                price_id=price_record.id,
                recorded_price=price_record.current_price,
                recorded_at=datetime.utcnow(),
            ))
            price_record.old_price = price_record.current_price
            price_record.current_price = item["price"]
            price_record.in_stock = item.get("in_stock", True)
            price_record.last_checked_at = datetime.utcnow()
            count += 1

    db.session.commit()
    return count


@celery.task(name="app.tasks.price_tasks.task_trigger_post_price_update")
def task_trigger_post_price_update():
    """تُشغَّل تلقائيًا بعد أي تحديث في الأسعار."""
    from app.tasks.prediction_tasks import task_update_all_predictions
    task_update_all_predictions.delay()
