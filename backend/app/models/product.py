from app.extensions import db
from app.models.base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    name_ar = db.Column(db.String(255), nullable=False)
    name_en = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description_ar = db.Column(db.Text, nullable=True)
    description_en = db.Column(db.Text, nullable=True)
    model_number = db.Column(db.String(150), nullable=True, index=True)
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    release_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    brand = db.relationship("Brand", back_populates="products")
    category = db.relationship("Category", back_populates="products")

    images = db.relationship(
        "ProductImage", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )
    specifications = db.relationship(
        "Specification", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )
    prices = db.relationship(
        "Price", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )
    reviews = db.relationship(
        "Review", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )
    favorites = db.relationship(
        "Favorite", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )
    watchlist_entries = db.relationship(
        "Watchlist", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )
    predictions = db.relationship(
        "Prediction", back_populates="product", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Product {self.slug}>"
