"""
اختبارات تكاملية (Integration Tests) لـ Products API.
ملاحظة: الاختبارات لا تعتمد على slugs أو IDs ثابتة،
بل تجلب البيانات ديناميكياً من الـ API لضمان الاستقرار.
"""
import pytest


class TestListProducts:

    def test_list_products_returns_200(self, client):
        """قائمة المنتجات تعمل بدون أخطاء."""
        response = client.get("/api/v1/products")
        assert response.status_code == 200
        data = response.json
        assert "data" in data
        assert "meta" in data

    def test_list_products_meta_structure(self, client):
        """meta يحتوي على الحقول المطلوبة."""
        response = client.get("/api/v1/products")
        meta = response.json["meta"]
        assert "page" in meta
        assert "per_page" in meta
        assert "total" in meta
        assert "total_pages" in meta

    def test_list_products_default_pagination(self, client):
        """الصفحة الافتراضية = 1، 12 عنصر لكل صفحة."""
        response = client.get("/api/v1/products")
        meta = response.json["meta"]
        assert meta["page"] == 1
        assert meta["per_page"] == 12

    def test_list_products_data_is_list(self, client):
        """data يُرجع قائمة دائماً."""
        response = client.get("/api/v1/products")
        assert isinstance(response.json["data"], list)

    def test_list_products_with_search(self, client):
        """البحث بالنص لا يُسبّب خطأ."""
        response = client.get("/api/v1/products?q=Galaxy")
        assert response.status_code == 200
        assert isinstance(response.json["data"], list)

    def test_list_products_page_param(self, client):
        """فلتر الصفحة يعمل بشكل صحيح."""
        response = client.get("/api/v1/products?page=1&per_page=5")
        assert response.status_code == 200
        assert response.json["meta"]["per_page"] == 5

    def test_list_products_per_page_capped_at_50(self, client):
        """per_page لا يتجاوز 50 حتى لو طُلب أكثر."""
        response = client.get("/api/v1/products?per_page=1000")
        assert response.status_code == 200
        assert response.json["meta"]["per_page"] <= 50

    def test_list_products_sort_price_asc(self, client):
        """الترتيب بالسعر من الأقل لا يُسبّب خطأ."""
        response = client.get("/api/v1/products?sort=price_asc")
        assert response.status_code == 200

    def test_list_products_sort_name(self, client):
        """الترتيب بالاسم لا يُسبّب خطأ."""
        response = client.get("/api/v1/products?sort=name_asc")
        assert response.status_code == 200


class TestGetProduct:

    def _get_first_product_slug(self, client):
        """Helper: يجلب slug أول منتج فعّال من الـ API."""
        response = client.get("/api/v1/products")
        products = response.json.get("data", [])
        return products[0]["slug"] if products else None

    def test_get_existing_product(self, client):
        """جلب منتج موجود → 200."""
        slug = self._get_first_product_slug(client)
        if not slug:
            pytest.skip("لا توجد منتجات في قاعدة البيانات")

        response = client.get(f"/api/v1/products/{slug}")
        assert response.status_code == 200
        assert "data" in response.json

    def test_get_nonexistent_product_returns_404(self, client):
        """منتج غير موجود → 404."""
        response = client.get("/api/v1/products/nonexistent-product-xyz-999")
        assert response.status_code == 404

    def test_product_detail_has_required_fields(self, client):
        """تفاصيل المنتج تحتوي على الحقول الأساسية."""
        slug = self._get_first_product_slug(client)
        if not slug:
            pytest.skip("لا توجد منتجات في قاعدة البيانات")

        response = client.get(f"/api/v1/products/{slug}")
        data = response.json["data"]
        assert "id" in data
        assert "name_ar" in data
        assert "slug" in data
        assert "brand" in data
        assert "category" in data

    def test_product_detail_brand_has_name(self, client):
        """بيانات العلامة التجارية موجودة."""
        slug = self._get_first_product_slug(client)
        if not slug:
            pytest.skip("لا توجد منتجات في قاعدة البيانات")

        response = client.get(f"/api/v1/products/{slug}")
        brand = response.json["data"]["brand"]
        assert brand is not None
        assert "name_ar" in brand

    def test_product_detail_slug_matches(self, client):
        """الـ slug المُسترجَع يطابق المطلوب."""
        slug = self._get_first_product_slug(client)
        if not slug:
            pytest.skip("لا توجد منتجات في قاعدة البيانات")

        response = client.get(f"/api/v1/products/{slug}")
        assert response.json["data"]["slug"] == slug


class TestCompareProducts:

    def test_compare_with_valid_ids(self, client):
        """مقارنة منتجات بمعرّفات حقيقية."""
        products = client.get("/api/v1/products").json["data"]
        if not products:
            pytest.skip("لا توجد منتجات")

        product_id = products[0]["id"]
        response = client.get(f"/api/v1/products/compare?ids={product_id}")
        assert response.status_code == 200
        assert len(response.json["data"]) == 1

    def test_compare_empty_ids(self, client):
        """مقارنة بدون معرّفات → قائمة فارغة."""
        response = client.get("/api/v1/products/compare?ids=")
        assert response.status_code == 200
        assert response.json["data"] == []

    def test_compare_caps_at_4(self, client):
        """المقارنة لا تُرجع أكثر من 4 منتجات."""
        response = client.get("/api/v1/products/compare?ids=1,2,3,4,5,6")
        assert response.status_code == 200
        assert len(response.json["data"]) <= 4


class TestCatalogEndpoints:

    def test_list_categories(self, client):
        """قائمة التصنيفات تعمل."""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        assert isinstance(response.json["data"], list)

    def test_list_brands(self, client):
        """قائمة العلامات التجارية تعمل."""
        response = client.get("/api/v1/brands")
        assert response.status_code == 200
        assert isinstance(response.json["data"], list)

    def test_list_countries(self, client):
        """قائمة الدول تعمل."""
        response = client.get("/api/v1/countries")
        assert response.status_code == 200
        assert isinstance(response.json["data"], list)

    def test_price_history_returns_200(self, client):
        """تاريخ الأسعار لمنتج موجود لا يُسبّب خطأ."""
        products = client.get("/api/v1/products").json["data"]
        if not products:
            pytest.skip("لا توجد منتجات")

        product_id = products[0]["id"]
        response = client.get(f"/api/v1/products/{product_id}/price-history")
        assert response.status_code == 200
        assert "data" in response.json
        assert "stats" in response.json


class TestHealthCheck:

    def test_health_check_returns_ok(self, client):
        """endpoint الصحة يعمل دائماً."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json["status"] == "ok"
