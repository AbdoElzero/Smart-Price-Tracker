"""
تجميع كل الموديلات في مكان واحد لسهولة الاستيراد:
    from app.models import Product, User, ...

هذا الملف أيضًا ضروري حتى يتعرّف Flask-Migrate على كل الجداول.
"""
from app.models.base import BaseModel
from app.models.currency import Currency
from app.models.country import Country
from app.models.category import Category
from app.models.brand import Brand
from app.models.store import Store
from app.models.product import Product
from app.models.product_image import ProductImage
from app.models.specification import Specification
from app.models.price import Price
from app.models.price_history import PriceHistory
from app.models.user import User, UserRole
from app.models.review import Review
from app.models.favorite import Favorite
from app.models.watchlist import Watchlist
from app.models.notification import Notification, NotificationType
from app.models.prediction import Prediction, RecommendationType

__all__ = [
    "BaseModel",
    "Currency",
    "Country",
    "Category",
    "Brand",
    "Store",
    "Product",
    "ProductImage",
    "Specification",
    "Price",
    "PriceHistory",
    "User",
    "UserRole",
    "Review",
    "Favorite",
    "Watchlist",
    "Notification",
    "NotificationType",
    "Prediction",
    "RecommendationType",
]
