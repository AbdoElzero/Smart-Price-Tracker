"""
اختبارات وحدة (Unit Tests) لمحرك تحليل الأسعار.

هذه الاختبارات لا تحتاج قاعدة بيانات ولا HTTP ← تعمل بشكل معزول تام.
"""
import pytest
from app.ai.price_analyzer import analyze_price
from app.models import RecommendationType


class TestPriceAnalyzer:

    def test_insufficient_data_returns_none_recommendation(self):
        """لو البيانات أقل من 7 نقاط → لا توصية."""
        result = analyze_price(100.0, [90.0, 95.0, 100.0])
        assert result.recommendation is None
        assert result.confidence_score == 0.0
        assert result.data_points == 3

    def test_buy_now_when_price_at_historical_low(self):
        """السعر في أدنى 15% → اشتري الآن."""
        # تاريخ أسعار يتراوح بين 1000 و2000
        history = list(range(1000, 2100, 100))  # [1000, 1100, ..., 2000] = 11 نقطة
        current_price = 1000.0  # أدنى سعر في التاريخ

        result = analyze_price(current_price, history)

        assert result.recommendation == RecommendationType.BUY_NOW
        assert result.confidence_score > 0
        assert result.percentile <= 15

    def test_high_price_when_at_historical_peak(self):
        """السعر في أعلى 40% → السعر مرتفع."""
        history = list(range(1000, 2100, 100))  # [1000, ..., 2000]
        current_price = 2000.0  # أعلى سعر

        result = analyze_price(current_price, history)

        assert result.recommendation == RecommendationType.HIGH_PRICE
        assert result.percentile > 60

    def test_wait_when_price_is_average(self):
        """السعر عند المتوسط → انتظر."""
        history = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
        current_price = 150.0  # وسط النطاق تماماً

        result = analyze_price(current_price, history)

        assert result.recommendation == RecommendationType.WAIT
        assert 15 < result.percentile <= 60

    def test_result_contains_all_statistics(self):
        """النتيجة تحتوي على كل الإحصاءات المطلوبة."""
        history = [100, 120, 140, 160, 180, 200, 220, 240, 260, 280]
        result = analyze_price(150.0, history)

        assert result.min_price == 100
        assert result.max_price == 280
        assert result.avg_price > 0
        assert result.median_price > 0
        assert result.data_points == 10
        assert result.analyzed_at is not None

    def test_reason_ar_is_non_empty_string(self):
        """شرح القرار بالعربية غير فارغ في كل الحالات."""
        history = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]

        for current_price in [100.0, 145.0, 190.0]:
            result = analyze_price(current_price, history)
            assert isinstance(result.reason_ar, str)
            assert len(result.reason_ar) > 10

    def test_confidence_score_between_0_and_100(self):
        """درجة الثقة بين 0 و100 دائماً."""
        history = list(range(100, 1100, 100))  # 10 نقاط

        for price in [100.0, 500.0, 1000.0]:
            result = analyze_price(price, history)
            if result.recommendation is not None:
                assert 0 <= float(result.confidence_score) <= 100

    def test_empty_history_returns_none_recommendation(self):
        """تاريخ فارغ → لا توصية."""
        result = analyze_price(500.0, [])
        assert result.recommendation is None
        assert result.data_points == 0

    def test_current_price_below_all_history(self):
        """السعر الحالي أقل من كل التاريخ → buy_now."""
        history = [200, 210, 220, 230, 240, 250, 260, 270, 280, 290]
        result = analyze_price(100.0, history)
        assert result.recommendation == RecommendationType.BUY_NOW

    def test_current_price_above_all_history(self):
        """السعر الحالي أعلى من كل التاريخ → high_price."""
        history = [100, 110, 120, 130, 140, 150, 160, 170, 180, 190]
        result = analyze_price(1000.0, history)
        assert result.recommendation == RecommendationType.HIGH_PRICE
