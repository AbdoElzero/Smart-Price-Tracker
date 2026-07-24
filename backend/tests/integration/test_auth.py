"""
اختبارات تكاملية (Integration Tests) لـ Authentication API.
"""
import pytest


class TestRegister:

    def test_register_success(self, client):
        """تسجيل حساب جديد بنجاح."""
        response = client.post("/api/v1/auth/register", json={
            "name": "مستخدم جديد",
            "email": "newuser@example.com",
            "password": "StrongPass123",
        })
        assert response.status_code == 201
        data = response.json
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "newuser@example.com"
        assert data["user"]["name"] == "مستخدم جديد"

    def test_register_duplicate_email_returns_409(self, client, regular_user):
        """تسجيل بريد موجود مسبقاً → 409."""
        response = client.post("/api/v1/auth/register", json={
            "name": "مستخدم ثاني",
            "email": "ahmed_test@example.com",  # بريد موجود
            "password": "StrongPass123",
        })
        assert response.status_code == 409

    def test_register_short_password_returns_422(self, client):
        """كلمة سر أقل من 8 أحرف → 422."""
        response = client.post("/api/v1/auth/register", json={
            "name": "مستخدم",
            "email": "user2@example.com",
            "password": "123",
        })
        assert response.status_code == 422

    def test_register_invalid_email_returns_422(self, client):
        """بريد إلكتروني غير صالح → 422."""
        response = client.post("/api/v1/auth/register", json={
            "name": "مستخدم",
            "email": "not-an-email",
            "password": "StrongPass123",
        })
        assert response.status_code == 422

    def test_register_missing_name_returns_422(self, client):
        """اسم مفقود → 422."""
        response = client.post("/api/v1/auth/register", json={
            "email": "user3@example.com",
            "password": "StrongPass123",
        })
        assert response.status_code == 422

    def test_register_returns_role_user(self, client):
        """الدور الافتراضي عند التسجيل = user."""
        response = client.post("/api/v1/auth/register", json={
            "name": "مستخدم عادي",
            "email": "rolecheck@example.com",
            "password": "StrongPass123",
        })
        assert response.status_code == 201
        assert response.json["user"]["role"] == "user"


class TestLogin:

    def test_login_success(self, client, regular_user):
        """تسجيل دخول صحيح → 200 + tokens."""
        response = client.post("/api/v1/auth/login", json={
            "email": "ahmed_test@example.com",
            "password": "TestPass123",
        })
        assert response.status_code == 200
        data = response.json
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "ahmed_test@example.com"

    def test_login_wrong_password_returns_401(self, client, regular_user):
        """كلمة سر خاطئة → 401."""
        response = client.post("/api/v1/auth/login", json={
            "email": "ahmed_test@example.com",
            "password": "WrongPassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_email_returns_401(self, client):
        """بريد غير موجود → 401."""
        response = client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "SomePassword123",
        })
        assert response.status_code == 401

    def test_login_missing_fields_returns_422(self, client):
        """حقول مفقودة → 422."""
        response = client.post("/api/v1/auth/login", json={
            "email": "ahmed_test@example.com",
        })
        assert response.status_code == 422

    def test_login_email_case_insensitive(self, client, regular_user):
        """البريد الإلكتروني غير حساس لحالة الحروف."""
        response = client.post("/api/v1/auth/login", json={
            "email": "AHMED_TEST@EXAMPLE.COM",
            "password": "TestPass123",
        })
        assert response.status_code == 200


class TestMe:

    def test_me_returns_current_user(self, client, auth_headers):
        """GET /me يُرجع بيانات المستخدم الحالي."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert "user" in response.json
        assert response.json["user"]["email"] == "ahmed_test@example.com"

    def test_me_without_token_returns_401(self, client):
        """بدون token → 401."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_me_with_invalid_token_returns_401(self, client):
        """توكن غير صالح → 401."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401


class TestRefresh:

    def test_refresh_returns_new_access_token(self, client, regular_user):
        """refresh_token يُصدر access_token جديد."""
        login = client.post("/api/v1/auth/login", json={
            "email": "ahmed_test@example.com",
            "password": "TestPass123",
        })
        refresh_token = login.json["refresh_token"]

        response = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {refresh_token}"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json

    def test_refresh_with_access_token_fails(self, client, auth_headers):
        """لا يمكن استخدام access_token كـ refresh_token."""
        access_token = auth_headers["Authorization"].split(" ")[1]
        response = client.post(
            "/api/v1/auth/refresh",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        assert response.status_code == 401


class TestLogout:

    def test_logout_success(self, client, auth_headers):
        """تسجيل الخروج يُرجع 200."""
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        assert response.status_code == 200
        assert "message" in response.json

    def test_logout_without_token_returns_401(self, client):
        """تسجيل الخروج بدون توكن → 401."""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 401
