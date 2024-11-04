import io
import typing as t
import logging

import cv2
import cv2.typing

from app.modules.common import exceptions, interfaces
from app.modules.user_recognition import entities, services


class RecognitionController(interfaces.BaseController):

    def __init__(
        self,
        recognition_service: services.RecognitionService,
        image_manager: entities.ImageManager
    ) -> None:
        self.recognition_service = recognition_service
        self.image_manager = image_manager

    def detect_face(
        self,
        image_bytes: io.BytesIO
    ) -> t.Dict[str, t.Any]:
        try:
            detection = self.recognition_service.call(image_bytes=image_bytes)
            io_image = self.image_manager.convert_cv2_image_to_bytes_io(self.image_manager.get_frame().get_value())

            if io_image is None:
                raise Exception("Imagen no se pudo codificar.")

            return {"data": detection, "image": io_image}

        except exceptions.UseCaseException as error:
            logging.error(f"UseCaseException in detect_face: {error}")
            raise error

        except Exception as error:
            logging.error(f"Unexpected error in detect_face: {error}")
            raise error


    def convert_bytes_to_cv2_image(self, data: io.BytesIO) -> cv2.typing.MatLike:
        self.image_manager.convert_bytes_to_cv2_image(data=data)

    def convert_cv2_image_to_bytes(self, image: cv2.typing.MatLike) -> bytes:
        self.image_manager.convert_cv2_image_to_bytes(image=image)

