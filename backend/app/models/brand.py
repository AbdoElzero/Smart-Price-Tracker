from app.extensions import db
from app.models.base import BaseModel


class Brand(BaseModel):
    __tablename__ = "brands"

    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    logo_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    products = db.relationship("Product", back_populates="brand", lazy="dynamic")

    def __repr__(self):
        return f"<Brand {self.slug}>"
