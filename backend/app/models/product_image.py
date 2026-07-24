from app.extensions import db
from app.models.base import BaseModel


class ProductImage(BaseModel):
    __tablename__ = "product_images"

    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False, nullable=False)
    sort_order = db.Column(db.Integer, default=0, nullable=False)

    product = db.relationship("Product", back_populates="images")

    def __repr__(self):
        return f"<ProductImage product_id={self.product_id}>"
