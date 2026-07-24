"""
خدمة التوقعات: تجمع بيانات تاريخ الأسعار من قاعدة البيانات،
تُمرّرها للـ PriceAnalyzer، ثم تحفظ النتيجة في جدول Prediction.
"""
from datetime import datetime
from app.extensions import db
from app.models import Product, Price, PriceHistory, Prediction, RecommendationType
from app.ai.price_analyzer import analyze_price
from app.errors.exceptions import NotFoundError


class PredictionService:

    def get_for_product(self, product_id):
        """جلب آخر توقع محفوظ لمنتج معيّن (لو موجود)."""
        return (
            Prediction.query
            .filter_by(product_id=product_id)
            .order_by(Prediction.analyzed_at.desc())
            .first()
        )

    def analyze_and_save(self, product_id):
        """
        يُشغّل التحليل الكامل لمنتج واحد ويحفظ نتيجته في الـ DB.
        يُستدعى من:
          - الـ Celery task الدوري (لكل المنتجات دفعة واحدة)
          - الـ API endpoint عند الطلب لأول مرة أو بعد مدة انتهاء التحليل
        """
        product = Product.query.get(product_id)
        if not product:
            raise NotFoundError("المنتج غير موجود")

        # جمع بيانات تاريخ الأسعار من كل المتاجر للمنتج
        prices = Price.query.filter_by(product_id=product_id).all()
        if not prices:
            return None

        all_history_values = []
        current_price_value = None

        for price in prices:
            history_rows = (
                PriceHistory.query
                .filter_by(price_id=price.id)
                .order_by(PriceHistory.recorded_at.desc())
                .limit(180)  # نحلّل آخر 180 تسجيل كحد أقصى (تقريبًا 6 أشهر بتسجيل يومي)
                .all()
            )
            for row in history_rows:
                all_history_values.append(float(row.recorded_price))

            # نأخذ أفضل سعر حالي (أقل سعر متوفر) لاتخاذ التوصية
            if price.in_stock and price.current_price:
                cp = float(price.current_price)
                if current_price_value is None or cp < current_price_value:
                    current_price_value = cp

        if current_price_value is None:
            return None

        result = analyze_price(current_price_value, all_history_values)

        if result.recommendation is None:
            # بيانات غير كافية — نحفظ سجل بدون توصية فعلية
            return None

        # حذف التوقع القديم واستبداله بالجديد
        old = self.get_for_product(product_id)
        if old:
            db.session.delete(old)
            db.session.flush()

        prediction = Prediction(
            product_id=product_id,
            recommendation=result.recommendation,
            confidence_score=result.confidence_score,
            reason_ar=result.reason_ar,
            reason_en=result.reason_en,
            based_on_days=90,
            analyzed_at=result.analyzed_at,
        )
        db.session.add(prediction)
        db.session.commit()
        return prediction
