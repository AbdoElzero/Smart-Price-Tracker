"""
سكريبت اختياري لإضافة بيانات تاريخ أسعار تجريبية لمنتجات الـ Demo،
لاختبار نظام الذكاء الاصطناعي قبل توفّر بيانات حقيقية من الـ Scrapers.

⚠️ هذه البيانات تجريبية بالكامل (تُولَّد بشكل برمجي) وليست أسعار حقيقية.
الغرض منها فقط اختبار منطق التحليل والتوصية.

التشغيل (اختياري):
    python seed_price_history.py
"""
import random
from datetime import datetime, timedelta
from app import create_app
from app.extensions import db
from app.models import Product, Price, PriceHistory, Store, Country, Currency
from app.services.prediction_service import PredictionService


def generate_realistic_price_history(base_price, days=90):
    """يولّد تاريخ سعر واقعي بتذبذب طبيعي (مع ارتفاع وانخفاض وعروض عشوائية)."""
    prices = []
    current = base_price
    for i in range(days):
        # تذبذب يومي طبيعي (±2%)
        daily_change = random.uniform(-0.02, 0.02)

        # عرض عشوائي كل 30 يوم تقريبًا (15% خصم)
        if random.random() < 0.03:
            current = base_price * random.uniform(0.82, 0.90)
        # عودة للسعر الطبيعي
        elif random.random() < 0.05:
            current = base_price * random.uniform(0.97, 1.05)
        else:
            current = current * (1 + daily_change)

        # تقييد السعر بين 70% و120% من السعر الأساسي
        current = max(base_price * 0.70, min(base_price * 1.20, current))
        prices.append(round(current, 2))
    return prices


def run():
    app = create_app()
    with app.app_context():
        print("🌱 بدء إضافة بيانات تاريخ أسعار تجريبية...")

        products = Product.query.filter_by(is_active=True).all()
        if not products:
            print("⚠️  لا توجد منتجات. شغّل seed_products.py أولاً.")
            return

        # نحتاج متجر ودولة وعملة واحدة على الأقل
        store = Store.query.first()
        country = Country.query.first()
        currency = Currency.query.filter_by(code="EGP").first() or Currency.query.first()

        if not store or not country or not currency:
            print("⚠️  يجب تشغيل seed.py أولاً لإنشاء المتاجر والدول والعملات.")
            return

        # أسعار أساسية تجريبية لكل منتج (بالعملة المحلية)
        base_prices = {
            "apple-iphone-15-128gb": 49999,
            "samsung-galaxy-s24-256gb": 42999,
            "apple-macbook-air-m2-256gb": 79999,
            "asus-rog-strix-g16": 65999,
            "nvidia-geforce-rtx-4070": 28999,
            "samsung-odyssey-g7-27": 18999,
        }

        prediction_service = PredictionService()

        for product in products:
            base_price = base_prices.get(product.slug, 15000)
            current_price = round(base_price * random.uniform(0.95, 1.05), 2)

            # إنشاء سعر حالي لو ما كانش موجود
            existing_price = Price.query.filter_by(
                product_id=product.id, store_id=store.id, country_id=country.id
            ).first()

            if not existing_price:
                existing_price = Price(
                    product_id=product.id,
                    store_id=store.id,
                    country_id=country.id,
                    currency_id=currency.id,
                    current_price=current_price,
                    in_stock=True,
                    product_url=f"{store.website_url}/product/{product.slug}",
                )
                db.session.add(existing_price)
                db.session.flush()
                print(f"  ✅ أضاف سعر لـ {product.name_ar}: {current_price}")
            else:
                print(f"  ⏭️  سعر موجود مسبقًا لـ {product.name_ar}")

            # توليد تاريخ أسعار (90 يوم)
            existing_count = PriceHistory.query.filter_by(price_id=existing_price.id).count()
            if existing_count < 7:
                history_values = generate_realistic_price_history(base_price, days=90)
                base_date = datetime.utcnow() - timedelta(days=90)
                for i, price_val in enumerate(history_values):
                    ph = PriceHistory(
                        price_id=existing_price.id,
                        recorded_price=price_val,
                        recorded_at=base_date + timedelta(days=i),
                    )
                    db.session.add(ph)
                print(f"  📈 أضاف 90 نقطة بيانات تاريخية لـ {product.name_ar}")

        db.session.commit()
        print("\n✅ تم حفظ بيانات الأسعار التاريخية!")

        # تشغيل التحليل الآن
        print("\n🧠 تشغيل نظام الذكاء الاصطناعي على كل المنتجات...")
        for product in products:
            try:
                result = prediction_service.analyze_and_save(product.id)
                if result:
                    icon = {"buy_now": "✅", "wait": "⏳", "high_price": "🔴"}.get(
                        result.recommendation.value, "❓"
                    )
                    print(f"  {icon} {product.name_ar}: {result.recommendation.value} ({result.confidence_score}%)")
                else:
                    print(f"  ⚠️  {product.name_ar}: بيانات غير كافية")
            except Exception as e:
                print(f"  ❌ {product.name_ar}: خطأ - {e}")

        print("\n🎉 اكتمل التحليل! يمكنك الآن مشاهدة التوصيات على صفحة كل منتج.")


if __name__ == "__main__":
    run()
