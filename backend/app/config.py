"""
إعدادات التطبيق بحسب البيئة (Development / Testing / Production).
"""
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SWAGGER_CONFIG = {
    "title": "Smart Price Tracker API",
    "uiversion": 3,
    "specs_route": "/api/v1/docs/",
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/api/v1/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
}


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES", 2592000))
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"

    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

    SWAGGER = SWAGGER_CONFIG

    UPLOAD_FOLDER = os.path.join('/tmp/uploads/avatars')
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_AVATAR_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Rate Limiting
    RATELIMIT_DEFAULT = "500 per minute"  # ← مرتفع كافٍ للتطوير

    DEBUG = os.environ.get("DEBUG", "False") == "True"


class DevelopmentConfig(Config):
    DEBUG = True
    # في بيئة التطوير: نرفع الحد أكثر لتجنّب 429 عند الاختبار السريع
    RATELIMIT_DEFAULT = "1000 per minute"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL", "sqlite:///:memory:")
    RATELIMIT_ENABLED = False  # تعطيل Rate Limit في الاختبارات تمامًا


class ProductionConfig(Config):
    DEBUG = False
    RATELIMIT_DEFAULT = "200 per minute"  # أكثر صرامة في الإنتاج


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
