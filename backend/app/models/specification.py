from app.extensions import db
from app.models.base import BaseModel


class Specification(BaseModel):
    __tablename__ = "specifications"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    group_name = db.Column(db.String(100), nullable=False)  # مثال: "المعالج", "الشاشة", "الذاكرة"
    key_ar = db.Column(db.String(150), nullable=False)
    key_en = db.Column(db.String(150), nullable=False)
    value_ar = db.Column(db.String(500), nullable=False)
    value_en = db.Column(db.String(500), nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    product = db.relationship("Product", back_populates="specifications")

    def __repr__(self):
        return f"<Specification {self.key_en} product_id={self.product_id}>"
