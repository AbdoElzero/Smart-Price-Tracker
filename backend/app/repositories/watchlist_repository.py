from app.models import Watchlist
from app.repositories.base_repository import BaseRepository


class WatchlistRepository(BaseRepository):
    model = Watchlist

    def find(self, user_id, product_id):
        return Watchlist.query.filter_by(user_id=user_id, product_id=product_id).first()

    def list_for_user(self, user_id):
        return (
            Watchlist.query.filter_by(user_id=user_id, is_active=True)
            .order_by(Watchlist.created_at.desc())
            .all()
        )
