from app.extensions import db
from app.models.base import BaseModel


class PriceHistory(BaseModel):
    """
    سجل تاريخي لكل تغيير في سعر منتج معيّن داخل متجر معيّن.
    هذا الجدول هو أساس الرسم البياني للأسعار ونظام الذكاء الاصطناعي (Prediction).
    """
    __tablename__ = "price_history"

    price_id = db.Column(db.Integer, db.ForeignKey("prices.id"), nullable=False, index=True)
    recorded_price = db.Column(db.Numeric(12, 2), nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False, index=True)

    price = db.relationship("Price", back_populates="history")

    def __repr__(self):
        return f"<PriceHistory price_id={self.price_id} {self.recorded_price} @ {self.recorded_at}>"
