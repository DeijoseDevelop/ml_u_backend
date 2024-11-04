from typing import Any

from app.modules.common import interfaces
from app.modules.category_classificator import repositories
from app.modules.common import exceptions


class PredictService(interfaces.Service):
    """
    Servicioso para realizar predicciones utilizando PredictRepository.
    """

    def __init__(self, repository: repositories.PredictRepository) -> None:
        if repository is None:
            raise ValueError("Se requiere un PredictRepository válido.")
        self.repository = repository

    def call(self, text: str) -> Any:
        """
        Realiza una predicción basada en el texto proporcionado.

        Args:
            text (str): El texto sobre el cual se realizará la predicción.

        Returns:
            Any: El resultado de la predicción.

        Raises:
            ValueError: Si el texto proporcionado no es una cadena válida.
            UseCaseException: Si ocurre un error durante la predicción.
        """
        if not text or not isinstance(text, str):
            raise ValueError("El texto de entrada debe ser una cadena no vacía.")
        try:
            prediction = self.repository.predict(text)
            return prediction
        except Exception as error:
            raise exceptions.UseCaseException(f"Error al realizar la predicción: {error}") from error
