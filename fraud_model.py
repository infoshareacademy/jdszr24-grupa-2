"""Wspólny moduł modelu fraud detection — używany przez predict.py i app.py.

Model: strojony las losowy (parametry z notebooka Ocean's_Four_Project.ipynb)
opakowany w kalibrację prawdopodobieństw (Platt). Przy pierwszym użyciu trenuje
się na data/credit_card_fraud_10k.csv (~kilkanaście sekund) i zapisuje do
models/fraud_model.joblib — kolejne uruchomienia wczytują gotowy plik.
"""
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "credit_card_fraud_10k.csv")
MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_model.joblib")
RANDOM_STATE = 42

CATEGORIES = ["Clothing", "Electronics", "Food", "Grocery", "Travel"]

# kolejność i nazwy cech wejściowych modelu
FEATURES = ["amount", "transaction_hour", "merchant_category",
            "foreign_transaction", "location_mismatch", "device_trust_score",
            "velocity_last_24h", "cardholder_age"]


def hour_to_sin_cos(X):
    h = np.asarray(X, dtype=float)
    return np.column_stack([np.sin(2 * np.pi * h[:, 0] / 24),
                            np.cos(2 * np.pi * h[:, 0] / 24)])


def hour_feature_names(transformer, names):
    return ["hour_sin", "hour_cos"]


def make_preprocess():
    return ColumnTransformer([
        ("cat", OneHotEncoder(drop="first"), ["merchant_category"]),
        ("hour", FunctionTransformer(
            hour_to_sin_cos, feature_names_out=hour_feature_names),
            ["transaction_hour"]),
        ("num", StandardScaler(), ["amount", "foreign_transaction",
                                   "location_mismatch", "device_trust_score",
                                   "velocity_last_24h", "cardholder_age"]),
    ])


def train(data_path: str = DATA_PATH):
    """Trenuje skalibrowany model na pełnym zbiorze."""
    df = pd.read_csv(data_path).drop_duplicates()
    X = df[FEATURES]
    y = df["is_fraud"]

    base = Pipeline([
        ("prep", make_preprocess()),
        ("model", RandomForestClassifier(
            n_estimators=400, min_samples_leaf=2, class_weight="balanced",
            n_jobs=-1, random_state=RANDOM_STATE)),
    ])
    model = CalibratedClassifierCV(base, method="sigmoid", cv=5)
    model.fit(X, y)
    return model


def load_or_train():
    """Wczytuje model z dysku albo trenuje i zapisuje przy pierwszym użyciu."""
    if os.path.exists(MODEL_PATH):
        try:
            return joblib.load(MODEL_PATH)
        except Exception:
            os.remove(MODEL_PATH)  # uszkodzony/niekompatybilny plik — trenujemy od nowa
    model = train()
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    tmp_path = MODEL_PATH + ".tmp"
    joblib.dump(model, tmp_path)
    os.replace(tmp_path, MODEL_PATH)  # zapis atomowy — brak wpół zapisanych plików
    return model


def predict_proba_one(model, transaction: dict) -> float:
    """Zwraca prawdopodobieństwo fraudu dla pojedynczej transakcji (dict z FEATURES)."""
    X = pd.DataFrame([transaction], columns=FEATURES)
    return float(model.predict_proba(X)[:, 1][0])
