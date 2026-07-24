from app.extensions import db
from app.models.base import BaseModel


class Store(BaseModel):
    __tablename__ = "stores"

    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    logo_url = db.Column(db.String(500), nullable=True)
    website_url = db.Column(db.String(500), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)

    # يُفعَّل فقط بعد مراجعة شروط الاستخدام (ToS) الخاصة بكل متجر على حدة
    is_scraping_enabled = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    country = db.relationship("Country", back_populates="stores")
    prices = db.relationship("Price", back_populates="store", lazy="dynamic")

    def __repr__(self):
        return f"<Store {self.slug}>"
