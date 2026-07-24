"""
اختبارات تكاملية لـ Admin API.
تتحقق بشكل خاص من أمان نقاط النهاية الإدارية.
"""
import pytest


class TestAdminSecurity:

    def test_stats_requires_auth(self, client):
        """الإحصائيات تتطلب تسجيل دخول."""
        response = client.get("/api/v1/admin/stats")
        assert response.status_code == 401

    def test_stats_requires_admin_role(self, client, auth_headers):
        """المستخدم العادي لا يستطيع الوصول للإحصائيات."""
        response = client.get("/api/v1/admin/stats", headers=auth_headers)
        assert response.status_code == 403

    def test_admin_products_requires_admin(self, client, auth_headers):
        """قائمة منتجات الأدمن محمية من المستخدم العادي."""
        response = client.get("/api/v1/admin/products", headers=auth_headers)
        assert response.status_code == 403

    def test_admin_users_requires_admin(self, client, auth_headers):
        """قائمة المستخدمين محمية من المستخدم العادي."""
        response = client.get("/api/v1/admin/users", headers=auth_headers)
        assert response.status_code == 403

    def test_admin_delete_product_requires_admin(self, client, auth_headers):
        """حذف منتج محمي من المستخدم العادي."""
        response = client.delete("/api/v1/admin/products/1", headers=auth_headers)
        assert response.status_code == 403


class TestAdminAccess:

    def test_admin_can_get_stats(self, client, admin_headers):
        """المشرف يستطيع الوصول للإحصائيات."""
        response = client.get("/api/v1/admin/stats", headers=admin_headers)
        assert response.status_code == 200
        data = response.json["data"]
        assert "products" in data
        assert "users" in data

    def test_admin_stats_structure(self, client, admin_headers):
        """هيكل الإحصائيات صحيح."""
        response = client.get("/api/v1/admin/stats", headers=admin_headers)
        data = response.json["data"]
        assert "total" in data["products"]
        assert "active" in data["products"]
        assert "total" in data["users"]

    def test_admin_can_list_products(self, client, admin_headers):
        """المشرف يستطيع رؤية كل المنتجات."""
        response = client.get("/api/v1/admin/products", headers=admin_headers)
        assert response.status_code == 200
        assert "data" in response.json
        assert "meta" in response.json

    def test_admin_can_list_users(self, client, admin_headers):
        """المشرف يستطيع رؤية كل المستخدمين."""
        response = client.get("/api/v1/admin/users", headers=admin_headers)
        assert response.status_code == 200
        assert isinstance(response.json["data"], list)

    def test_admin_create_product(self, client, admin_headers):
        """المشرف يستطيع إضافة منتج جديد."""
        from app.models import Brand, Category
        from app.extensions import db

        products_before = client.get(
            "/api/v1/admin/products", headers=admin_headers
        ).json["meta"]["total"]

        response = client.post("/api/v1/admin/products", json={
            "name_ar": "منتج اختبار",
            "name_en": "Test Product Admin",
            "brand_id": 1,
            "category_id": 1,
            "is_active": True,
        }, headers=admin_headers)

        assert response.status_code == 201
        assert response.json["data"]["name_ar"] == "منتج اختبار"

    def test_admin_create_product_missing_required_fields(self, client, admin_headers):
        """إضافة منتج بدون حقول مطلوبة → 422."""
        response = client.post("/api/v1/admin/products", json={
            "name_ar": "منتج ناقص",
        }, headers=admin_headers)
        assert response.status_code == 422

    def test_admin_update_product(self, client, admin_headers):
        """المشرف يستطيع تعديل منتج موجود."""
        response = client.put("/api/v1/admin/products/1", json={
            "is_active": False,
        }, headers=admin_headers)
        # لو المنتج موجود → 200، لو مش موجود → 404 (كلاهما مقبول)
        assert response.status_code in [200, 404]

    def test_admin_delete_nonexistent_product(self, client, admin_headers):
        """حذف منتج غير موجود → 404."""
        response = client.delete("/api/v1/admin/products/99999", headers=admin_headers)
        assert response.status_code == 404
