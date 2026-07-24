from app.repositories.favorite_repository import FavoriteRepository
from app.repositories.product_repository import ProductRepository
from app.errors.exceptions import NotFoundError


class FavoriteService:
    def __init__(self):
        self.favorite_repo = FavoriteRepository()
        self.product_repo = ProductRepository()

    def list_favorites(self, user_id):
        favorites = self.favorite_repo.list_for_user(user_id)
        return [f.product for f in favorites]

    def list_favorite_ids(self, user_id):
        return self.favorite_repo.list_ids_for_user(user_id)

    def toggle(self, user_id, product_id):
        """يضيف المنتج للمفضلة لو غير موجود، أو يحذفه لو موجود (Toggle).
        يرجع True لو تمت الإضافة، False لو تمت الإزالة."""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("المنتج غير موجود")

        existing = self.favorite_repo.find(user_id, product_id)
        if existing:
            self.favorite_repo.delete(existing)
            return False

        self.favorite_repo.create(user_id=user_id, product_id=product_id)
        return True
