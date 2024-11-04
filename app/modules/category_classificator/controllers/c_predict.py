from typing import Any
import logging

from app.modules.category_classificator import services
from app.modules.common import exceptions, interfaces


class PredictController(interfaces.BaseController):
    """
    Controlador para manejar predicciones utilizando PredictService.
    """

    def __init__(self, predict_service: services.PredictService) -> None:
        if predict_service is None:
            raise ValueError("Se requiere un PredictService válido.")

        self.predict_service = predict_service

    def predict(self, text: str) -> Any:
        """
        Realiza una predicción basada en el texto proporcionado.

        Args:
            text (str): El texto a clasificar.

        Returns:
            Any: El resultado de la predicción.

        Raises:
            UseCaseException: Si ocurre un error durante la predicción.
        """
        try:
            prediction = self.predict_service.call(text=text)
            return prediction
        except exceptions.UseCaseException as error:
            # Registrar el error y volver a lanzarlo
            logging.error(f"Error en PredictController.predict: {error.message}")
            raise error
