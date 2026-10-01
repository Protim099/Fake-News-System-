from django.contrib.auth.models import User
from django.db import models

class NewsPrediction(models.Model):
    PREDICTION_CHOICES = [
        ("REAL", "REAL"),
        ("FAKE", "FAKE"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="predictions")
    news_text = models.TextField()
    news_url = models.URLField(blank=True, null=True)
    prediction = models.CharField(max_length=10, choices=PREDICTION_CHOICES)
    confidence = models.FloatField()
    model_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def confidence_percent(self):
        return self.confidence * 100

    def __str__(self):
        return f"{self.prediction} - {self.user.username} - {self.created_at:%Y-%m-%d %H:%M}"

class ModelPerformance(models.Model):
    model_name = models.CharField(max_length=100)
    accuracy = models.FloatField()
    precision = models.FloatField()
    recall = models.FloatField()
    f1_score = models.FloatField()
    trained_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-trained_at"]

    def __str__(self):
        return f"{self.model_name} ({self.accuracy:.3f})"
