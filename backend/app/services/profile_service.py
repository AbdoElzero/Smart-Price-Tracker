import os
import uuid
from flask import current_app
from PIL import Image, UnidentifiedImageError

from app.repositories.user_repository import UserRepository
from app.errors.exceptions import AuthError, NotFoundError, ValidationAppError
from app.utils.security import hash_password, verify_password


def _allowed_avatar_file(filename, allowed_extensions):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


class ProfileService:
    def __init__(self):
        self.user_repo = UserRepository()

    def update_profile(self, user_id, data):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("المستخدم غير موجود")

        update_fields = {}
        if "name" in data:
            update_fields["name"] = data["name"].strip()
        if "preferred_country_id" in data:
            update_fields["preferred_country_id"] = data["preferred_country_id"]

        if not update_fields:
            return user

        return self.user_repo.update(user, **update_fields)

    def change_password(self, user_id, data):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("المستخدم غير موجود")

        if not user.password_hash:
            raise AuthError("هذا الحساب مسجَّل عبر Google ولا يملك كلمة سر حاليًا")

        if not verify_password(data["current_password"], user.password_hash):
            raise AuthError("كلمة السر الحالية غير صحيحة")

        self.user_repo.update(user, password_hash=hash_password(data["new_password"]))
        return user

    def update_avatar(self, user_id, file_storage):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("المستخدم غير موجود")

        if not file_storage or file_storage.filename == "":
            raise ValidationAppError("يرجى اختيار صورة")

        allowed_extensions = current_app.config["ALLOWED_AVATAR_EXTENSIONS"]
        if not _allowed_avatar_file(file_storage.filename, allowed_extensions):
            raise ValidationAppError("صيغة الصورة غير مدعومة (المسموح: png, jpg, jpeg, webp)")

        upload_folder = current_app.config["UPLOAD_FOLDER"]
        os.makedirs(upload_folder, exist_ok=True)

        filename = f"{uuid.uuid4().hex}.jpg"
        filepath = os.path.join(upload_folder, filename)

        try:
            image = Image.open(file_storage.stream)
            image = image.convert("RGB")
            image.thumbnail((512, 512))
            image.save(filepath, "JPEG", quality=85)
        except UnidentifiedImageError:
            raise ValidationAppError("تعذّر قراءة الصورة، يرجى تجربة صورة أخرى")

        # حذف الصورة القديمة لو كانت مرفوعة محليًا (وليست رابط خارجي من Google)
        if user.avatar_url and user.avatar_url.startswith("/static/uploads/avatars/"):
            old_path = os.path.join(upload_folder, os.path.basename(user.avatar_url))
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except OSError:
                    pass

        new_avatar_url = f"/static/uploads/avatars/{filename}"
        return self.user_repo.update(user, avatar_url=new_avatar_url)
