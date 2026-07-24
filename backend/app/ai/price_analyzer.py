"""
محرّك تحليل الأسعار الإحصائي (AI Decision Engine).
يعتمد على بيانات PriceHistory الفعلية لكل منتج ويُنتج توصية مع شرح.

المنطق:
- نحسب الـ percentile للسعر الحالي بين الأسعار التاريخية
- السعر في أدنى 15% → ✅ اشتري الآن
- السعر في الـ 15-60% → ⏳ انتظر
- السعر في أعلى 40% → 🔴 السعر مرتفع
- لو البيانات أقل من 7 نقاط → لا توصية كافية

هذا النظام لا يستخدم LLM أو نماذج ML خارجية.
يعتمد على إحصاء بسيط وشفاف وقابل للتفسير.
"""
import statistics
from datetime import datetime
from app.models import RecommendationType


MIN_DATA_POINTS = 7  # الحد الأدنى لتقديم توصية موثوقة


class PriceAnalysisResult:
    __slots__ = (
        "recommendation",
        "confidence_score",
        "reason_ar",
        "reason_en",
        "current_price",
        "min_price",
        "max_price",
        "avg_price",
        "median_price",
        "percentile",
        "data_points",
        "analyzed_at",
    )

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def analyze_price(current_price: float, price_history: list[float]) -> PriceAnalysisResult:
    """
    يحلّل السعر الحالي مقارنةً بتاريخ الأسعار ويُرجع نتيجة تحليل كاملة.

    المدخلات:
        current_price: السعر الحالي (من جدول Price)
        price_history: قائمة بكل الأسعار التاريخية لنفس المنتج في نفس المتجر (من PriceHistory)

    المخرجات:
        PriceAnalysisResult مع التوصية والشرح والإحصاءات
    """
    now = datetime.utcnow()
    data_points = len(price_history)

    if data_points < MIN_DATA_POINTS:
        return PriceAnalysisResult(
            recommendation=None,
            confidence_score=0.0,
            reason_ar=(
                f"لا تتوفر بيانات تاريخية كافية لتقديم توصية موثوقة بعد "
                f"({data_points} نقطة بيانات فقط، والحد الأدنى {MIN_DATA_POINTS})."
            ),
            reason_en=(
                f"Insufficient price history for a reliable recommendation "
                f"({data_points} data points, minimum is {MIN_DATA_POINTS})."
            ),
            current_price=current_price,
            min_price=min(price_history) if price_history else current_price,
            max_price=max(price_history) if price_history else current_price,
            avg_price=current_price,
            median_price=current_price,
            percentile=None,
            data_points=data_points,
            analyzed_at=now,
        )

    min_price = min(price_history)
    max_price = max(price_history)
    avg_price = statistics.mean(price_history)
    median_price = statistics.median(price_history)
    sorted_history = sorted(price_history)

    # حساب الـ percentile: كم نسبة الأسعار التاريخية كانت أقل من السعر الحالي؟
    below_count = sum(1 for p in sorted_history if p <= current_price)
    percentile = (below_count / data_points) * 100

    # حساب نسبة الانخفاض من الحد الأقصى
    drop_from_max_pct = ((max_price - current_price) / max_price * 100) if max_price > 0 else 0

    # حساب الانحراف المعياري (مفيد لتقييم ثبات/تذبذب السعر)
    try:
        std_dev = statistics.stdev(price_history)
        price_volatile = (std_dev / avg_price * 100) > 15  # أكثر من 15% تذبذب
    except statistics.StatisticsError:
        std_dev = 0
        price_volatile = False

    # اتخاذ القرار
    if percentile <= 15:
        recommendation = RecommendationType.BUY_NOW
        confidence = round(min(99, 95 - percentile), 1)
        reason_ar = (
            f"السعر الحالي ({current_price:.2f}) يُعدّ من أفضل الأسعار المسجَّلة تاريخيًا، "
            f"إذ يقع في أدنى {percentile:.0f}٪ من الأسعار على مدار الفترة المُحلَّلة. "
            f"أدنى سعر مسجَّل كان {min_price:.2f} والمتوسط {avg_price:.2f}."
        )
        reason_en = (
            f"Current price ({current_price:.2f}) is among the best recorded historically, "
            f"ranking in the bottom {percentile:.0f}% of all prices analyzed. "
            f"Lowest ever was {min_price:.2f}, average is {avg_price:.2f}."
        )

    elif percentile <= 60:
        recommendation = RecommendationType.WAIT
        confidence = round(min(85, 60 + (60 - percentile)), 1)
        reason_ar = (
            f"السعر الحالي ({current_price:.2f}) مقبول نسبيًا (يقع في النسبة المئوية {percentile:.0f}٪). "
            f"المتوسط التاريخي {avg_price:.2f} وأدنى سعر مسجَّل {min_price:.2f}. "
        )
        if price_volatile:
            reason_ar += "السعر يتذبذب بشكل ملحوظ مما يعني احتمال نزوله قريبًا."
        else:
            reason_ar += "يُنصح بالانتظار لاحتمال نزول السعر في الفترة القادمة."
        reason_en = (
            f"Current price ({current_price:.2f}) is moderate (at the {percentile:.0f}th percentile). "
            f"Historical average is {avg_price:.2f}, lowest recorded is {min_price:.2f}."
        )

    else:
        recommendation = RecommendationType.HIGH_PRICE
        confidence = round(min(95, 50 + (percentile - 60)), 1)
        reason_ar = (
            f"السعر الحالي ({current_price:.2f}) مرتفع مقارنةً بالتاريخ، "
            f"إذ يقع في أعلى {100 - percentile:.0f}٪ من الأسعار المسجَّلة. "
            f"أدنى سعر مسجَّل {min_price:.2f}، والمتوسط {avg_price:.2f}. "
        )
        if drop_from_max_pct > 5:
            reason_ar += f"السعر انخفض بالفعل {drop_from_max_pct:.1f}٪ من أعلى سعر ({max_price:.2f})، لكنه لا يزال مرتفعًا."
        else:
            reason_ar += "يُنصح بالانتظار حتى ينخفض السعر أكثر."
        reason_en = (
            f"Current price ({current_price:.2f}) is high compared to history, "
            f"ranking in the top {100 - percentile:.0f}% of all recorded prices. "
            f"Lowest recorded: {min_price:.2f}, average: {avg_price:.2f}."
        )

    return PriceAnalysisResult(
        recommendation=recommendation,
        confidence_score=confidence,
        reason_ar=reason_ar,
        reason_en=reason_en,
        current_price=current_price,
        min_price=min_price,
        max_price=max_price,
        avg_price=round(avg_price, 2),
        median_price=round(median_price, 2),
        percentile=round(percentile, 1),
        data_points=data_points,
        analyzed_at=now,
    )
