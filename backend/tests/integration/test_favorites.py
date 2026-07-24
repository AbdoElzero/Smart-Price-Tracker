"""
اختبارات تكاملية (Integration Tests) لـ Favorites API.
"""
import pytest


class TestFavorites:

    def test_list_favorites_requires_auth(self, client):
        """قائمة المفضلة تتطلب تسجيل دخول."""
        response = client.get("/api/v1/favorites")
        assert response.status_code == 401

    def test_list_favorites_empty_for_new_user(self, client, auth_headers):
        """مستخدم جديد → مفضلة فارغة."""
        response = client.get("/api/v1/favorites", headers=auth_headers)
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_get_favorite_ids_requires_auth(self, client):
        """قائمة معرّفات المفضلة تتطلب تسجيل دخول."""
        response = client.get("/api/v1/favorites/ids")
        assert response.status_code == 401

    def test_favorite_ids_is_list(self, client, auth_headers):
        """معرّفات المفضلة تُرجع قائمة."""
        response = client.get("/api/v1/favorites/ids", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json["data"], list)

    def test_toggle_favorite_requires_auth(self, client):
        """Toggle المفضلة يتطلب تسجيل دخول."""
        response = client.post("/api/v1/favorites/1/toggle")
        assert response.status_code == 401

    def test_toggle_nonexistent_product_returns_404(self, client, auth_headers):
        """Toggle منتج غير موجود → 404."""
        response = client.post("/api/v1/favorites/99999/toggle", headers=auth_headers)
        assert response.status_code == 404

    def test_toggle_favorite_adds_product(self, client, auth_headers):
        """Toggle منتج → يُضاف للمفضلة."""
        products = client.get("/api/v1/products").json["data"]
        if not products:
            pytest.skip("لا توجد منتجات")

        product_id = products[0]["id"]
        response = client.post(f"/api/v1/favorites/{product_id}/toggle", headers=auth_headers)
        assert response.status_code == 200
        assert response.json["favorited"] is True

    def test_toggle_favorite_twice_removes_product(self, client, auth_headers):
        """Toggle مرتين → يُزال من المفضلة."""
        products = client.get("/api/v1/products").json["data"]
        if not products:
            pytest.skip("لا توجد منتجات")

        product_id = products[0]["id"]
        # Toggle مرة أولى (إضافة)
        client.post(f"/api/v1/favorites/{product_id}/toggle", headers=auth_headers)
        # Toggle مرة ثانية (إزالة)
        response = client.post(f"/api/v1/favorites/{product_id}/toggle", headers=auth_headers)
        assert response.status_code == 200
        assert response.json["favorited"] is False
