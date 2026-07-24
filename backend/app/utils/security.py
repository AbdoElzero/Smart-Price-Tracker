"""
دوال تشفير وفحص كلمات السر باستخدام bcrypt.
"""
import bcrypt


def hash_password(password: str) -> str:
    """تشفير كلمة سر خام إلى hash آمن للتخزين."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """مقارنة كلمة سر خام بالـ hash المخزّن."""
    if not password_hash:
        return False
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False
