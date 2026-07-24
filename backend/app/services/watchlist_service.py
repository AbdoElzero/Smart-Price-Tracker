from app.repositories.watchlist_repository import WatchlistRepository
from app.repositories.product_repository import ProductRepository
from app.errors.exceptions import NotFoundError


class WatchlistService:
    def __init__(self):
        self.watchlist_repo = WatchlistRepository()
        self.product_repo = ProductRepository()

    def list_for_user(self, user_id):
        return self.watchlist_repo.list_for_user(user_id)

    def add_or_update(self, user_id, product_id, data):
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise NotFoundError("المنتج غير موجود")

        target_price = data.get("target_price")
        notify_on_any_drop = data.get("notify_on_any_drop", True)

        existing = self.watchlist_repo.find(user_id, product_id)
        if existing:
            return self.watchlist_repo.update(
                existing,
                target_price=target_price,
                notify_on_any_drop=notify_on_any_drop,
                is_active=True,
            )

        return self.watchlist_repo.create(
            user_id=user_id,
            product_id=product_id,
            target_price=target_price,
            notify_on_any_drop=notify_on_any_drop,
        )

    def remove(self, user_id, product_id):
        existing = self.watchlist_repo.find(user_id, product_id)
        if not existing:
            raise NotFoundError("هذا المنتج غير موجود في قائمة متابعتك")
        self.watchlist_repo.delete(existing)
