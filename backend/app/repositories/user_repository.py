from app.models import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model = User

    def find_by_email(self, email):
        return User.query.filter_by(email=email.lower().strip()).first()

    def find_by_google_id(self, google_id):
        return User.query.filter_by(google_id=google_id).first()

    def email_exists(self, email):
        return self.find_by_email(email) is not None
