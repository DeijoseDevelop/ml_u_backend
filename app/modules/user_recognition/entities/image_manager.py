import io
import typing as t

import cv2
import cv2.typing
import numpy as np

from .frame import Frame
from app.modules.common import interfaces


class ImageManager(interfaces.Manager):

    def __init__(self) -> None:
        self._frame = Frame()

    def get_frame(self) -> Frame:
        return self._frame

    def set_frame(self, frame: cv2.typing.MatLike) -> None:
        self._frame.set_value(frame)

    def draw_rectangle(self, positions: t.Tuple[int, int, int, int], thickness: int) -> None:
        (top, right, bottom, left) = positions
        cv2.rectangle(
            self._frame.get_value(),
            (left, top), (right, bottom),
            (0, 0, 255), thickness
        )

    def draw_text(self, name: str, positions: t.Tuple[int, int, int, int], thickness: int) -> None:
        (top, right, bottom, left) = positions
        cv2.putText(
            self._frame.get_value(), name,
            (left + 6, bottom - 6),
            cv2.FONT_HERSHEY_DUPLEX,
            0.5, (255, 255, 255), thickness
        )

    def show_image(self) -> None:
        cv2.imshow('image', self._frame.get_value())

    def convert_bytes_to_cv2_image(self, data: io.BytesIO) -> cv2.typing.MatLike:
        data.seek(0)

        nparr = np.frombuffer(data.read(), np.uint8)
        cv2_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return cv2_image

    def convert_cv2_image_to_bytes_io(self, image: cv2.typing.MatLike) -> io.BytesIO | None:
        is_success, buffer = cv2.imencode(".jpeg", image)

        if is_success:
            return io.BytesIO(buffer)

    def convert_cv2_image_to_bytes(self, image: cv2.typing.MatLike) -> bytes:
        is_success, buffer = cv2.imencode(".jpeg", image)

        if is_success:
            return buffer.tobytes()

    def resize_image(self, image: cv2.typing.MatLike, scale_percent: float):
        width = int(image.shape[1] * scale_percent / 100)
        height = int(image.shape[0] * scale_percent / 100)
        dim = (width, height)
        return cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
