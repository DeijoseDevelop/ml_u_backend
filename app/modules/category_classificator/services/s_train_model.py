from typing import List, Dict, Any

from app.modules.common import interfaces
from app.modules.category_classificator import repositories
from app.modules.common import exceptions


class TrainModelService(interfaces.Service):
    """
    Servicio para entrenar un modelo utilizando TrainModelRepository.
    """

    def __init__(self, repository: repositories.TrainModelRepository) -> None:
        if repository is None:
            raise ValueError("Se requiere un TrainModelRepository válido.")
        self.repository = repository

    def call(self, texts: List[str], labels: List[str]) -> None:
        """
        Entrena el modelo con los textos y etiquetas proporcionados.

        Args:
            texts (List[str]): Lista de textos de entrenamiento.
            labels (List[str]): Lista de etiquetas correspondientes.

        Raises:
            ValueError: Si los textos y etiquetas no son listas no vacías de igual longitud.
            UseCaseException: Si ocurre un error durante el entrenamiento.
        """
        if not texts or not labels or len(texts) != len(labels):
            raise ValueError("Los textos y etiquetas deben ser listas no vacías de igual longitud.")
        try:
            data = {"texts": texts, "labels": labels}
            self.repository.train(
                texts=data["texts"],
                labels=data["labels"]
            )
        except Exception as error:
            raise exceptions.UseCaseException(f"Error al entrenar el modelo: {error}") from error
