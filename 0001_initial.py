from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="ModelPerformance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("model_name", models.CharField(max_length=100)),
                ("accuracy", models.FloatField()),
                ("precision", models.FloatField()),
                ("recall", models.FloatField()),
                ("f1_score", models.FloatField()),
                ("trained_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering":["-trained_at"]},
        ),
        migrations.CreateModel(
            name="NewsPrediction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("news_text", models.TextField()),
                ("news_url", models.URLField(blank=True, null=True)),
                ("prediction", models.CharField(choices=[("REAL","REAL"),("FAKE","FAKE")], max_length=10)),
                ("confidence", models.FloatField()),
                ("model_name", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="predictions", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering":["-created_at"]},
        ),
    ]
