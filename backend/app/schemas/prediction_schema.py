from marshmallow import Schema, fields


class PredictionSchema(Schema):
    recommendation = fields.Method("get_recommendation")
    confidence_score = fields.Decimal(as_string=True, allow_none=True)
    reason_ar = fields.String()
    reason_en = fields.String()
    based_on_days = fields.Integer()
    analyzed_at = fields.DateTime()

    label_ar = fields.Method("get_label_ar")
    color = fields.Method("get_color")
    icon = fields.Method("get_icon")

    def get_recommendation(self, obj):
        return obj.recommendation.value if obj.recommendation else None

    def get_label_ar(self, obj):
        labels = {
            "buy_now": "اشتري الآن",
            "wait": "انتظر قليلاً",
            "high_price": "السعر مرتفع",
        }
        return labels.get(obj.recommendation.value, "") if obj.recommendation else ""

    def get_color(self, obj):
        colors = {
            "buy_now": "success",
            "wait": "warning",
            "high_price": "danger",
        }
        return colors.get(obj.recommendation.value, "gray") if obj.recommendation else "gray"

    def get_icon(self, obj):
        icons = {
            "buy_now": "✅",
            "wait": "⏳",
            "high_price": "🔴",
        }
        return icons.get(obj.recommendation.value, "❓") if obj.recommendation else "❓"
