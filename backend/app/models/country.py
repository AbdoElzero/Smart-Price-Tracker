from app.extensions import db
from app.models.base import BaseModel


class Country(BaseModel):
    __tablename__ = "countries"

    code = db.Column(db.String(2), unique=True, nullable=False, index=True)  # ISO 3166-1: SA, EG, AE...
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    flag_emoji = db.Column(db.String(10), nullable=True)
    currency_id = db.Column(db.Integer, db.ForeignKey("currencies.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    currency = db.relationship("Currency", back_populates="countries")
    stores = db.relationship("Store", back_populates="country", lazy="dynamic")
    prices = db.relationship("Price", back_populates="country", lazy="dynamic")
    users = db.relationship("User", back_populates="preferred_country", lazy="dynamic")

    def __repr__(self):
        return f"<Country {self.code}>"
