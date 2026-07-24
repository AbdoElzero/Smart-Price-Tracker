"""
Application Factory الرئيسي لـ Flask.
"""
import os
from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors, swagger, limiter, celery
from app.errors.handlers import register_error_handlers


def create_app(config_name=None):
    config_name = config_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config.get("FRONTEND_URL", "*")}})
    swagger.init_app(app)
    limiter.init_app(app)

    _configure_celery(app)

    os.makedirs(app.config["UPLOAD_FOLDER"] = '/tmp/uploads/avatars' )

    from app import models  # noqa: F401
    from app.utils import jwt_callbacks  # noqa: F401

    register_error_handlers(app)

    from app.api.v1.auth import auth_bp
    from app.api.v1.products import products_bp
    from app.api.v1.catalog import catalog_bp
    from app.api.v1.favorites import favorites_bp
    from app.api.v1.profile import profile_bp
    from app.api.v1.watchlist import watchlist_bp
    from app.api.v1.notifications import notifications_bp
    from app.api.v1.predictions import predictions_bp
    from app.api.v1.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(catalog_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(watchlist_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(admin_bp)

    @app.route("/health")
    def health_check():
        return jsonify({"status": "ok", "service": "smart-price-tracker-backend"})

    return app


def _configure_celery(app):
    celery.config_from_object({
        "broker_url": app.config.get("CELERY_BROKER_URL", "redis://localhost:6379/1"),
        "result_backend": app.config.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2"),
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
        "timezone": "Africa/Cairo",
        "enable_utc": True,
        "beat_schedule": {
            "check-prices-every-hour": {
                "task": "app.tasks.price_tasks.task_check_all_prices",
                "schedule": 3600.0,
            },
            "update-predictions-every-6-hours": {
                "task": "app.tasks.prediction_tasks.task_update_all_predictions",
                "schedule": 21600.0,
            },
            "check-watchlist-notifications-every-2-hours": {
                "task": "app.tasks.notification_tasks.task_check_watchlist_and_notify",
                "schedule": 7200.0,
            },
        },
    })

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
