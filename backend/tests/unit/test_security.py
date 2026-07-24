"""
اختبارات وحدة (Unit Tests) لدوال التشفير.
"""
import pytest
from app.utils.security import hash_password, verify_password


class TestSecurity:

    def test_hash_password_returns_string(self):
        """hash_password يُرجع string."""
        result = hash_password("TestPassword123")
        assert isinstance(result, str)

    def test_hash_is_not_plain_text(self):
        """الـ hash لا يساوي كلمة السر الأصلية أبداً."""
        password = "MySecretPass"
        hashed = hash_password(password)
        assert hashed != password

    def test_verify_correct_password_returns_true(self):
        """كلمة السر الصحيحة → True."""
        password = "CorrectPassword123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password_returns_false(self):
        """كلمة السر الخاطئة → False."""
        hashed = hash_password("OriginalPassword")
        assert verify_password("WrongPassword", hashed) is False

    def test_two_hashes_of_same_password_are_different(self):
        """نفس كلمة السر تعطي hash مختلف في كل مرة (Salt مختلف)."""
        password = "SamePassword123"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 != hash2

    def test_verify_with_empty_hash_returns_false(self):
        """hash فارغ → False (بدون استثناء)."""
        assert verify_password("SomePassword", None) is False

    def test_verify_with_empty_password(self):
        """كلمة سر فارغة مقارنةً بـ hash حقيقي → False."""
        hashed = hash_password("RealPassword")
        assert verify_password("", hashed) is False

    def test_hash_long_password(self):
        """كلمة سر طويلة جداً تُعالَج بدون مشاكل."""
        long_password = "A" * 100
        hashed = hash_password(long_password)
        assert verify_password(long_password, hashed) is True

    def test_hash_password_with_special_characters(self):
        """كلمة سر بأحرف خاصة وعربية تعمل بشكل صحيح."""
        password = "كلمة_سر!@#123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
