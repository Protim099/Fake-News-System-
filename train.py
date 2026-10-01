import argparse
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from ml.preprocessing import clean_text

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

def normalize_label(value):
    s = str(value).strip().lower()
    if s in {"fake", "false", "0", "f", "1_fake"}:
        return "FAKE"
    if s in {"real", "true", "1", "r", "0_real"}:
        return "REAL"
    return str(value).strip().upper()

def train(dataset_path, text_column="text", label_column="label", model_path=None, vectorizer_path=None):
    df = pd.read_csv(dataset_path)
    if text_column not in df.columns or label_column not in df.columns:
        raise ValueError(
            f"Dataset must contain '{text_column}' and '{label_column}'. "
            f"Available columns: {list(df.columns)}"
        )
    df = df[[text_column, label_column]].dropna()
    df[text_column] = df[text_column].astype(str).map(clean_text)
    df[label_column] = df[label_column].map(normalize_label)
    df = df[df[text_column].str.len() > 0]
    df = df[df[label_column].isin(["REAL", "FAKE"])]
    if df[label_column].nunique() < 2:
        raise ValueError("Training data must contain both REAL and FAKE labels.")

    X_train, X_test, y_train, y_test = train_test_split(
        df[text_column], df[label_column], test_size=0.2, random_state=42, stratify=df[label_column]
    )

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_df=0.98, sublinear_tf=True)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    model.fit(X_train_vec, y_train)
    y_pred = model.predict(X_test_vec)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, pos_label="FAKE", zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, pos_label="FAKE", zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, pos_label="FAKE", zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, y_pred, labels=["REAL", "FAKE"]).tolist(),
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
        "test_size": len(y_test),
        "train_size": len(y_train),
    }

    model_path = Path(model_path or BASE_DIR / "ml/models/fake_news_logistic_regression.joblib")
    vectorizer_path = Path(vectorizer_path or BASE_DIR / "ml/models/tfidf_vectorizer.joblib")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    vectorizer_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    with open(model_path.with_suffix(".json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print("\n=== Fake News Model Evaluation ===")
    for key in ("accuracy", "precision", "recall", "f1_score"):
        print(f"{key}: {metrics[key]:.4f}")
    print("\nConfusion matrix [REAL, FAKE]:")
    print(metrics["confusion_matrix"])
    print("\nClassification report:")
    print(metrics["classification_report"])
    return metrics

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=os.getenv("DATASET_PATH", "ml/dataset/demo_news.csv"))
    parser.add_argument("--text-column", default=os.getenv("TEXT_COLUMN", "text"))
    parser.add_argument("--label-column", default=os.getenv("LABEL_COLUMN", "label"))
    parser.add_argument("--model-path", default=os.getenv("MODEL_PATH", "ml/models/fake_news_logistic_regression.joblib"))
    parser.add_argument("--vectorizer-path", default=os.getenv("VECTORIZER_PATH", "ml/models/tfidf_vectorizer.joblib"))
    args = parser.parse_args()
    train(args.dataset, args.text_column, args.label_column, args.model_path, args.vectorizer_path)
