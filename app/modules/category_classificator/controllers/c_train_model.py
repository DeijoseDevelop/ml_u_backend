from typing import Dict, List
import logging

from app.modules.category_classificator import services
from app.modules.common import exceptions, interfaces


class TrainModelController(interfaces.BaseController):
    """
    Controlador para manejar el entrenamiento del modelo utilizando CleanDataService y TrainModelService.
    """

    def __init__(
        self,
        clean_data_service: services.CleanDataService,
        train_model_service: services.TrainModelService,
    ) -> None:
        if clean_data_service is None or train_model_service is None:
            raise ValueError("Se requieren servicios válidos para CleanData y TrainModel.")

        self.clean_data_service = clean_data_service
        self.train_model_service = train_model_service

    def train(self) -> str:
        """
        Entrena el modelo utilizando los datos obtenidos de CleanDataService.

        Returns:
            str: Mensaje de éxito al completar el entrenamiento.

        Raises:
            UseCaseException: Si ocurre un error durante el entrenamiento.
        """
        try:
            data = self.get_data()
            self.train_model_service.call(
                texts=data["texts"],
                labels=data["labels"]
            )
            return "Entrenamiento completado con éxito."
        except exceptions.UseCaseException as error:
            logging.error(f"Error en TrainModelController.train: {error.message}")
            raise

    def get_data(self) -> Dict[str, List[str]]:
        """
        Obtiene los datos de entrenamiento desde CleanDataService.

        Returns:
            Dict[str, List[str]]: Un diccionario con las claves 'texts' y 'labels'.

        Raises:
            UseCaseException: Si ocurre un error al obtener los datos.
        """
        try:
            texts, labels = self.clean_data_service.call()
            return {"texts": texts, "labels": labels}
        except exceptions.UseCaseException as error:
            logging.error(f"Error en TrainModelController.get_data: {error.message}")
            raise error
