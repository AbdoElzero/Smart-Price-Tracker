from app.extensions import db
from app.models.base import BaseModel


class Price(BaseModel):
    """
    السعر الحالي لمنتج معيّن في متجر معيّن وفي دولة معيّنة.
    تاريخ تغيّر هذا السعر يُسجَّل في جدول PriceHistory.
    """
    __tablename__ = "prices"
    __table_args__ = (
        db.UniqueConstraint(
            "product_id", "store_id", "country_id", name="uq_price_product_store_country"
        ),
    )

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=False)

    current_price = db.Column(db.Numeric(12, 2), nullable=False)
    old_price = db.Column(db.Numeric(12, 2), nullable=True)
    in_stock = db.Column(db.Boolean, default=True, nullable=False)
    product_url = db.Column(db.String(1000), nullable=False)
    last_checked_at = db.Column(db.DateTime, nullable=True)

    product = db.relationship("Product", back_populates="prices")
    store = db.relationship("Store", back_populates="prices")
    country = db.relationship("Country", back_populates="prices")
    currency = db.relationship("Currency", back_populates="prices")
    history = db.relationship(
        "PriceHistory", back_populates="price", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Price product_id={self.product_id} store_id={self.store_id} {self.current_price}>"
