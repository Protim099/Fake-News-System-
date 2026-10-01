import re
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def ensure_nltk_resources():
    resources = [
        ("corpora/stopwords", "stopwords"),
        ("corpora/wordnet", "wordnet"),
        ("tokenizers/punkt", "punkt"),
    ]
    for path, package in resources:
        try:
            nltk.data.find(path)
        except LookupError:
            nltk.download(package, quiet=True)

ensure_nltk_resources()
STOPWORDS = set(stopwords.words("english"))
LEMMATIZER = WordNetLemmatizer()

def clean_text(text: str, use_lemmatization: bool = True) -> str:
    text = "" if text is None else str(text)
    text = BeautifulSoup(text, "html.parser").get_text(" ")
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = re.findall(r"[a-z]+", text)
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]
    if use_lemmatization:
        tokens = [LEMMATIZER.lemmatize(t) for t in tokens]
    return " ".join(tokens)
