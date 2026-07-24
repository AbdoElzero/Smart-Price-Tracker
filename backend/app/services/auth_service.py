"""
Service Layer لكل منطق Authentication.
هذا الكلاس لا يتعامل مباشرة مع قاعدة البيانات (هذا عمل Repository)،
ولا يتعامل مع HTTP request/response (هذا عمل Blueprint/Route).
"""
import os
from flask_jwt_extended import create_access_token, create_refresh_token
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests

from app.repositories.user_repository import UserRepository
from app.errors.exceptions import ConflictError, AuthError
from app.utils.security import hash_password, verify_password
from app.models import UserRole


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, data):
        email = data["email"].lower().strip()
        if self.user_repo.email_exists(email):
            raise ConflictError("هذا البريد الإلكتروني مستخدم مسبقًا")

        user = self.user_repo.create(
            name=data["name"].strip(),
            email=email,
            password_hash=hash_password(data["password"]),
            preferred_country_id=data.get("preferred_country_id"),
            role=UserRole.USER,
        )
        return self._build_tokens(user), user

    def login(self, data):
        email = data["email"].lower().strip()
        user = self.user_repo.find_by_email(email)

        if not user or not verify_password(data["password"], user.password_hash):
            raise AuthError("البريد الإلكتروني أو كلمة السر غير صحيحة")

        if not user.is_active:
            raise AuthError("هذا الحساب مُعطَّل، يرجى التواصل مع الدعم")

        return self._build_tokens(user), user

    def login_with_google(self, id_token_str):
        try:
            client_id = os.environ.get("GOOGLE_CLIENT_ID")
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), client_id
            )
        except ValueError:
            raise AuthError("رمز تسجيل الدخول عبر Google غير صالح")

        google_id = idinfo["sub"]
        email = idinfo.get("email", "").lower().strip()
        name = idinfo.get("name") or (email.split("@")[0] if email else "مستخدم Google")
        avatar_url = idinfo.get("picture")

        user = self.user_repo.find_by_google_id(google_id)

        if not user:
            user = self.user_repo.find_by_email(email)
            if user:
                # حساب موجود بنفس البريد لكن بدون ربط Google - نربطه الآن
                user = self.user_repo.update(user, google_id=google_id, avatar_url=avatar_url)
            else:
                user = self.user_repo.create(
                    name=name,
                    email=email,
                    google_id=google_id,
                    avatar_url=avatar_url,
                    is_verified=True,
                    role=UserRole.USER,
                )

        return self._build_tokens(user), user

    def get_user_by_id(self, user_id):
        return self.user_repo.get_by_id(user_id)

    def _build_tokens(self, user):
        additional_claims = {"role": user.role.value}
        access_token = create_access_token(
            identity=str(user.id), additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(identity=str(user.id))
        return {"access_token": access_token, "refresh_token": refresh_token}
