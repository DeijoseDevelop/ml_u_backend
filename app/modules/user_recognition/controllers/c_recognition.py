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
        image_bytes: io.BytesIO,
        data
    ) -> t.Dict[str, t.Any]:
        try:
            
            detections = self.recognition_service.call(image_bytes=image_bytes)
            io_image = self.image_manager.convert_cv2_image_to_bytes_io(self.image_manager.get_frame().get_value())
            detection = detections[0] 
            if detection["matched"]:
                ingress_data = {
                "user_id": detection["user_id"],
                "suggestions_comments": None,
                "protection_notice": True,
                "reason": data.get("service"),
                "site": data.get("site")
                }
                self.recognition_service.add_ingress_record(data=ingress_data)
            else:
                logging.error("No se pudo reconocer al usuario")

            if io_image is None:
                raise Exception("Imagen no se pudo codificar.")

            return {"data": detections, "image": io_image}

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

