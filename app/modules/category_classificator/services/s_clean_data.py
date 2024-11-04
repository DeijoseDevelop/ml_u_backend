from typing import List, Tuple, Optional

from app.modules.common import interfaces
from app.modules.category_classificator import repositories
from app.modules.common import exceptions


class CleanDataService(interfaces.Service):
    """
    Servicio para limpiar y preparar los datos utilizando CleanDataRepository.
    """

    def __init__(self, repository: Optional[repositories.CleanDataRepository] = None) -> None:
        if repository is None:
            raise ValueError("Se requiere un CleanDataRepository válido.")
        self.repository = repository

    def call(self) -> Tuple[List[str], List[str]]:
        """
        Llama al método 'clean' del repositorio y retorna los textos y etiquetas.

        Returns:
            Tuple[List[str], List[str]]: Una tupla con listas de textos y etiquetas.

        Raises:
            UseCaseException: Si ocurre un error al limpiar los datos.
        """
        try:
            texts, labels = self.repository.clean()
            return texts, labels
        except Exception as error:
            raise exceptions.UseCaseException(f"Error al limpiar los datos: {error}") from error
