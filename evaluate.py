import json
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
metrics_file = BASE_DIR / "ml/models/fake_news_logistic_regression.json"
if not metrics_file.exists():
    print("No evaluation file found. Run python ml/train.py first.")
else:
    print(metrics_file.read_text(encoding="utf-8"))
