from rest_framework import serializers
from detector.models import NewsPrediction, ModelPerformance

class PredictionCreateSerializer(serializers.Serializer):
    news_text = serializers.CharField(min_length=20, max_length=50000)
    news_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)

class NewsPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsPrediction
        fields = ("id", "news_text", "news_url", "prediction", "confidence", "model_name", "created_at")

class ModelPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPerformance
        fields = ("id", "model_name", "accuracy", "precision", "recall", "f1_score", "trained_at")
