"""
مهمة Celery: فحص قوائم المتابعة وتوليد إشعارات تلقائية (كل ساعتين).
"""
import logging
from datetime import datetime, timedelta
from app.extensions import celery, db
from app.models import Watchlist, Price, Notification, NotificationType

logger = logging.getLogger(__name__)

MIN_DROP_PERCENT = 1.0
MIN_NOTIFICATION_INTERVAL_HOURS = 24


@celery.task(name="app.tasks.notification_tasks.task_check_watchlist_and_notify")
def task_check_watchlist_and_notify():
    logger.info("🔔 بدء مهمة فحص قوائم المتابعة...")

    active_watchlist = Watchlist.query.filter_by(is_active=True).all()

    if not active_watchlist:
        logger.info("⚠️  قائمة المتابعة فارغة.")
        return {"status": "skipped"}

    notifications_created = 0

    for entry in active_watchlist:
        try:
            if _check_and_notify(entry):
                notifications_created += 1
        except Exception as e:
            logger.error(f"خطأ في watchlist entry {entry.id}: {e}")

    db.session.commit()
    logger.info(f"✅ إشعارات جديدة: {notifications_created}")
    return {"status": "completed", "notifications_created": notifications_created}


def _check_and_notify(entry):
    product = entry.product
    user = entry.user

    if not product or not user or not user.is_active:
        return False

    best_price = (
        Price.query
        .filter_by(product_id=product.id, in_stock=True)
        .order_by(Price.current_price.asc())
        .first()
    )
    if not best_price:
        return False

    current_price = float(best_price.current_price)

    # تجنّب الإشعارات المتكررة (24 ساعة)
    recent = (
        Notification.query
        .filter_by(user_id=user.id, related_product_id=product.id)
        .order_by(Notification.created_at.desc())
        .first()
    )
    if recent and (datetime.utcnow() - recent.created_at) < timedelta(hours=MIN_NOTIFICATION_INTERVAL_HOURS):
        return False

    notification_type = title = message = None
    store_name = best_price.store.name_ar if best_price.store else "متجر"

    # حالة 1: وصل للسعر المستهدف
    if entry.target_price and current_price <= float(entry.target_price):
        notification_type = NotificationType.TARGET_REACHED
        title = "🎯 وصل السعر للهدف!"
        message = (
            f"'{product.name_ar}' وصل للسعر المستهدف ({entry.target_price})! "
            f"السعر الحالي: {current_price:.2f} في {store_name}."
        )

    # حالة 2: انخفض السعر
    elif entry.notify_on_any_drop and best_price.old_price:
        old = float(best_price.old_price)
        if old > 0:
            drop_pct = ((old - current_price) / old) * 100
            if drop_pct >= MIN_DROP_PERCENT:
                notification_type = NotificationType.PRICE_DROP
                title = f"📉 انخفض السعر {drop_pct:.1f}%!"
                message = (
                    f"'{product.name_ar}' انخفض من {old:.2f} إلى {current_price:.2f} "
                    f"في {store_name} (خصم {drop_pct:.1f}%)."
                )

    if notification_type:
        db.session.add(Notification(
            user_id=user.id,
            type=notification_type,
            title=title,
            message=message,
            is_read=False,
            related_product_id=product.id,
        ))
        logger.info(f"  🔔 {user.email} ← {title}")
        return True

    return False
