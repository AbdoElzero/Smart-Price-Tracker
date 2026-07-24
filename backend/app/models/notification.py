import enum
from app.extensions import db
from app.models.base import BaseModel


class NotificationType(enum.Enum):
    PRICE_DROP = "price_drop"
    TARGET_REACHED = "target_reached"
    BACK_IN_STOCK = "back_in_stock"
    SYSTEM = "system"


class Notification(BaseModel):
    __tablename__ = "notifications"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    type = db.Column(db.Enum(NotificationType), nullable=False, default=NotificationType.SYSTEM)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    related_product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)

    user = db.relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification user_id={self.user_id} type={self.type}>"
