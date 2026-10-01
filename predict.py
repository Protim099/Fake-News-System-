from pathlib import Path
import joblib
from django.conf import settings
from ml.preprocessing import clean_text

BASE_DIR = Path(__file__).resolve().parent.parent

class PredictionService:
    def __init__(self):
        self.model_path = BASE_DIR / settings.MODEL_PATH
        self.vectorizer_path = BASE_DIR / settings.VECTORIZER_PATH
        if not self.model_path.exists() or not self.vectorizer_path.exists():
            raise FileNotFoundError(
                "Trained model not found. Run: python ml/train.py"
            )
        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)

    def predict(self, text):
        cleaned = clean_text(text)
        if not cleaned.strip():
            raise ValueError("News text contains no usable words after preprocessing.")
        X = self.vectorizer.transform([cleaned])
        prediction = str(self.model.predict(X)[0]).upper()
        probabilities = self.model.predict_proba(X)[0]
        classes = [str(c).upper() for c in self.model.classes_]
        confidence = float(max(probabilities))
        return {
            "prediction": prediction,
            "confidence": confidence,
            "model_name": "TF-IDF + Logistic Regression",
        }
