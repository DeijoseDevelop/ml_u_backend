import typing as t
from typing import Any
from pathlib import Path

from scipy.sparse import spmatrix
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


class TrainModelRepository:
    def __init__(self, model_path: str, vectorizer_path: str) -> None:
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self.model = MultinomialNB()
        self.vectorizer = TfidfVectorizer()
        self.x_train_tfidf: spmatrix = None
        self.y_train: t.List[str] = []

    def train(self, texts: t.List[str], labels: t.List[str]) -> None:
        """
        Entrena el modelo con los textos y etiquetas proporcionados.
        """
        self._preprocess_data(texts, labels)
        self._vectorize_data()
        self.model.fit(self.x_train_tfidf, self.y_train)

    def _preprocess_data(self, texts: t.List[str], labels: t.List[str]) -> None:
        """
        Divide los datos en conjuntos de entrenamiento y prueba.
        """
        x_train, _, y_train, _ = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )
        self.x_train = x_train
        self.y_train = y_train

    def _vectorize_data(self) -> None:
        """
        Convierte los textos de entrenamiento en una matriz TF-IDF.
        """
        self.x_train_tfidf = self.vectorizer.fit_transform(self.x_train)

    def save_model(self) -> None:
        """
        Guarda el modelo entrenado y el vectorizador en las rutas especificadas.
        """
        try:
            joblib.dump(self.model, str(self.model_path))
            joblib.dump(self.vectorizer, str(self.vectorizer_path))
            print(f"Modelo guardado en {self.model_path}")
            print(f"Vectorizador guardado en {self.vectorizer_path}")
        except Exception as e:
            raise Exception(f"Error al guardar el modelo o vectorizador: {e}")
