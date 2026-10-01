from django.contrib import admin
from .models import NewsPrediction, ModelPerformance

@admin.register(NewsPrediction)
class NewsPredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "prediction", "confidence", "model_name", "created_at")
    list_filter = ("prediction", "model_name")
    search_fields = ("news_text", "news_url", "user__username")

@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ("model_name", "accuracy", "precision", "recall", "f1_score", "trained_at")
