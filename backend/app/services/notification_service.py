import math
from app.repositories.notification_repository import NotificationRepository
from app.errors.exceptions import NotFoundError, ForbiddenError


class NotificationService:
    def __init__(self):
        self.notification_repo = NotificationRepository()

    def list_for_user(self, user_id, page=1, per_page=20):
        items, total = self.notification_repo.list_for_user(user_id, page, per_page)
        unread_count = self.notification_repo.unread_count(user_id)
        meta = {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": math.ceil(total / per_page) if total else 0,
            "unread_count": unread_count,
        }
        return items, meta

    def unread_count(self, user_id):
        return self.notification_repo.unread_count(user_id)

    def mark_as_read(self, user_id, notification_id):
        notification = self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise NotFoundError("الإشعار غير موجود")
        if notification.user_id != user_id:
            raise ForbiddenError("لا تملك صلاحية الوصول لهذا الإشعار")
        return self.notification_repo.update(notification, is_read=True)

    def mark_all_as_read(self, user_id):
        self.notification_repo.mark_all_read(user_id)

    def delete(self, user_id, notification_id):
        notification = self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise NotFoundError("الإشعار غير موجود")
        if notification.user_id != user_id:
            raise ForbiddenError("لا تملك صلاحية الوصول لهذا الإشعار")
        self.notification_repo.delete(notification)
