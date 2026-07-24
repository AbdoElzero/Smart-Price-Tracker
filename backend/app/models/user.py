import enum
from app.extensions import db
from app.models.base import BaseModel


class UserRole(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)  # nullable لحسابات Google فقط
    google_id = db.Column(db.String(255), unique=True, nullable=True, index=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    role = db.Column(db.Enum(UserRole), default=UserRole.USER, nullable=False)
    preferred_country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)

    preferred_country = db.relationship("Country", back_populates="users")

    reviews = db.relationship(
        "Review", back_populates="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    favorites = db.relationship(
        "Favorite", back_populates="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    watchlist_entries = db.relationship(
        "Watchlist", back_populates="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    notifications = db.relationship(
        "Notification", back_populates="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.email}>"
