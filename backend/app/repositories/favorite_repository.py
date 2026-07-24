from app.models import Favorite
from app.repositories.base_repository import BaseRepository


class FavoriteRepository(BaseRepository):
    model = Favorite

    def find(self, user_id, product_id):
        return Favorite.query.filter_by(user_id=user_id, product_id=product_id).first()

    def list_for_user(self, user_id):
        return Favorite.query.filter_by(user_id=user_id).order_by(Favorite.created_at.desc()).all()

    def list_ids_for_user(self, user_id):
        rows = Favorite.query.filter_by(user_id=user_id).with_entities(Favorite.product_id).all()
        return [row[0] for row in rows]
