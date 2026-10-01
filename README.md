# AI-Based Fake News Detection System

A production-style Django + Django REST Framework + MySQL web application for demonstrating AI/NLP-based fake-news classification.

> **Important:** The classifier returns an AI/ML prediction, not a guarantee that a claim is true or false. Always verify important claims with reliable sources.

## 1. Features

- Registration, login, logout and Django password validation
- User profile and normal/admin roles
- News text + optional URL submission
- REST API prediction endpoint
- Reusable NLTK preprocessing
- TF-IDF + Logistic Regression baseline
- Optional SVM / Transformer extension points
- Joblib model/vectorizer persistence
- Accuracy, precision, recall, F1 and confusion matrix generated from the actual dataset
- User dashboard and prediction history
- Admin dashboard
- Chart.js visualization
- MySQL via environment variables
- CSRF protection, ORM queries and DRF throttling
- Demo dataset clearly labeled as demo only

## 2. Architecture

Browser -> Django Templates/Bootstrap/JS -> DRF API -> Prediction Service -> preprocessing -> TF-IDF -> Logistic Regression -> MySQL history.

Training is separate:

CSV -> cleaning -> train/test split -> TF-IDF -> Logistic Regression -> evaluation -> joblib model/vectorizer.

## 3. Windows installation

Open Command Prompt or PowerShell:

```powershell
cd fake_news_detection
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `mysqlclient` fails to build on Windows, install a compatible MySQL/MariaDB development environment or use the optional SQLite development mode by setting `DB_ENGINE=sqlite` in `.env`.

## 4. MySQL setup

Create a database:

```sql
CREATE DATABASE fake_news_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Create `.env` from `.env.example` and set:

```env
DJANGO_SECRET_KEY=replace-with-a-long-random-value
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=fake_news_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Never commit `.env`.

## 5. Migrations

```powershell
python manage.py makemigrations accounts detector
python manage.py migrate
```

Create an admin account:

```powershell
python manage.py createsuperuser
```

The Django superuser is automatically treated as an admin in the custom dashboard.

## 6. Demo dataset and training

The project includes `ml/dataset/demo_news.csv`.

It is deliberately small and is **not scientific evidence of real-world performance**.

Train:

```powershell
python ml/train.py
```

or:

```powershell
python manage.py train_model
```

The command prints accuracy, precision, recall, F1, confusion matrix and classification report. It saves:

- `ml/models/fake_news_logistic_regression.joblib`
- `ml/models/tfidf_vectorizer.joblib`
- `ml/models/fake_news_logistic_regression.json`

For a real experiment, replace the demo CSV with a properly licensed public dataset and set:

```env
DATASET_PATH=ml/dataset/your_dataset.csv
TEXT_COLUMN=text
LABEL_COLUMN=label
```

If your dataset uses different columns, change the environment variables. The training script expects labels that can be mapped to REAL/FAKE (for example `real/fake`, `true/false`, or `1/0`). Inspect and adapt `normalize_label()` if your dataset uses another scheme.

## 7. Run the server

```powershell
python manage.py runserver
```

Open:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/detect/
- http://127.0.0.1:8000/dashboard/
- http://127.0.0.1:8000/admin-dashboard/
- http://127.0.0.1:8000/django-admin/

## 8. API

All API endpoints require an authenticated Django session.

### POST `/api/predict/`

Request:

```json
{
  "news_text": "Paste the news article here. It should contain enough text to analyze.",
  "news_url": "https://example.com/article"
}
```

Response contains:

```json
{
  "id": 1,
  "news_text": "...",
  "news_url": "...",
  "prediction": "REAL",
  "confidence": 0.82,
  "model_name": "TF-IDF + Logistic Regression",
  "created_at": "..."
}
```

### GET `/api/history/`
Returns the current user's recent predictions.

### GET `/api/dashboard/`
Returns current-user totals and recent predictions.

### GET `/api/model-performance/`
Returns stored training metrics.

### GET `/api/admin-stats/`
Returns system statistics for admin users.

## 9. Security

- Django's built-in password hashing
- CSRF protection for session-authenticated browser requests
- ORM-based database access
- DRF authentication and permission checks
- API throttling
- Environment variables for secrets/database credentials
- Input length and URL validation
- No manual password storage
- `DEBUG=False` should be used in production
- Use HTTPS in production
- Configure secure cookies and a real secret key in production

## 10. Testing

Run:

```powershell
python manage.py test
```

Also manually test:

1. Register a new user.
2. Login/logout.
3. Open Detect and submit text before training; verify the friendly model-not-found error.
4. Run training.
5. Submit text again.
6. Verify the result and confidence.
7. Verify history and dashboard counts.
8. Create a superuser and verify admin dashboard.
9. Verify invalid/short text and invalid URL errors.
10. Verify anonymous users cannot access prediction API.

## 11. Model limitations

The baseline model is a text classifier. It does not fact-check claims against the internet. Accuracy can change substantially when moving from the demo dataset to a real dataset or to new topics and sources. Dataset leakage, class imbalance, source artifacts, satire, multilingual content, and distribution shift should be evaluated in a proper research experiment.

## 12. Optional model improvements

- Linear SVM comparison
- DistilBERT / other Transformer classifier
- Class-weighting and calibrated probabilities
- Better multilingual preprocessing
- Explainability with SHAP/LIME
- Source/domain reputation features
- Retrieval-based claim verification
- Human review workflow
- Model versioning and experiment tracking
- Celery/background training jobs
- Production logging and monitoring
- Docker deployment
- Automated CI/CD

## 13. Screenshots placeholders

Add screenshots of:

- Home page
- Registration/Login
- Detection page
- Result card
- User dashboard
- Prediction history
- Admin dashboard
- API response
- Model training terminal

## 14. Project structure

See the complete folder tree delivered with this project.

## 15. License

Choose an appropriate license before public deployment. Also verify the license/terms of any external dataset you use.
