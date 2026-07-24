from app.extensions import db
from app.models.base import BaseModel


class Favorite(BaseModel):
    __tablename__ = "favorites"
    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="uq_favorite_user_product"),
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    user = db.relationship("User", back_populates="favorites")
    product = db.relationship("Product", back_populates="favorites")

    def __repr__(self):
        return f"<Favorite user_id={self.user_id} product_id={self.product_id}>"
