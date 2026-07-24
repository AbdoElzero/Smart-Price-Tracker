"""
سكريبت اختياري لإضافة إشعارات تجريبية (Demo Notifications) لأول مستخدم مسجَّل،
لأغراض اختبار واجهة الإشعارات فقط.

⚠️ هذه الإشعارات تجريبية بالكامل (مذكور ذلك صراحة في نص كل إشعار)، وليست نتيجة
فحص أسعار حقيقي. الإشعارات الحقيقية ستُولَّد تلقائيًا لاحقًا من نظام Celery
الذي يفحص الأسعار بشكل دوري ويقارنها بقائمة المتابعة لكل مستخدم.

التشغيل (اختياري):
    python seed_notifications.py
"""
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import User, Notification, NotificationType


def run():
    app = create_app()
    with app.app_context():
        user = User.query.order_by(User.id.asc()).first()
        if not user:
            print("⚠️  لا يوجد أي مستخدم مسجَّل بعد. سجّل حساب أولاً ثم أعد تشغيل هذا السكريبت.")
            return

        print(f"🌱 إضافة إشعارات تجريبية للمستخدم: {user.email}")

        demo_notifications = [
            {
                "type": NotificationType.PRICE_DROP,
                "title": "انخفض السعر! 📉",
                "message": "[تجريبي] انخفض سعر منتج في قائمة متابعتك بنسبة 12%.",
                "is_read": False,
                "minutes_ago": 5,
            },
            {
                "type": NotificationType.TARGET_REACHED,
                "title": "وصل للسعر المستهدف 🎯",
                "message": "[تجريبي] وصل أحد المنتجات إلى السعر المستهدف الذي حدّدته.",
                "is_read": False,
                "minutes_ago": 120,
            },
            {
                "type": NotificationType.BACK_IN_STOCK,
                "title": "عاد للتوفر ✅",
                "message": "[تجريبي] أحد المنتجات في مفضلتك أصبح متوفرًا من جديد.",
                "is_read": True,
                "minutes_ago": 1440,
            },
            {
                "type": NotificationType.SYSTEM,
                "title": "مرحبًا بك في Smart Price Tracker 👋",
                "message": "[تجريبي] شكرًا لانضمامك، ابدأ بمتابعة منتجاتك المفضّلة الآن.",
                "is_read": True,
                "minutes_ago": 4320,
            },
        ]

        for item in demo_notifications:
            notif = Notification(
                user_id=user.id,
                type=item["type"],
                title=item["title"],
                message=item["message"],
                is_read=item["is_read"],
                created_at=datetime.utcnow() - timedelta(minutes=item["minutes_ago"]),
            )
            db.session.add(notif)

        db.session.commit()
        print("🎉 تمت إضافة 4 إشعارات تجريبية بنجاح!")


if __name__ == "__main__":
    run()
