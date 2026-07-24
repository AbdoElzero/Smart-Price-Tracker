"""
conftest.py — إعداد بيئة الاختبار المشتركة.

الإصلاح الرئيسي: استخدام StaticPool من SQLAlchemy لضمان أن كل الطلبات
في الـ test client تستخدم نفس قاعدة البيانات in-memory.
بدون StaticPool، كل request يفتح connection جديد ويحصل على قاعدة بيانات فارغة.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from app import create_app
from app.extensions import db as _db
from app.models import (
    User, UserRole, Currency, Country, Category, Brand, Product
)
from app.utils.security import hash_password


@pytest.fixture(scope="session")
def app():
    """
    ينشئ تطبيق Flask واحد لكل جلسة اختبار.
    يستخدم SQLite in-memory مع StaticPool لضمان مشاركة
    نفس الـ connection بين التطبيق وكل طلبات الـ test client.
    """
    flask_app = create_app("testing")

    # ← الإصلاح الجوهري: StaticPool يضمن connection واحد مشترك
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    flask_app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "connect_args": {"check_same_thread": False},
        "poolclass": StaticPool,
    }

    with flask_app.app_context():
        _db.create_all()
        _seed_basic_data()
        yield flask_app
        _db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """عميل HTTP لاختبار الـ API endpoints."""
    with app.test_client() as c:
        yield c


@pytest.fixture(scope="function")
def db(app):
    """جلسة قاعدة بيانات نظيفة لكل اختبار."""
    with app.app_context():
        yield _db
        _db.session.rollback()


@pytest.fixture(scope="function")
def regular_user(db):
    """مستخدم عادي جاهز للاختبار."""
    user = User(
        name="أحمد محمد",
        email="ahmed_test@example.com",
        password_hash=hash_password("TestPass123"),
        role=UserRole.USER,
        is_active=True,
        is_verified=True,
    )
    db.session.add(user)
    db.session.commit()
    yield user
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture(scope="function")
def admin_user(db):
    """مستخدم مشرف جاهز للاختبار."""
    user = User(
        name="مدير النظام",
        email="admin_test@example.com",
        password_hash=hash_password("AdminPass123"),
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True,
    )
    db.session.add(user)
    db.session.commit()
    yield user
    try:
        db.session.delete(user)
        db.session.commit()
    except Exception:
        db.session.rollback()


@pytest.fixture(scope="function")
def auth_headers(client, regular_user):
    """JWT headers للمستخدم العادي."""
    response = client.post("/api/v1/auth/login", json={
        "email": "ahmed_test@example.com",
        "password": "TestPass123",
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="function")
def admin_headers(client, admin_user):
    """JWT headers للمشرف."""
    response = client.post("/api/v1/auth/login", json={
        "email": "admin_test@example.com",
        "password": "AdminPass123",
    })
    token = response.json["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _seed_basic_data():
    """
    بيانات أساسية مشتركة بين الاختبارات.
    تُنشأ مرة واحدة لكل جلسة اختبار.
    """
    # عملة
    currency = Currency(
        code="EGP",
        name_ar="جنيه مصري",
        name_en="Egyptian Pound",
        symbol="ج.م",
        exchange_rate_to_usd=49.0,
    )
    _db.session.add(currency)
    _db.session.flush()

    # دولة
    country = Country(
        code="EG",
        name_ar="مصر",
        name_en="Egypt",
        flag_emoji="🇪🇬",
        currency_id=currency.id,
    )
    _db.session.add(country)

    # تصنيف
    category = Category(
        name_ar="هواتف",
        name_en="Phones",
        slug="phones-test",
    )
    _db.session.add(category)

    # علامة تجارية
    brand = Brand(
        name_ar="سامسونج",
        name_en="Samsung",
        slug="samsung-test",
    )
    _db.session.add(brand)
    _db.session.flush()

    # منتج
    product = Product(
        name_ar="جالكسي S24",
        name_en="Galaxy S24",
        slug="galaxy-s24-test",
        brand_id=brand.id,
        category_id=category.id,
        is_active=True,
    )
    _db.session.add(product)
    _db.session.commit()
