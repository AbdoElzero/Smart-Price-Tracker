import enum
from app.extensions import db
from app.models.base import BaseModel


class RecommendationType(enum.Enum):
    BUY_NOW = "buy_now"
    WAIT = "wait"
    HIGH_PRICE = "high_price"


class Prediction(BaseModel):
    """
    نتيجة تحليل الذكاء الاصطناعي (الإحصائي) لمنتج معيّن في وقت معيّن.
    يُحدَّث بشكل دوري (Celery Task) بناءً على بيانات PriceHistory.
    """
    __tablename__ = "predictions"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    recommendation = db.Column(db.Enum(RecommendationType), nullable=False)
    confidence_score = db.Column(db.Numeric(5, 2), nullable=False)  # نسبة من 0 إلى 100
    reason_ar = db.Column(db.Text, nullable=False)
    reason_en = db.Column(db.Text, nullable=False)
    based_on_days = db.Column(db.Integer, nullable=False, default=90)
    analyzed_at = db.Column(db.DateTime, nullable=False)

    product = db.relationship("Product", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction product_id={self.product_id} {self.recommendation}>"
