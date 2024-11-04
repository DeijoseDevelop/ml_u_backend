
import io
import typing as t

from app.modules.common import interfaces
from app.modules.user_recognition import repositories
from app.modules.common import exceptions

class RecognitionService(interfaces.Service):

    def __init__(self, repository: repositories.RecognitionRepository):
        self.repository = repository

    def call(self, image_bytes: io.BytesIO) -> t.List[t.Dict[str, str | bool | t.Tuple[int, t.Any, t.Any, int]]]:
        detection = self.repository.detect_face(image_bytes=image_bytes)

        if len(detection) == 0:
            raise exceptions.UseCaseException(message="Coincidencias no detectadas")

        return detection