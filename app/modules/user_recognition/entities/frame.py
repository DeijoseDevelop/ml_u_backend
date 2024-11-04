import typing as t

import cv2
import cv2.typing

class Frame(object):

    def __init__(self) -> None:
        self._value: cv2.typing.MatLike | None
        self._rgb_value: cv2.typing.MatLike | None

    def get_value(self) -> cv2.typing.MatLike | None:
        return self._value

    def get_rgb_value(self) -> cv2.typing.MatLike | None:
        return self._rgb_value

    def set_value(self, frame: cv2.typing.MatLike) -> "Frame":
        self._value = frame
        return self

    def convert_to_rgb(self) -> "Frame":
        self._rgb_value = cv2.cvtColor(self._value, cv2.COLOR_BGR2RGB)
        return self