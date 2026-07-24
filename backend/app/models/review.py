from app.extensions import db
from app.models.base import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"
    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="uq_review_user_product"),
    )

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rating = db.Column(db.SmallInteger, nullable=False)  # من 1 إلى 5
    comment = db.Column(db.Text, nullable=True)
    is_approved = db.Column(db.Boolean, default=True, nullable=False)

    product = db.relationship("Product", back_populates="reviews")
    user = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return f"<Review user_id={self.user_id} product_id={self.product_id} rating={self.rating}>"
