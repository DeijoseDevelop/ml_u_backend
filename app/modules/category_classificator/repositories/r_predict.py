from typing import Any
from pathlib import Path

import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer


class PredictRepository:
    def __init__(self, model_path: str, vectorizer_path: str) -> None:
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self.model: MultinomialNB = self._load_model()
        self.vectorizer: TfidfVectorizer = self._load_vectorizer()

    def _load_model(self) -> MultinomialNB:
        if not self.model_path.exists():
            raise FileNotFoundError(f"El modelo no se encontró en {self.model_path}")
        try:
            model = joblib.load(str(self.model_path))
            return model
        except Exception as e:
            raise Exception(f"Error al cargar el modelo: {e}")

    def _load_vectorizer(self) -> TfidfVectorizer:
        if not self.vectorizer_path.exists():
            raise FileNotFoundError(f"El vectorizador no se encontró en {self.vectorizer_path}")
        try:
            vectorizer = joblib.load(str(self.vectorizer_path))
            return vectorizer
        except Exception as e:
            raise Exception(f"Error al cargar el vectorizador: {e}")

    def predict(self, text: str) -> Any:
        """
        Realiza una predicción sobre el texto proporcionado.
        """
        if not text or not isinstance(text, str):
            raise ValueError("El texto de entrada debe ser una cadena no vacía.")
        vectorized_text = self.vectorizer.transform([text.lower()])
        prediction = self.model.predict(vectorized_text)
        return prediction[0]
