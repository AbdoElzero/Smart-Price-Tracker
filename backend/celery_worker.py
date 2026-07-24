"""
نقطة تشغيل Celery Worker و Celery Beat.

⚠️ على Windows (مع Memurai) يجب استخدام --pool=solo:

    # نافذة PowerShell 3 (Worker):
    celery -A celery_worker.celery worker --loglevel=info --pool=solo

    # نافذة PowerShell 4 (Beat - الجدول الدوري):
    celery -A celery_worker.celery beat --loglevel=info
"""
from app import create_app
from app.extensions import celery

flask_app = create_app()
flask_app.app_context().push()

# استيراد المهام ليتعرف عليها Celery
import app.tasks.price_tasks       # noqa: F401
import app.tasks.prediction_tasks  # noqa: F401
import app.tasks.notification_tasks  # noqa: F401
