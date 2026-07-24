from app.extensions import db
from app.models.base import BaseModel


class Watchlist(BaseModel):
    __tablename__ = "watchlist"
    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="uq_watchlist_user_product"),
    )

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    target_price = db.Column(db.Numeric(12, 2), nullable=True)
    notify_on_any_drop = db.Column(db.Boolean, default=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    user = db.relationship("User", back_populates="watchlist_entries")
    product = db.relationship("Product", back_populates="watchlist_entries")

    def __repr__(self):
        return f"<Watchlist user_id={self.user_id} product_id={self.product_id}>"
