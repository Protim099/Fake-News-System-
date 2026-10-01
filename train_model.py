import os
from django.core.management.base import BaseCommand
from django.conf import settings
from detector.models import ModelPerformance
from ml.train import train

class Command(BaseCommand):
    help = "Train the fake-news classifier and save evaluation metrics."

    def add_arguments(self, parser):
        parser.add_argument("--dataset", default=settings.DATASET_PATH)
        parser.add_argument("--text-column", default=settings.TEXT_COLUMN)
        parser.add_argument("--label-column", default=settings.LABEL_COLUMN)

    def handle(self, *args, **options):
        metrics = train(
            options["dataset"],
            options["text_column"],
            options["label_column"],
            settings.MODEL_PATH,
            settings.VECTORIZER_PATH,
        )
        ModelPerformance.objects.create(
            model_name="TF-IDF + Logistic Regression",
            accuracy=metrics["accuracy"],
            precision=metrics["precision"],
            recall=metrics["recall"],
            f1_score=metrics["f1_score"],
        )
        self.stdout.write(self.style.SUCCESS("Model trained and performance saved."))
