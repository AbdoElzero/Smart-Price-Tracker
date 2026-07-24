from app.extensions import db
from app.models import Notification
from app.repositories.base_repository import BaseRepository


class NotificationRepository(BaseRepository):
    model = Notification

    def list_for_user(self, user_id, page=1, per_page=20):
        q = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc())
        total = q.count()
        items = q.offset((page - 1) * per_page).limit(per_page).all()
        return items, total

    def unread_count(self, user_id):
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()

    def mark_all_read(self, user_id):
        Notification.query.filter_by(user_id=user_id, is_read=False).update({"is_read": True})
        db.session.commit()
