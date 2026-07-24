from app.extensions import db
from app.models.base import BaseModel


class Currency(BaseModel):
    __tablename__ = "currencies"

    code = db.Column(db.String(3), unique=True, nullable=False, index=True)  # SAR, EGP, AED...
    name_ar = db.Column(db.String(50), nullable=False)
    name_en = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    exchange_rate_to_usd = db.Column(db.Numeric(14, 6), nullable=False, default=1.0)

    countries = db.relationship("Country", back_populates="currency", lazy="dynamic")
    prices = db.relationship("Price", back_populates="currency", lazy="dynamic")

    def __repr__(self):
        return f"<Currency {self.code}>"
